import streamlit as st
from GenQue import generate
import pandas as pd
import json

def main():
    st.title("Exam Question Generator")

    # Add a text input for the user to input the subject
    subject = st.text_input("Enter the subject:")

    # Add a selectbox for the user to choose the type of questions
    question_types = ["Open Question", "Close Question", "Indirect Question"]  # Add more types as needed
    selected_type = st.selectbox("Select the type of questions:", question_types)

    # Add a slider to select the number of questions to generate
    num_questions = st.slider("Number of questions to generate:", min_value=1, max_value=10, value=5)

    # Add a button to trigger question generation
    if st.button("Generate Questions"):
        # Call your question generation function with the subject, type of questions, and number of questions
        questions = generate(subject, selected_type, num_questions)
        questions_dict = json.loads(questions)

        # df = pd.DataFrame(columns=["Question", "Answer"])

        questions_with_answers = []

        # Display the generated questions
        st.header("Generated Questions:")
        for i, (key, value) in enumerate(questions_dict.items()):
            if i < num_questions:
                st.subheader(f"Question {i+1}:")
                st.markdown(f"<p style='font-size: 18px;'>{value}</p>", unsafe_allow_html=True)
                answer_id = f"answer_{i}"
                st.markdown(f'<textarea id="{answer_id}" name="{answer_id}" rows="10" cols="80"></textarea>', unsafe_allow_html=True)
                questions_with_answers.append({"Question": value, "Answer": ""})

        df = pd.DataFrame(questions_with_answers)
        
        if st.button("Submit"):
            for i, row in enumerate(df.iterrows()):
                if i < num_questions:
                    question = row[1]["Question"]
                    answer = st.markdown(f'<script>document.getElementById("answer_{i}").value</script>', unsafe_allow_html=True)
                    df.at[i, "Answer"] = answer
            df.to_csv("questions_with_answers.csv", index=False)
            st.success("Questions and answers saved to questions_with_answers.csv")

if __name__ == "__main__":
    main()