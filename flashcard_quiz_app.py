
import streamlit as st
import json
import random
from collections import defaultdict

# Load flashcards
with open("quiz_flashcards.json", "r") as f:
    flashcards = json.load(f)

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'results' not in st.session_state:
    st.session_state.results = defaultdict(lambda: {'correct': 0, 'total': 0})
if 'finished' not in st.session_state:
    st.session_state.finished = False

# Set up layout
st.title("Liquefaction Quiz App")

# Shuffle and categorize flashcards by section
sections = sorted(set(card["category"] for card in flashcards))
selected_section = st.selectbox("Choose a section to study:", sections)

# Filter cards by selected section
section_cards = [card for card in flashcards if card["category"] == selected_section]

if not section_cards:
    st.warning("No questions found for this section.")
    st.stop()

current_card = section_cards[st.session_state.index]

st.subheader(f"Question {st.session_state.index + 1} of {len(section_cards)}")
st.markdown(f"**Category:** {current_card['category']}")
st.markdown(f"**Q:** {current_card['question']}")

# Shuffle answers
choices = current_card["choices"]
random.shuffle(choices)
user_choice = st.radio("Choose your answer:", choices)

if st.button("Submit Answer"):
    st.session_state.results[current_card["category"]]["total"] += 1
    if user_choice == current_card["correct_answer"]:
        st.success("✅ Correct!")
        st.session_state.results[current_card["category"]]["correct"] += 1
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. Correct answer: {current_card['correct_answer']}")

    if st.session_state.index + 1 >= len(section_cards):
        st.session_state.finished = True
    else:
        st.session_state.index += 1

if st.session_state.finished:
    st.subheader("🎯 Quiz Complete!")
    st.markdown(f"**Total Score:** {st.session_state.score} / {len(section_cards)}")
    st.markdown("---")
    st.markdown("### 📊 Section Performance")
    for section, result in st.session_state.results.items():
        total = result['total']
        correct = result['correct']
        percent = (correct / total) * 100 if total else 0
        st.markdown(f"**{section}**: {correct}/{total} correct ({percent:.1f}%)")
    st.button("Restart Quiz", on_click=lambda: st.session_state.clear())

