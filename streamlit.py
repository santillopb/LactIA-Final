from threading import local
import streamlit as st;
import streamlit.components.v1 as components
from requests_toolbelt.multipart.encoder import MultipartEncoder;
import requests
import os;

# interact with FastAPI endpoint
#backend = 'http://localhost:8000/'
backend = os.environ["FAST_API_URL"]


def process(question: str, server_url: str):

    m = MultipartEncoder(
        fields={'question': question}
        )
    r = requests.post(server_url,
                      data=m,
                      params=m.fields,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)
    return r

# construct UI layout
st.title('LactIA Bot')

st.write('''ChatBot de lactancia con inteligencia artificial''')  # description and instructions

from PIL import Image
image = Image.open('pediatra.png')

st.image(image, width=100)

user_input_context = st.text_area("Hola soy Lactia Bot. ¿En qué te puedo ayudar?")

if st.button('Ver respuesta'):

    if user_input_context:
        result = process(user_input_context, backend)
        res = result.content
        #st.write(f'Respuesta:    {res.decode("utf-8") }')
        #components.html("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'><style>html{ background-color: #000000 }</style>"+"<div class='container-fluid bg-success bg-opacity-50'>"+f'Respuesta:    {res.decode("utf-8") }'+"</div>", height=600, scrolling=True)
        components.html("<style>#main-content { background-color: #B9F1C0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font }</style>"+"<div id='main-content'>"+f'Respuesta:    {res.decode("utf-8") }'+"</div>", height=600, scrolling=True)
        
        #href='./style.css'
    else:
        # handle case with no image
        st.write("Hazme una pregunta!")

