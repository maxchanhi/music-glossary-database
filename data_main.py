import streamlit as st
import pymongo
from st_keyup import st_keyup
from natural_lang_search import natural_search_main

st.set_page_config("Music Dictionary")
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(f"mongodb+srv://max49363d93:{st.secrets['MONGODB_PASSWORD']}@<host>/?retryWrites=true&w=majority&appName=Music-terms")

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
st.title("Music Dictionary")

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

elif not st.session_state.search_term:
    st.write("No results found.")


