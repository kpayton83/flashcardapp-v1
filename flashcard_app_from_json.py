
import streamlit as st
import json

# Load flashcards from external JSON
with open("flashcards.json", "r") as f:
    flashcards = json.load(f)

st.title("Liquefaction Study Flashcards")
mode = st.radio("Choose a mode", ["Flashcard Mode", "Quiz Mode"])

if 'index' not in st.session_state:
    st.session_state.index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def next_card():
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.session_state.show_answer = False

if mode == "Flashcard Mode":
    st.header("Flashcard Mode")
    st.write(f"**Q:** {flashcards[st.session_state.index]['question']}")
    
    if st.session_state.show_answer:
        st.success(f"**A:** {flashcards[st.session_state.index]['answer']}")
    if st.button("Show Answer" if not st.session_state.show_answer else "Hide Answer"):
        st.session_state.show_answer = not st.session_state.show_answer

    if st.button("Next Card"):
        next_card()

elif mode == "Quiz Mode":
    st.header("Quiz Mode")
    st.write(f"**Q:** {flashcards[st.session_state.index]['question']}")
    user_answer = st.text_input("Your Answer:")
    if st.button("Submit Answer"):
        if user_answer.lower() in flashcards[st.session_state.index]['answer'].lower():
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is:\n{flashcards[st.session_state.index]['answer']}")
    if st.button("Next Question"):
        next_card()
