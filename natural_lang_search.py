from langchain_community.document_loaders import TextLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
import faiss
import streamlit as st
api_key = st.secrets["Mistral_key"]
def save_embeddings():
    # Load data
    loader = TextLoader("music_terms.txt")
    docs = loader.load()
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    # Define the embedding model
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)
    # Create the vector store
    vector = FAISS.from_documents(documents, embeddings)
    vector.save_local("terms_faiss_index_mis")

def load_embeddings(query):
    # Define the embedding model
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=st.secrets["Mistral_key"])
    # Load the vector store
    vector = FAISS.load_local("terms_faiss_index_mis", embeddings,allow_dangerous_deserialization=True)
    retriever = vector.as_retriever()
    model = ChatMistralAI(mistral_api_key=api_key)

    prompt = ChatPromptTemplate.from_template("""

    Answer questions about music terms based on the given context to the student:
    <context>
    {context}
    </context>
    Provide a short answer to the student's question.
    Avoid saying according to the text.
    Avoid answering questions not found in the database.
    Avoid answers that is not related to the question. If the user asks for German, only show German.
    Anwser "I don't know"  if you cannot find the answer.                                     
    List answer in point form.                                          
    Question: {input}""")

    # Create a retrieval chain to answer questions
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input":query})
    return response["answer"]

def natural_search_main():
    if "dicanswer" not in st.session_state:
        st.session_state.dicanswer = ""
    if "dic_login" not in st.session_state:
        st.session_state.dic_login = False
    if not st.session_state.dic_login:
        pw=st.text_input("Enter the password to enable AI chat:")
        if st.button("Login") and pw in st.secrets["app_password"]:
            st.session_state.dic_login = True

    if st.session_state.dic_login:
        with st.expander("Ask a question",expanded=True):
            user_input = st.text_input("Your question:", "")
            if st.button("Get Answer"):
                if user_input:
                    with st.spinner("Retrieving answer..."):
                        st.session_state.dicanswer = load_embeddings(user_input)
                        st.write("Answer:", st.session_state.dicanswer)
                else:
                    st.warning("Please enter a question.")
            st.markdown("""
**Disclaimer:** The AI-generated answers may not always be accurate. For precise information, please refer to the dictionary below or consult your teacher.
""")
from pytube import Search
def youtube_search(query):
    search_query = query + " music piece"
    search_results = Search(search_query).results

    if len(search_results) > 0:
        video = search_results[0]
        st.subheader(f"YouTube Video: [{video.title}]({video.watch_url})")            
        st.video(video.watch_url)
        st.write("Disclaimer: This video is searched based on the term you entered. The accuracy of the search results may vary.")
    else:
        st.write("No music pieces found on YouTube for this term.")
