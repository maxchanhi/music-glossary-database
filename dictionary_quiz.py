import streamlit as st 
import random
from question import get_question,grades

def check_answer():
    st.session_state['check_ans'] = True
def term_quiz():
        
    if 'question_list' not in st.session_state:
        st.session_state['question_list'] = []
    if 'check_ans' not in st.session_state:
        st.session_state['check_ans'] = True
    if 'answer' not in st.session_state:
        st.session_state['answer'] = ""
        st.session_state['question'] = ""

    pick_meaning=None
    st.subheader("Term quiz")
    selected_grade=st.multiselect("Select the grade(s) you want to test on:",grades,default=grades)
    if st.session_state['question']:
        pick_ques= st.session_state['question']
        pick_meaning = st.radio(f"Choose the correct meaning of {pick_ques}?",st.session_state['question_list'],index=None)
    col1,col2=st.columns([4,1])
    with col1:
        if st.button("New Question",disabled= not st.session_state['check_ans']):
            pick_ques,meaning,option_list=get_question(selected_grade)
            st.session_state['question_list'] = option_list
            st.session_state['question']=pick_ques
            st.session_state['answer']=meaning
            st.session_state['check_ans']=False
            st.rerun()
    with col2:
        check_ans=st.button("Check Answer",on_click=check_answer,disabled=st.session_state['check_ans'] or pick_meaning is None)
        if check_ans:
            if st.session_state['answer'] == pick_meaning:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is: {st.session_state['answer']}")

if __name__ == "__main__":
    term_quiz()