

from sklearn_crfsuite import metrics
import pickle
from itertools import groupby
import ast
import pandas as pd
import os

class Predict():

    ALL_LETTERS        = {"'", "b", "t", "j", "x", "kh", "d", "r", "s", "sh", 
                        "dh","c", "g", "f", "q", "k", "l", "m", "n", "w", "h", "y", 
                        "a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo", 
                        "ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"}

    CONSONANTS         = {"'", "b", "t", "j", "x", "kh", "d", "r", "s", "sh", "dh",
                        "c", "g", "f", "q", "k", "l", "m", "n", "w", "h", "y"}

    CONS_DIGRAPH       = {"kh", "sh", "dh"}

    CONS_BAR_DIGRAPHS  = {"'", "b", "t", "j", "x", "d", "r", "s", "c", "g", 
                        "f", "q", "k", "l", "m", "n", "w", "h", "y"}

    # defining all vowel variations
    SHORT_VOWELS       = {"a", "i", "u", "e", "o"}
    LONG_VOWELS        = {"aa", "ii", "uu", "ee", "oo"}

    VOLATILE_DIPHTH    = {"ay", "aw", "ey", "oy", "ow"}
    LONG_DIPHTH        = {"aay", "aaw", "eey", "ooy", "oow"}

    # defining vowel short hands
    DIPHTHONGS         = {"ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"}
    VOWELS_BAR_DIPHTH  = {"a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo"}

    VOWELS_INCL_DIPHTH = {"a", "i", "u", "e", "o", "aa", "ii", "uu", "ee", "oo", 
                        "ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"}


    # utils.py
    

    # LONG_VOWELS = {'aa', 'ee', 'ii', 'oo', 'uu'}
    # DIPHTHONGS = {'ay', 'aw', 'ey', 'ow'}
    # LONG_VOWELS = {"aa", "ii", "uu", "ee", "oo"}
    # LONG_DIPHTH = {"aay", "aaw", "eey", "ooy", "oow"}

    # DIPHTHONGS  = {"ay", "aw", "ey", "oy", "ow", "aay", "aaw", "eey", "ooy", "oow"}
    # VOLATILE_DIPHTH = {"ay", "aw", "ey", "oy", "ow"}

    

    def has_long_diphthong(self, syl):
        return any(vv in syl for vv in self.LONG_DIPHTH)

    def has_long_vowel(self, syl):
        return any(vv in syl for vv in self.LONG_VOWELS)

    #TODO: what's going on here??
    def has_Diphthong(self, syl):
        return any(d in syl for d in self.VOLATILE_DIPHTH)
    
    def has_diphthong(self, syl):
        return any(vv in syl for vv in self.DIPHTHONGS)

    def has_coda(self, syl):
        if syl == 'SP':
            return False
        vowels = 'aeiou' #TODO: this aint right, use real vowels
        return len(syl) > 0 and syl[-1].isalpha() and syl[-1] not in vowels


    # def get_syl_type(syl="SP", label="S"):
    #     '''be sure to pass in syllable always and correct label when syllable is not SP'''
    #     if syl == 'SP':
    #         return 'SP'
    #     elif label == 'S':
    #         return 'short'
    #     elif label == 'L':
    #         return 'long'
        
    def get_syl_type(self, s):
            if self.has_long_vowel(s) or self.has_long_diphthong(s):
                return "L"
            elif (not self.has_Diphthong(s)):
                return "S"
            else:
                return "?"

    def get_word_boundaries(self, syllables_w_sp):
        """Extract word_start/word_end for syllables-only sequence."""
        res = []
        for k, g in groupby(syllables_w_sp, lambda x: x == 'SP'):
            if not k:
                res.append(list(g))
        
        word_start, word_end = [], []
        for word in res:
            if word:
                word_start.append(word[0])
                word_end.append(word[-1])
        return word_start, word_end


    #TODO: ensure this logic is deterministic. ie, are the categories going to be check in the specific order?
    # LONG_DIPHTH --> LONG_VOWELS --> DIPHTHONGS --> SHORT_VOWELS
    def get_nucleus(self, curr_syll):
        """Extract nucleus from syllable."""
        if curr_syll == 'SP':
            return ''
        
        # Combine all categories into a single sorted list (longest first)
        for category in [self.LONG_DIPHTH, self.LONG_VOWELS, self.DIPHTHONGS, self.SHORT_VOWELS]:
            for item in category:
                if item in curr_syll:
                    return item
        return ''


    def word2features_syllables(self, syl_len, syllables, curr_syll, 
                                i, word_start, word_end):
        """Feature extractor for syllable i (no labels needed in features)."""
        features = {}

        #set up
        features['prev_nucleus'] = ''
        features['curr_nucleus'] = ''
        features['next_nucleus'] = ''
        features['prev_has_coda'] = False
        features['next_has_coda'] = False
        features['post_initial'] = False
        features['penultimate'] = False

        # Basic features
        # commenting these out had no impact
        features['syll_length'] = len(curr_syll)

        # Phonology
        # commenting these out had no impact
        features['vowel:long']   = self.has_long_vowel(curr_syll)
        features['vowel:longdiph'] = self.has_long_diphthong(curr_syll)
        features['vowel:diph']   = self.has_Diphthong(curr_syll)
        features['vowel:short']  = not self.has_long_vowel(curr_syll)
        features['has_coda']     = self.has_coda(curr_syll)
        features['curr_nucleus'] = self.get_nucleus(curr_syll)

        # Word structure
        # commenting these out had no impact
        features['is_word_start'] = (curr_syll in word_start)
        features['is_word_end']   = (curr_syll in word_end)
        
        # Position
        # commenting these out had no impact
        features['BOS']   = (i == 0)
        features['EOS']   = (i == (syl_len - 1))
        #comment these out later
        features['pos=1'] = (i == 0)
        features['pos=2'] = (i == 1)
        features['early'] = ((i / syl_len) < 0.3)
        features['late']  = ((i / syl_len) > 0.7)
        
        # Context
                    #commenting these out had a big impact
                    #just two highlighted bigrams alone could produce 1.0000 accuracy
                                #all above features                     produced 0.9885 accuracy
                                #all other features (excluding bigrams) produced 0.9900 accuracy

                    #the other features below alone got an overall accuracy of 0.7312 . I.G. they're not needed and the bigrams alone are doing all the heavy lifting.
        if i > 0:
            # prev_type = get_syl_type(syllables[i - 1], labels[i - 1])
            # curr_type = get_syl_type(curr_syll, curr_label)

            prev_type = self.get_syl_type(syllables[i - 1])
            curr_type = self.get_syl_type(curr_syll)

            features[f'prev_bigram_type:{prev_type}-{curr_type}'] = True # this one
            features['prev_nucleus'] = self.get_nucleus(syllables[i - 1])
            features['prev_has_coda'] = self.has_coda(syllables[i - 1])
            features['post_initial'] = (syllables[i - 1] in word_start)

        if i < syl_len - 1:
            # next_type = get_syl_type(syllables[i + 1], labels[i + 1])
            # curr_type = get_syl_type(curr_syll, curr_label)

            next_type = self.get_syl_type(syllables[i + 1])
            curr_type = self.get_syl_type(curr_syll)

            features[f'next_bigram_type:{curr_type}-{next_type}'] = True # and this one
            features['next_nucleus'] = self.get_nucleus(syllables[i + 1])
            features['next_has_coda'] = self.has_coda(syllables[i + 1])
            features['penultimate'] = (syllables[i + 1] in word_end)
        
        return features

    def load_and_prepare_df(self, df):
        """Load df and return X (features), y (labels) for CRF."""

        # df = df.head(n=500)
        
        # Parse list columns
        # df['syllables'] = df['syllables'].apply(ast.literal_eval)
        # # df['labels'] = df['labels'].apply(ast.literal_eval)
        # df['syllables_w_SP'] = df['syllables_w_SP'].apply(ast.literal_eval)
        
        # Compute word boundaries
        word_info = df['syllables_w_SP'].apply(self.get_word_boundaries)
        df['word_start'] = [info[0] for info in word_info]
        df['word_end']   = [info[1] for info in word_info]
        
        # Build X and y
        X, y = [], []
        count = 0

        try:
            for _, row in df.iterrows():
                syllables = row['syllables']
                # labels = row['labels']
                ws = row['word_start']
                we = row['word_end']

                # print("Debugging row:", count)
                count += 1
                # print("syllables")
                # display(syllables)
                # print("labels")
                # display(labels)
                # print("word_start")
                # display(ws)
                # print("word_end")
                # display(we)
                
                # Validate lengths
                # assert len(syllables) == len(labels), "Word length mismatch!"
                assert len(ws) == len(we), "End-Start length mismatch!"
                
                
                # Feature extraction
                feats = [
                    self.word2features_syllables(len(syllables), syllables, syllables[i], i, ws, we) for i in range(len(syllables))
                ]
                # labels, labels[i]

                X.append(feats)
                # y.append(labels)
        except Exception as e:
            print(f"Error processing row {count}: {e}")
            print("Syllables:", syllables)
            # print("Labels:", labels)
            print("Word Start:", ws)
            print("Word End:", we)

            raise e
        
        return X, y, df  # return df for debugging if needed


    def load_and_prepare_csv(self, filepath):
        """Load CSV and return X (features), y (labels) for CRF."""
        df = self.pd.read_csv(filepath)
        
        return self.load_and_prepare_df(df)

    # evaluate.py
    # from utils import load_and_prepare
    
    # Load model

    def predict_syll(self, df, model_path=None):

        if model_path is None:
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(base_dir, 'jiifto_crf.pkl')

        with open(model_path, 'rb') as f:
            crf = pickle.load(f)

        # Load test data
        # print("Loading test data...")
        X_test, y_test, df_test = self.load_and_prepare_df(df)
        # print(f"Loaded {len(X_test)} test lines.")

        # Predict
        # print("Predicting...")
        y_pred = crf.predict(X_test)

        return y_pred

# Evaluate
# labels = ['L', 'S']
# print("\nClassification Report:")
# print(metrics.flat_classification_report(y_test, y_pred, labels=labels, digits=4))

# acc = accuracy_score(y_test, y_pred)
# print(f"\nOverall Accuracy: {acc:.4f}")

# Optional: Save predictions
# import pandas as pd
# df_test = ... (if you returned df from load_and_prepare)
# Add predictions to analyze errors