
import streamlit as st
import json
import random
from collections import defaultdict
import os

# File path
FLASHCARD_FILE = "quiz_flashcards.json"

# Load flashcards
with open(FLASHCARD_FILE, "r") as f:
    flashcards = json.load(f)

# Session state setup
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'results' not in st.session_state:
    st.session_state.results = defaultdict(lambda: {'correct': 0, 'total': 0})
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("Liquefaction Quiz App")

sections = sorted(set(card["category"] for card in flashcards))
selected_section = st.selectbox("Choose a section to study:", sections)

# Filter cards by section
section_cards = [card for card in flashcards if card["category"] == selected_section]
total_questions = len(section_cards)

st.session_state.index = max(0, min(st.session_state.index, total_questions - 1))
current_card = section_cards[st.session_state.index]

st.subheader(f"Question {st.session_state.index + 1} of {total_questions}")
st.markdown(f"**Category:** {current_card['category']}")
st.markdown(f"**Q:** {current_card['question']}")

# Shuffle once
question_key = f"choices_{selected_section}_{st.session_state.index}"
if question_key not in st.session_state:
    st.session_state[question_key] = random.sample(current_card["choices"], len(current_card["choices"]))
choices = st.session_state[question_key]

user_choice = st.radio("Choose your answer:", choices)

if st.button("Submit Answer"):
    st.session_state.submitted = True
    st.session_state.results[current_card["category"]]["total"] += 1
    if user_choice == current_card["correct_answer"]:
        st.success("✅ Correct!")
        st.session_state.results[current_card["category"]]["correct"] += 1
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. Correct answer: {current_card['correct_answer']}")

if st.session_state.submitted:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.index = max(0, st.session_state.index - 1)
            st.session_state.submitted = False
    with col2:
        if st.button("Next"):
            st.session_state.index = min(total_questions - 1, st.session_state.index + 1)
            st.session_state.submitted = False

# Developer Mode
st.markdown("---")
if st.checkbox("🛠 Developer Mode: Add/Edit Flashcards"):
    st.subheader("Edit Existing Flashcards")
    for i, card in enumerate(section_cards):
        with st.expander(f"Edit Q{i+1}: {card['question'][:50]}..."):
            card["question"] = st.text_input(f"Question {i+1}", card["question"], key=f"q_{i}")
            card["correct_answer"] = st.text_input(f"Correct Answer {i+1}", card["correct_answer"], key=f"ca_{i}")
            card["choices"][0] = card["correct_answer"]
            for j in range(1, len(card["choices"])):
                card["choices"][j] = st.text_input(f"Distractor {j} for Q{i+1}", card["choices"][j], key=f"d_{i}_{j}")

    st.subheader("➕ Add New Flashcard")
    new_q = st.text_input("New Question")
    new_ca = st.text_input("Correct Answer")
    new_d1 = st.text_input("Distractor 1")
    new_d2 = st.text_input("Distractor 2")
    new_d3 = st.text_input("Distractor 3")

    if st.button("Add Flashcard"):
        flashcards.append({
            "category": selected_section,
            "question": new_q,
            "correct_answer": new_ca,
            "choices": random.sample([new_ca, new_d1, new_d2, new_d3], 4)
        })
        st.success("✅ New flashcard added. Please save below.")

    if st.button("💾 Save All Changes"):
        with open(FLASHCARD_FILE, "w") as f:
            json.dump(flashcards, f, indent=2)
        st.success("✅ All changes saved to file.")


# ----------------------------------------
# 🧪 TEST MODE
# ----------------------------------------
st.markdown("---")
if st.checkbox("🧪 Take 30-Question Random Test"):
    test_questions = random.sample(flashcards, 30)
    test_score = 0
    test_answers = []

    for i, card in enumerate(test_questions):
        st.subheader(f"Q{i + 1}: {card['question']}")
        qkey = f"test_q_{i}"
        selected = st.radio("Choose:", card["choices"], key=qkey)
        test_answers.append((selected, card["correct_answer"]))
        st.markdown("---")

    if st.button("Submit Test"):
        correct = sum(1 for selected, correct in test_answers if selected == correct)
        st.success(f"✅ You scored {correct}/30 ({(correct/30)*100:.1f}%)")
        for i, (selected, correct) in enumerate(test_answers):
            if selected != correct:
                st.error(f"❌ Q{i+1}: Your answer: '{selected}' — Correct: '{correct}'")

# ----------------------------------------
# ➡️ NEXT SECTION NAVIGATION
# ----------------------------------------
if st.session_state.submitted and st.session_state.index == total_questions - 1:
    current_index = sections.index(selected_section)
    if current_index < len(sections) - 1:
        if st.button("➡️ Move to Next Section"):
            new_section = sections[current_index + 1]
            st.session_state.index = 0
            st.experimental_set_query_params(section=new_section)

# ----------------------------------------
# 🔬 Animation Placeholder (Button version)
# ----------------------------------------
st.markdown("---")
if st.button("🎞️ Show NaCl Electrolysis Animation"):
    st.image("nacl_process_diagram.png", caption="Chlorine Production from Brine (Diagram)")
    st.image("nacl_animation.gif", caption="Electrolysis of NaCl Animation (Autoplaying GIF)")


