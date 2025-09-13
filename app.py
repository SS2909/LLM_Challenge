import streamlit as st
import requests
import io

API_BASE = st.secrets.get('API_BASE', 'http://localhost:8000')

st.set_page_config(page_title='RAG Chat', layout='centered')

if 'token' not in st.session_state:
    st.session_state.token = None

def login():
    st.title('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        data = {'username': email, 'password': password}
        r = requests.post(f'{API_BASE}/login', data=data)
        if r.ok:
            st.session_state.token = r.json()['access_token']
            st.experimental_rerun()
        else:
            st.error('Login failed: ' + r.text)

def register():
    st.title('Register')
    email = st.text_input('Email', key='reg_email')
    password = st.text_input('Password', type='password', key='reg_pass')
    if st.button('Register'):
        r = requests.post(f'{API_BASE}/register', json={'email':email, 'password':password})
        if r.ok:
            st.success('Registered — now login')
        else:
            st.error('Register failed: ' + r.text)

if not st.session_state.token:
    mode = st.radio('Mode', ['Login','Register'])
    if mode == 'Login':
        login()
    else:
        register()
    st.stop()

headers = {'Authorization': f'Bearer {st.session_state.token}'}
st.title('RAG Chat')

with st.sidebar:
    st.header('Upload Document')
    uploaded = st.file_uploader('Upload PDF/TXT/DOCX', type=['pdf','txt','docx'])
    if uploaded:
        files = {'file': (uploaded.name, uploaded.getvalue())}
        r = requests.post(f'{API_BASE}/upload', files=files)
        if r.ok:
            st.success('File uploaded & ingested')
        else:
            st.error('Upload failed: ' + r.text)

if 'history' not in st.session_state:
    st.session_state.history = []

prompt = st.text_input('Ask anything about uploaded docs', key='prompt')
if st.button('Send') and prompt.strip():
    r = requests.post(f'{API_BASE}/chat', json={'message': prompt})
    if r.ok:
        answer = r.json()['answer']
        st.session_state.history.append(('user', prompt))
        st.session_state.history.append(('assistant', answer))
    else:
        st.error('Chat failed: ' + r.text)

for role, text in st.session_state.history[::-1]:
    if role == 'assistant':
        st.markdown(f'**Assistant:** {text}')
    else:
        st.markdown(f'**You:** {text}')
