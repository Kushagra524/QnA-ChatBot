# I will import all essential libraries

import os  # i used it to access env. variables
import streamlit as st  # to buildt webapp UI
import time   # i used it for time delay
from dotenv import load_dotenv   # to load API KEY from .env file
from langchain_groq import ChatGroq   # to connect Open source LLM models from GROQ
from langchain_core.output_parsers import StrOutputParser  # my model gets converted into string
from langchain_core.prompts import ChatPromptTemplate   # this is used to structure the prompt


# Now i will load my environment variables

load_dotenv()  # it wil read the .env file

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"]

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "QnA ChatBot using GROQ and LangChain"


# I will set Streamlit Page Configuration
# Why I put this here becoz streamlit requires config to be set at the top

st.set_page_config(
    page_title = "QnA ChatBot",
    page_icon = "🤖",
    layout = "wide"
)

# Now i will put my custom CSS
st.markdown("""<style>
            </style>""" , unsafe_allow_html = True)
# This line injects CSS into streamlit app , overrides default ui and defines : colors , animations and fonts

