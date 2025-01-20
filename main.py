import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "57802ca9-18f9-44ae-ac23-ce9229ed66f1"
FLOW_ID = "b214038b-1568-49d7-b2ab-6bc63d6f39d7"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "analysis" # The endpoint name of the flow

# Function to run the flow
def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Main function
def main():
    st.title("Social Media Performance Analysis")
    st.text("~By Cyber Creatures")
    name = st.text_input("What is your name?", placeholder="Enter your Name...")
    

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


    # Input field for the user
    message = st.text_area("", placeholder="How can we assist you today?")

    # Button to send the query
    if st.button("Analyze"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
                response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": message, "bot": response_text})

        except Exception as e:
            st.error(str(e))

    for chat in st.session_state["messages"]:
        st.markdown(f"**{name}:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.divider()  # Adds a divider for better readability
    # Display chat history
    st.subheader("Chat History")

if __name__ == "__main__":
    main()
