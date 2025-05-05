
# Liquefaction Flashcard App

An interactive flashcard and quiz app built with [Streamlit](https://streamlit.io) for reviewing technical knowledge related to CL2 system operations.

## 📁 Files

- `flashcard_app_from_json.py` – Main Streamlit app
- `flashcards.json` – File containing flashcards in Q&A format
- `flashcards_template_with_categories.json` – Optional: template to organize flashcards by category

## 🚀 How to Deploy with Streamlit Cloud

1. **Fork or Upload to GitHub**
   - Create a public GitHub repository
   - Upload both `flashcard_app_from_json.py` and `flashcards.json`

2. **Deploy on Streamlit Cloud**
   - Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click **“New app”**
   - Select your GitHub repo
   - Set the main file to: `flashcard_app_from_json.py`
   - Click **Deploy**

3. **Get a Shareable Link**
   - Streamlit will launch your app and give you a live URL to share

## ✏️ Editing Flashcards

To edit or add new flashcards:
- Open `flashcards.json` in your GitHub repo
- Click the pencil ✏️ icon to edit
- Save changes — the app will auto-refresh

### Sample JSON Format

```json
[
  {
    "category": "CL2 System",
    "question": "Where do the CL2 seal pots relieve?",
    "answer": "To the Emergency Vent Scrubber (EVS) at ±2.5\" water column."
  }
]
```

---

## 🧠 Modes Available

- **Flashcard Mode** – Flip through cards with answers
- **Quiz Mode** – Type your answer and get feedback

---

Built for training, studying, and operational readiness.
