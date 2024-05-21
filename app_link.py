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
# Function to filter conversation data based on user and system messages
def filter_conversation(conversation_data):
    user_messages = []
    system_replies = []
    for conv in conversation_data['conversation']:
        if conv['type'] == 'user':
            user_messages.extend(conv['messages'])
        elif conv['type'] == 'system':
            for msg in conv['messages']:
                if 'message' in msg:
                    # Remove HTML tags from system message
                    clean_msg = re.sub(r'<[^>]*>', '', msg['message'])
                    system_replies.append({'message': clean_msg})
    return user_messages, system_replies


# Function to render system replies, including text, images, and links
def render_system_reply(reply):
    # Remove <p> tags from the reply
    reply = re.sub(r'<\/?p>', '', reply)
    
    # Find all images in the reply
    image_urls = re.findall(r'<img[^>]+src="([^">]+)"', reply)
    for url in image_urls:
        st.image(url)

    # Find all links in the reply
    links = re.findall(r'<a[^>]+href="([^">]+)"[^>]*>([^<]+)<\/a>', reply)
    for url, text in links:
        st.write(f'[**{text}**]({url})')

    # Remove images and links for the text part
    clean_reply = re.sub(r'<img[^>]+>', '', reply)
    clean_reply = re.sub(r'<a[^>]+href="[^">]+"[^>]*>([^<]+)<\/a>', r'\1', clean_reply)
    st.write(clean_reply)

# Main Streamlit app
def main():
    st.title('AI Chat Box')

    # Set the default Conversation ID and Store ID
    default_conversation_id = '907daf260552160e48f79d8d43fe675fb8461b113471367d40b7b497dfaf4b9a'
    default_store_id = 'ai-asst.myshopify.com'

    # Fetch conversation data based on default Conversation ID and Store ID
    conversation_data = fetch_conversation_data(default_conversation_id, default_store_id)
    if conversation_data:
        # Filter conversation data
        user_messages, system_replies = filter_conversation(conversation_data)

        # Display user messages and system replies alternately
        st.header('Conversation:')
        for user_msg, sys_reply in zip(user_messages, system_replies):
            st.write(f'**User**: {user_msg["message"]}')
            st.write(f'**System**: {sys_reply["message"]}')
    else:
        st.error('Failed to fetch conversation data. Please check Conversation ID and Store ID.')

# Run the main Streamlit app
if __name__ == "__main__":
    main()
