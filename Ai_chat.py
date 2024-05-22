import streamlit as st
import requests
import re

# Function to fetch conversation data from the API
def fetch_conversation_data(conversation_id, store_id):
    url = f'https://chateasy.logbase.io/api/conversation?id={conversation_id}&storeId={store_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to filter conversation data based on user and system messages
def filter_conversation(conversation_data):
    user_messages = []
    system_replies = []
    for conv in conversation_data['conversation']:
        if conv['type'] == 'user':
            user_messages.extend(conv['messages'])
        elif conv['type'] == 'system':
            for msg in conv['messages']:
                # Remove HTML tags from system message
                clean_msg = re.sub(r'<[^>]*>', '', msg['message'])
                system_replies.append({'message': clean_msg})
    return user_messages, system_replies

# Function to display conversation
def display_conversation(conversation_id, store_id):
    # Fetch conversation data from the API
    conversation_data = fetch_conversation_data(conversation_id, store_id)
    if conversation_data:
        # Filter conversation data
        user_messages, system_replies = filter_conversation(conversation_data)

        # Display user messages and system replies alternately
        st.header('Conversation:')
        st.subheader(f'Conversation ID: {conversation_id}')
        for user_msg, sys_reply in zip(user_messages, system_replies):
            st.write(f'**User**: {user_msg["message"]}')
            st.write(f'**System**: {sys_reply["message"]}')

        # Display unique URL
        unique_url = f'https://chateasy.logbase.io/api/conversation?id={conversation_id}&storeId={store_id}'
        st.write(f'[View JSON file here]({unique_url})')

        # Display message counters
        st.sidebar.write("Message Counters")
        st.sidebar.write(f"User Messages: {len(user_messages)}")
        st.sidebar.write(f"System Messages: {len(system_replies)}")
    else:
        st.error('Failed to fetch conversation data. Please check Conversation ID and Store ID.')

# Main Streamlit app
def main():
    st.title('AI Chat Box')

    # Sidebar for dark mode and navigation
    st.sidebar.title('Settings')
    dark_mode = st.sidebar.checkbox('Dark Mode', value=True)

    # Apply dark mode if selected
    if dark_mode:
        st.markdown("""
            <style>
            .main {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main {
                background-color: #ffffff;
                color: #000000;
            }
            </style>
        """, unsafe_allow_html=True)

    # Sidebar navigation
    page = st.sidebar.radio('Go to', ['Home', 'View Conversation'])

    if page == 'Home':
        st.subheader('Enter Conversation Details')
        # Create input fields for Conversation ID and Store ID
        conversation_id = st.text_input('Conversation ID:')
        store_id = st.text_input('Store ID:')

        # Create an "Enter" button
        if st.button('Enter'):
            if conversation_id and store_id:
                # Set the URL with query parameters
                st.experimental_set_query_params(conversation_id=conversation_id, store_id=store_id)
                st.experimental_rerun()

    elif page == 'View Conversation':
        # Get query parameters
        query_params = st.experimental_get_query_params()
        conversation_id = query_params.get('conversation_id', [None])[0]
        store_id = query_params.get('store_id', [None])[0]

        if conversation_id and store_id:
            # Display the conversation
            display_conversation(conversation_id, store_id)
        else:
            st.warning('No conversation ID and store ID provided. Please go to the Home page and enter the details.')

# Run the main Streamlit app
if __name__ == "__main__":
    main()
