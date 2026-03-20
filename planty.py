import json
import os
import streamlit as st
from groq import Groq
from utils import translate_text, load_config



def Planty(sarvam_client, language):

    try :
        config_data = load_config()
        GROQ_API_KEY = config_data.get("GROQ_API_KEY", "")

        # save the api key to environment variable
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY

        client = Groq ()

        # initialize the chat history as streamlit session state of not present already
        if "chat_history" not in st.session_state :
            st.session_state.chat_history = []

        # Set the Streamlit page title
        st.title ( translate_text(sarvam_client, "🪴 Planty AI", language) )

        # Add a "Clear Chat" button to clear chat history
        if st.button(translate_text(sarvam_client, "🗑️ Clear Chat", language)):
            st.session_state.chat_history = []

        # display chat history
        for message in st.session_state.chat_history :
            with st.chat_message ( message["role"] ) :
                st.markdown ( message["content"] )

        # input field for user's message:
        user_prompt = st.chat_input ( translate_text(sarvam_client, "Ask Planty...", language) )

        if user_prompt :
            st.chat_message ( "user" ).markdown ( user_prompt )
            st.session_state.chat_history.append ( {"role" : "user", "content" : user_prompt} )

            # sens user's message to the LLM and get a response
            messages = [
                {"role" : "system", "content" : "You are a helpful assistant"},
                *st.session_state.chat_history
            ]

            response = client.chat.completions.create (
                model="llama-3.3-70b-versatile",
                messages=messages
            )

            assistant_response = response.choices[0].message.content
            
            # Translate the assistant's standard English response to the preferred language
            translated_assistant_response = translate_text(sarvam_client, assistant_response, language)
            
            st.session_state.chat_history.append ( {"role" : "assistant", "content" : translated_assistant_response} )

            # display the Planty response
            with st.chat_message ( "assistant" ) :
                st.markdown ( translated_assistant_response )

    except Exception as e :
        st.error ( translate_text(sarvam_client, f"Please on your Mobile Data: {e}", language) )

# Run the contact function when the script is executed
if __name__ == "__main__":
    Planty(None, "English")