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
st.title("💬 Talk to Sam") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": persona}, {"role": "assistant", "content": initial_message}]
    with st.sidebar:
        topic = st.selectbox('What would you like to discuss about?', topiclist)
      

# Define persona
with open('persona.txt') as f:
    persona = f.read()

# Define hidden instructions
prompt_instruction = 'Reflect on the system role before answering. Try to behave as much as possible as the person described in your system role.'

# Define initial message
initial_message = "Hi, I am Sam. I am a synthetic patient, based on the work of Giovanni Spitale, Gerold Schneider, Federico Germani, and Nikola Biller Andorno. Feel free to ask me about my experiece as a patient. Also, I speak English, Italian, German, and French."



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
