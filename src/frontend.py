import streamlit as st
from VectorStore import UfoSiteVectorStore
import os
os.environ["CUDA_VISIBLE_DEVICES"]=""

st.set_page_config(page_title="UFO Bot", page_icon=":robot_face:")
vector_store = UfoSiteVectorStore()

if "message_history" not in st.session_state:
    st.session_state.message_history = [{"role": "assistant", "content": "I am a UFOologist. Tell me about your UFO sighting."}]

left_col, main_col, right_col = st.columns([1,3,1])

with left_col:
    if st.button("Clear Chat"):
        st.session_state.message_history = []

    collection = st.radio("Collection", ["FAQs", "Aliens"])
    

with main_col:
    user_input = st.chat_input("Ask me anything about UFOs!")
    if user_input:
        if collection == "FAQs":
            related_questions = vector_store.query_faqs(user_input)
        else:
            related_questions = vector_store.query_aliens(user_input)
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.session_state.message_history.append({"role": "assistant", "content": related_questions})

    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]
        message_box = st.chat_message(this_message["role"])
        message_box.markdown(this_message["content"])


with right_col:
    st.text(st.session_state.message_history)    

