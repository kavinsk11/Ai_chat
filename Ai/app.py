import streamlit as st

# Set the title of the Streamlit app
st.title('AI Chat Box')

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
