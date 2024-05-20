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

# Main Streamlit app
def main():
    # Set the title of the Streamlit app
    st.title('AI Chat Box')

    # Create input fields for Conversation ID and Store ID
    conversation_id = st.text_input('Conversation ID:')
    store_id = st.text_input('Store ID:')

    # Create an "Enter" button
    if st.button('Enter'):
        if conversation_id and store_id:
            # Fetch conversation data from the API
            conversation_data = fetch_conversation_data(conversation_id, store_id)
            if conversation_data:
                # Filter conversation data
                user_messages, system_replies = filter_conversation(conversation_data)

                # Display user messages and system replies alternately
                st.header('Conversation:')
                for user_msg, sys_reply in zip(user_messages, system_replies):
                    st.write(f'User: {user_msg["message"]}')
                    st.write(f'System: {sys_reply["message"]}')
            else:
                st.error('Failed to fetch conversation data. Please check Conversation ID and Store ID.')

# Run the main Streamlit app
if __name__ == "__main__":
    main()
