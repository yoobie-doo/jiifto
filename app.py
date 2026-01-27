import streamlit as st
from utils.jiifto_parser  import Parser
from utils.jiifto_predict import Predict
import pandas as pd
# ---------- Page Config ----------
st.set_page_config(
    page_title="Poem In → Meter Out",
    layout="wide"
)

st.title("Jiifto Metrical Scansion")

@st.cache_resource
def get_model():
    return Predict()

prs = Parser()
prd = get_model()

# ---------- Text Processing Function ----------
def process_text(text: str) -> str:
    """
    Replace this logic with anything:
    - AI call
    - API request
    - NLP processing
    - Database lookup
    """
    
    return text.upper()  # example: convert to uppercase

def parse_predict(lines):
    def parse_single_line(ln: str) -> dict:
        syll_list = prs.parse_line(ln)
        spc_list = prs.insert_spaces(ln, syll_list)
        return {"syllables": syll_list, "syllables_w_SP": spc_list}

    # Check if input is a list or a single string
    if isinstance(lines, str):
        lines = [lines]  # Convert to list if it's a single string
    
    # Parse all lines and collect results
    rows = [parse_single_line(ln) for ln in lines]
    
    # Create DataFrame from the collected rows
    df = pd.DataFrame(rows)
    
    # Pass the DataFrame to the prediction function
    y_pred = prd.predict_syll(df)

    if y_pred:
        df['pred_meter'] = y_pred
        df = df.drop(['word_start', 'word_end', 'syllables_w_SP'], axis=1)
        return df
    else:
        st.warning("nothing to output")
        return


# ---------- Layout ----------
col1, col2 = st.columns(2)

# ---------- Input Column ----------
with col1:
    st.subheader("Input")
    user_text = ""
    for punctuation in ',.!?;"-':
        user_text = user_text.replace(punctuation, " ")
    user_text = st.text_area(
        label="Enter your text",
        height=300,
        placeholder="Type something here..."
    )

    process_button = st.button("Process")

# ---------- Output Column ----------

with col2:
    st.subheader("Output")

    st.info("Processed text will appear here")

    if process_button and user_text.strip():
        output_df = parse_predict(user_text.split('\n'))
        if not output_df.empty:
            st.dataframe(output_df)
        else:
            st.warning("No results returned")
        # output_text = ""
        
    


    # st.text_area(
    #     label="Result",
    #     value=output_text,
    #     height=300,
    #     disabled=True
    # )
