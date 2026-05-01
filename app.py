import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "QnA ChatBot with GROQ"


import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are an helpful assistant. Kindly respond to the queries smartly."),
        ("user" , "Question : {question}")
    ]
)


def generate_response(question , llm, temperature, max_tokens):
    llm = ChatGroq(
        model=llm,
        temperature=temperature,
        max_tokens=max_tokens
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Title of the app

st.title("Enhanced QnA ChatBot with GROQ")


# drop down menu to select models
llm = st.sidebar.selectbox("Select from the Folowing Open Source Groq Models : " , ["llama-3.1-8b-instant" , "llama-3.3-70b-versatile" , "meta-llama/llama-4-scout-17b-16e-instruct" , "meta-llama/llama-prompt-guard-2-22m" , "openai/gpt-oss-120b"])

# adjusting our resonse based on parameters like temp 7 max_tokens
temperature = st.sidebar.slider("Temperature" , min_value = 0.0 , max_value = 1.0 , value = 0.6)
max_tokens = st.sidebar.slider("Max tokens" , min_value = 50 , max_value = 600 , value = 250)




st.write("Heyy user , kindly ask your query.")
user_input = st.text_input("You : ")
if st.button("Throw an Answer."):
    if user_input:
        with st.spinner("Formulating a Response."):
            response = generate_response(user_input , llm , temperature , max_tokens)
            st.success(response)
    else:
        st.warning("Please enter a Query sir!")

