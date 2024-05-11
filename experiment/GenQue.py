from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-pro")

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=1,
                             google_api_key=os.getenv("GEMINI_KEY"))



RESPONSE_JSON = """
{
    "1" : "question",
    "2" : "question",
    "3" : "question",
    ...
}

"""



TEMPLATE = """
You are an expert question generator. we are conducting an exam on \
{subject} your job is to generate 15 question of type {typ} for that subject.  \
Make sure the questions are not repeated and check all the questions to be conforming the text as well. \
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make exatly {number} Questions \
### RESPONSE_JSON  \ 
{response_json} \

"""


gen_prompt = ChatPromptTemplate.from_template(TEMPLATE)
output_parser = StrOutputParser()
generation = gen_prompt | llm | output_parser



def generate(subject, typ, number):
    print("Generating...")
    quiz = generation.invoke({
    "subject" : subject,
    "typ" : typ,
    "number" : number,
    "response_json" : RESPONSE_JSON
    })

    # Regular expression pattern
    pattern = r'\{.*?\}'

    # Extracting substring
    substring = re.search(pattern, quiz, re.DOTALL)

    if substring:
        substring = substring.group()
        # print(substring)
    else:
        print("No response_json found.")

    return substring



if __name__ == '__main__':
    print("Gemini: ", generate("AI", "Open Question", 10))


