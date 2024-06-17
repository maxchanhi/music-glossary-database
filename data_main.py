import streamlit as st
import pymongo
from st_keyup import st_keyup
from natural_lang_search import natural_search_main,youtube_search
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dictionary_quiz import term_quiz
st.set_page_config("Music Dictionary")
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["uri"], server_api=ServerApi('1'))

client = init_connection()
@st.cache_data(ttl=600)
def get_term_data(search):
    db = client['music_terms']
    collection = db['terms']
    if search:
        # Fetch terms that start with the search term
        items = collection.find({"Term": {"$regex": f"^{search.lower()}"}})
        meaning = collection.find({"Meaning": {"$regex": f"^{search.lower()}"}})
        simple_type = collection.find({"Type": {"$regex": f"^{search.lower()}"}})
        result=list(items)+list(meaning)+list(simple_type)
        return result
    return []

# Initialize session state variables
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
    db = client['music_terms']
    collection = db['terms']
natural_search_main()
st.title("Music Terms Dictionary")

search_word = st_keyup("Search a non-English term", key="2", debounce=500)

if search_word:
    st.session_state.search_term = get_term_data(search_word)

if st.session_state.search_term:
    for item in st.session_state.search_term:
        st.write(f"**Term:** {item['Term']}")
        st.write(f"**Meaning:** {item['Meaning']}")
        st.write(f"**Tag:** {item['Tag']}")
        st.write(f"**Grade:** {item['Grade']}")
        st.write(f"**Language:** {item['Language']}")
        if 'Similar Italian' in item:
            st.write(f"**Similar Italian:** {item['Similar Italian']}")
        if 'Similar French' in item:
            st.write(f"**Similar French:** {item['Similar French']}")
        if len(st.session_state.search_term)>1:
            st.write("---") 
    if len(st.session_state.search_term) == 1:
        term = st.session_state.search_term[0]
        search_count = term.get('Search Count', 0) + 1
        db = client['music_terms']
        collection = db['terms']
        collection.update_one(
            {"_id": term['_id']},
            {"$set": {"Search Count": search_count}}
        )
        st.write(f"This term has been searched {search_count} times.")
        youtube_search(term['term'])
elif not st.session_state.search_term:
    st.write("No results found.")
if 'question_list' not in st.session_state:
    st.session_state['question_list'] = []
with st.expander("Random quick quiz!",expanded=st.session_state['question_list']):
    term_quiz()
    


