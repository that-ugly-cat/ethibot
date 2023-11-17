import openai
from openai import OpenAI
import streamlit as st
client = OpenAI()
# Set OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Get list of topics
import ethibot_topics
topiclist = [key for key in ethibot_topics.topics]

# Create interface
st.title("💬 Talk to EthiBot") 
if "messages" not in st.session_state:
    with st.sidebar:
        topic = st.selectbox('What would you like to discuss about?', topiclist)
        persona = ethibot_topics.topics[topic]['persona']
        initial_message = ethibot_topics.topics[topic]['initial message']
        if st.button("Let's start!", type="primary"):
            st.session_state["messages"] = [{"role": "system", "content": persona}, {"role": "assistant", "content": initial_message}]
    
   
# Define hidden instructions
prompt_instruction = 'Reflect on the system role before answering. Try to behave as much as possible as the entity described in your system role. Check thoroughly your output against the system role.'


# Show messages

for msg in st.session_state.messages:
    if msg['role'] != 'system':
        st.chat_message(msg['role']).write(msg['content'])
    if msg['role'] == 'assistant':
        msg['content'] = msg['content'].replace(prompt_instruction, '')


# Logic
if prompt := st.chat_input():
    openai.api_key = openai_api_key
    prompt_send = prompt_instruction + ' ' + prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    
    msg_role = response.choices[0].message.role
    msg_content = response.choices[0].message.content

    msg = {'role' : msg_role, 'content' : msg_content}
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg_content)
