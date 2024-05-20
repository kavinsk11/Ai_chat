import streamlit as st
import webbrowser

# Set the title of the Streamlit app
st.title('AI Chat Box')

# Create input fields for Conversation ID and Store ID
conversation_id = st.text_input('Conversation ID:')
store_id = st.text_input('Store ID:')

# Create an "Enter" button
if st.button('Enter'):
    if conversation_id and store_id:
        # Construct the URL for redirection
        chat_url = f'/chat?conversationId={conversation_id}&storeId={store_id}'
        # Display the constructed URL
        st.write(f'Redirecting to {chat_url}...')
        # Uncomment the following line to open the URL in a new browser tab
        # webbrowser.open(chat_url)
    else:
        st.error('Please enter both Conversation ID and Store ID')
