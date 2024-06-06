import pandas as pd
import streamlit as st
import requests
from streamlit_gsheets import GSheetsConnection
from st_keyup import st_keyup
spreadsheet_id = "https://docs.google.com/spreadsheets/d/1mIPxB3y2aEgp1tfp8-1pDqASj8F4iagtioOAwMuHsAs/edit#gid=0"  # Replace with your spreadsheet ID or URL
conn = GSheetsConnection(connection_name="my_gsheets_connection", spreadsheet_id=spreadsheet_id)
@st.cache_data(ttl=600)
def get_term_data(search):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="sheet1",
    ttl="10m",)
    if search:
        # Fetch terms that start with the search term
        items = df[df['Term'].str.lower().fillna('').str.startswith(search.lower())]
        meanings = df[df['Meaning'].str.lower().fillna('').str.startswith(search.lower())]
        simple_types = df[df['Type'].str.lower().fillna('').str.startswith(search.lower())] if 'Type' in df.columns else None
        result = pd.concat([items, meanings, simple_types]).drop_duplicates() if simple_types is not None else pd.concat([items, meanings]).drop_duplicates()
        return result
    return None

# Initialize session state variables
if "search_term" not in st.session_state:
    st.session_state.search_term = None

st.title("Music Terms Dictionary")

search_word = st_keyup("Search a non-English term", key="2", debounce=500)

if search_word:
    st.session_state.search_term = get_term_data(search_word)

if st.session_state.search_term is not None:
    for _, item in st.session_state.search_term.iterrows():
        st.write(f"**Term:** {item['Term']}")
        st.write(f"**Meaning:** {item['Meaning']}")
        st.write(f"**Tag:** {item['Tag']}")
        st.write(f"**Grade:** {item['Grade']}")
        st.write(f"**Language:** {item['Language']}")
        if 'Similar Italian' in item:
            st.write(f"**Similar Italian:** {item['Similar Italian']}")
        if 'Similar French' in item:
            st.write(f"**Similar French:** {item['Similar French']}")
        if len(st.session_state.search_term) > 1:
            st.write("---")
    if len(st.session_state.search_term) == 1:
        term = st.session_state.search_term.iloc[0]
        search_count = term.get('Search Count', 0) + 1
        df = conn.read()
        df.loc[df['Term'] == term['Term'], 'Search Count'] = search_count
        conn = GSheetsConnection()  # Re-authenticate the connection
        conn.write(df)
        st.write(f"This term has been searched {search_count} times.")

elif st.session_state.search_term is None:
    st.write("No results found.")
