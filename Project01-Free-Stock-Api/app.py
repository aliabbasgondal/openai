from model import BotModel
import streamlit as st
from dotenv import load_dotenv
import os
import base64

load_dotenv()

st.title("Financial Chatbot")
st.subheader("Chat bot assist you on financial analysis of the different companies. \n*Disclaimer: only 5 years old data can be retrieved.")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"


if "bot" not in st.session_state:
    st.session_state["bot"] = BotModel()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state["bot"].delete_chat_history()
    elif st.button("Listen the Chat History"):
        if(len(st.session_state.bot.get_messages()) > 0):
            st.session_state.bot.listen_chat_history()
            if('urdu.mp3'):
                st.audio('urdu.mp3')
            else:
                st.error('Something went wrong')
        else:
            st.error("No chat history")
    elif st.columns(1):
        st.subheader('Translate the chat history')
        select_val = st.radio('Select Language:', ["Urdu", "Punjabi", "French", "German"], index=None)
        if select_val is not None and len(st.session_state.bot.get_messages()) > 0:
            response = st.session_state.bot.translation(select_val)
            st.markdown(response)
# Display chat messages
for message in st.session_state.bot.get_messages():
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("How can I help?"):

    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        #for response in st.session_state.bot.send_message({"role": "user", "content": prompt}):
        #    full_response += response.choices[0].delta.content or ""
        #    message_placeholder.markdown(response + "|")
       # message_placeholder.markdown(response)
        for message in st.session_state.bot.send_message({"role": "user", "content": prompt}):
            role_label = "User" if message.role == "user" else "Assistant"
            full_response += message.content[0].text.value
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.bot.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
st.session_state.bot.save_chat_history()


