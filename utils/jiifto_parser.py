#@title libraries and imports
import io
import sys
import re
import os
import pandas as pd
import ast

class Parser():

    #TODO
    '''
    make an init func that stores all parsed strings into a df and computes their corresponding SP syllablifed lines
    '''

    #@title consonant and vowel definitions

    # orthographic inventory of standard Maxaa dialect Somali

    ALL_LETTERS        = ["'", "b", "t", "j", "x", "kh", "d", "r", "s", "sh", 
                        "dh","c", "g", "f", "q", "k", "l", "m", "n", "w", "h", "y", 
                        "a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo", 
                        "ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"]

    CONSONANTS         = ["'", "b", "t", "j", "x", "kh", "d", "r", "s", "sh", "dh",
                        "c", "g", "f", "q", "k", "l", "m", "n", "w", "h", "y"]

    CONS_DIGRAPH       = ["kh", "sh", "dh"]

    CONS_BAR_DIGRAPHS  = ["'", "b", "t", "j", "x", "d", "r", "s", "c", "g", 
                        "f", "q", "k", "l", "m", "n", "w", "h", "y"]

    # defining all vowel variations
    SHORT_VOWELS       = ["a", "i", "u", "e", "o"]
    LONG_VOWELS        = ["aa", "ii", "uu", "ee", "oo"]

    VOLATILE_DIPHTH    = ["ay", "aw", "ey", "oy", "ow"]
    LONG_DIPHTH        = ["aay", "aaw", "eey", "ooy", "oow"]

    # defining vowel short hands
    DIPHTHONGS         = ["ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"]
    VOWELS_BAR_DIPHTH  = ["a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo"]

    VOWELS_INCL_DIPHTH = ["a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo", 
                        "ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"]

    #@title split_into_syllables

    # name:        split_into_syllables
    #
    # inputs:      a word
    #
    # return:      a list of the syllables in word
    #
    # description: create a list of syllables from a given 
    #              word in standard Maxaa dialect Somali
    #
    # notes:       consonant clusters are >=3 consonants are ignored
    #              and no error is raised, even though they break 
    #              standard Somali orthography

    def split_into_syllables(self, word):

        syllables = []
        curr_char = ""
        i = 0

        index_last_char = len(word)

        while i < len(word):

            
                # check against indexing out of range
                if (i == index_last_char - 1):
                        curr_char += word[i]
                        i += 1

                # Check if current character is a consonant cluster (sh, kh, dh)
                elif word[i:i+2] in self.CONS_DIGRAPH:  # (shouldn't the check be this then??)
                # elif word[i:i+2] in CONSONANTS:
                    curr_char += word[i:i+2]
                    i += 2

                elif word[i] in self.CONSONANTS:
                    curr_char += word[i]
                    i += 1
                
                elif word[i] not in self.ALL_LETTERS:
                    curr_char += word[i]
                    print("error, there seem to be non-Somali letters:", word[i])
                    i += 1


                # Check if current character is a vowel
                if word[i:i+3] in self.VOWELS_BAR_DIPHTH:

                # If the current syllable is not empty
                # and the next character is a vowel
                    # add the current syllable to the list and reset it
                    if ((curr_char) and 
                        (i + 3 < len(word)) and 
                        (word[i+3] in self.VOWELS_BAR_DIPHTH)):
                        syllables.append(curr_char)
                        curr_char = ""
                    
                    curr_char += word[i:i+3]
                    i += 3

                elif word[i:i+2] in self.VOWELS_BAR_DIPHTH:
                    curr_char += word[i:i+2]
                    i += 2

                elif (i != index_last_char):
                    if (word[i] in self.VOWELS_BAR_DIPHTH):
                        curr_char += word[i]
                        i += 1

            # Add the current syllable to the list and reset
                if curr_char:  # if curr_char not empty             
                    syllables.append(curr_char)
                    curr_char = ""

        # correct error coda consonants are incorrectly
        # indexed on their own and trail behind

        corrected_syllables = self.correct_codas(syllables)
        return syllables



    #@title correct_codas

    # name:           correct_codas
    #
    # inputs:         a list of syllables that
    #
    # return:         the corrected list of syllables
    #
    # description:    picks up trailing consonants and attaches them
    #                 to the previous syllable as its coda

    def correct_codas(self, syllabified_word):

        counter = 0
        new_word = ""

        for i in syllabified_word:
            if i in self.CONSONANTS:
                if counter == 0:
                    #preserve 0th index initial consonant cluster
                    new_word = i + syllabified_word[counter + 1]
                    syllabified_word[counter + 1] = new_word
            
                else:
                    new_word = syllabified_word[counter - 1] + i
                    syllabified_word[counter - 1] = new_word

                syllabified_word.remove(i)
                new_word = ""

            counter += 1
        return syllabified_word



    #@title parse_line

    # name:           parse_line
    #
    # inputs:         string
    #
    # return:         properly syllabified string
    #
    # description:    take any string in standard Maxaa-dialect Somali and
    #                 parse it into a list of syllables
    #

    def parse_line(self, line):
        line = line.lower().strip() #TODO: test to make sure strip() doesn't break anything
        # remove all non-alphabet characters
        line = line.replace("’", "'")
        line = line.replace("-", " ")
        regex = re.compile('[^a-zA-Z\' ]')
        line = regex.sub(' ', line)

        word_arr = line.split()

        parsed_line = []
        for word in word_arr:
            syllables = self.split_into_syllables(word)
            parsed_line += syllables

        # unsure why I need to correct here?
        # leave as is for now
        parsed_line = self.correct_codas(parsed_line) #TODO fix this error
        return parsed_line


    def insert_spaces(self, text, tokens):
        text = text.replace("’", "'")
        text = text.strip()
        result = []
        token_idx = 0

        i = 0
        while i < len(text):
            if text[i] == " ":
                result.append("SP")
                i += 1
            else:
                token = tokens[token_idx]
                result.append(token)
                i += len(token)
                token_idx += 1

        return result




    