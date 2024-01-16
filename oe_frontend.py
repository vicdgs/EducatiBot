import streamlit as st

import oe_backend

st.title("EducatiBot")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_question = st.text_input("Fes-me una pregunta:", key="input_text")


if st.button('Enviar'):
    if user_question:
        st.session_state.chat_history.append(('user', user_question))

        respuesta = oe_backend.main_answer_gpt(user_question)

        st.session_state.chat_history.append(('bot', respuesta))

        st.experimental_rerun()


for role, text in st.session_state.chat_history:
    if role == 'user':
        st.markdown(f"<div style='text-align: right; color: blue;'>{text}</div>", unsafe_allow_html=True)
    else:  # bot
        st.markdown(f"<div style='text-align: left; color: green;'>{text}</div>", unsafe_allow_html=True)
