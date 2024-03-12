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
    sample_que = "Explain the concept of reinforcement learning and its use in \
        training artificial intelligence agents."
    sample_ans = """Reinforcement learning is a type of machine learning that allows an agent to learn how to behave in an environment by interacting with it and receiving rewards or punishments for its actions. The agent learns to associate certain actions with positive outcomes and other actions with negative outcomes, and it adjusts its behavior accordingly.

    Reinforcement learning is often used in training artificial intelligence agents, such as those used in video games or robotics. By allowing the agent to learn from its own experiences, reinforcement learning can help it to develop more effective strategies for achieving its goals.

    One of the key challenges in reinforcement learning is the exploration-exploitation tradeoff. The agent must balance the need to explore new actions and learn about the environment with the need to exploit its current knowledge to maximize its rewards. If the agent explores too much, it may never learn the optimal policy for the environment. If it exploits too much, it may miss out on opportunities to improve its policy.

    There are a number of different reinforcement learning algorithms that can be used to train agents. Some of the most common algorithms include:

    * **Q-learning:** Q-learning is a value-based reinforcement learning algorithm that estimates the value of each state-action pair. The agent then uses these values to select the action that is expected to maximize its long-term reward.
    * **SARSA:** SARSA is a variant of Q-learning that uses a different update rule. SARSA is often used in situations where the environment is partially observable.
    * **Policy gradients:** Policy gradient methods are a class of reinforcement learning algorithms that directly optimize the policy function. Policy gradient methods are often used in situations where the state space is large or continuous.

    Reinforcement learning is a powerful tool that can be used to train agents to solve a wide variety of problems. However, it is important to understand the challenges involved in reinforcement learning, such as the exploration-exploitation tradeoff, in order to use it effectively."""
    print("Grade: ", review_grade(sample_que, sample_ans))
