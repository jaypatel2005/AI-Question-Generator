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
                             temperature=0.7,
                             google_api_key=os.getenv("GEMINI_KEY"))



TEMPLATE = """
Hey, I need your help reviewing my answer for a question.
grade can be any floating point number

Here's the question: 
{que}

My answer: 
{ans}

Generate the response in the following format:
### Grade 
grade/10
"""


grade_prompt = ChatPromptTemplate.from_template(TEMPLATE)
output_parser = StrOutputParser()
grading = grade_prompt | llm | output_parser

def review_grade(que, ans):
    print("Reviewing...")
    grade = grading.invoke({
    "que" : que,
    "ans" : ans
    })

    pattern = r'\b\d+\b'

    match = re.search(pattern, grade)

    if match:
        # Extract the integer grade
        grade = int(match.group())
        # print("Grade:", grade)
    else:
        print("No grade found.")
    
    return grade


if __name__ == '__main__':
    sample_que = "Discuss the trends and advancements in database technology, including cloud-based databases and NoSQL databases."
    sample_ans = "I don't know"
    print("Grade: ", review_grade(sample_que, sample_ans))
