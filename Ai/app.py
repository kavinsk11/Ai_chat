import streamlit as st
import json

# Function to load conversation data from JSON
def load_conversation_data(json_data):
    conversation_data = json.loads(json_data)
    return conversation_data

# Function to filter conversation data based on user and system messages
def filter_conversation(conversation_data):
    user_messages = []
    system_replies = []
    for conv in conversation_data['conversation']:
        if conv['type'] == 'user':
            user_messages.extend(conv['messages'])
        elif conv['type'] == 'system':
            system_replies.extend(conv['messages'])
    return user_messages, system_replies

# Main Streamlit app
def main():
    # Set the title of the Streamlit app
    st.title('AI Chat Box')

    # Load the conversation data from JSON
    with open('conversation.json', 'r') as f:
        json_data = f.read()
    conversation_data = load_conversation_data(json_data)

    # Filter conversation data
    user_messages, system_replies = filter_conversation(conversation_data)

    # Display user messages and system replies separately
    st.header('User Messages:')
    for msg in user_messages:
        st.write(msg['message'])

    st.header('System Replies:')
    for reply in system_replies:
        st.write(reply['message'])

    # Create input fields for Conversation ID and Store ID
    conversation_id = st.text_input('Conversation ID:')
    store_id = st.text_input('Store ID:')

    # Create an "Enter" button
    if st.button('Enter'):
        if conversation_id and store_id:
            # Construct the URL for redirection
            chat_url = f'https://chateasy.logbase.io/api/conversation?id={conversation_id}&storeId={store_id}'
            # Use JavaScript to perform the redirection
            st.write(f'''
                <meta http-equiv="refresh" content="0; url={chat_url}">
                <a href="{chat_url}">Click here if you are not redirected.</a>
            ''', unsafe_allow_html=True)
        else:
            st.error('Please enter both Conversation ID and Store ID')

# Run the main Streamlit app
if __name__ == "__main__":
    main()
