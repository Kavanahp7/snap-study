# 📚 Snap & Study

## Project Overview:

**Snap & Study** is an AI-powered study assistant designed to help students understand study material in a simple and interactive way.

The application allows students to **ask study-related questions or upload images** such as textbook pages, diagrams, questions, and handwritten notes. Using the **Google Gemini API**, Snap & Study analyzes the provided content and generates clear explanations along with important concepts and revision points.

The application also provides a **Gmail integration** that allows students to send their study summary directly to their email for later revision.

## Project Objective:

The main objective of Snap & Study is to make studying easier by combining **AI-powered explanations, image understanding, and study summaries** in one simple application.

It is especially useful when students need help understanding content from images, diagrams, handwritten notes, or textbook pages.

## Key Features:

**AI Study Assistant:** Students can ask study-related questions and receive simple explanations.

**Image-Based Learning:** Students can upload images of questions, textbook pages, diagrams, or handwritten notes.

**Concept Explanation:** Gemini AI analyzes the provided content and explains the topic in student-friendly language.

**Revision Points:** Important concepts and key points are provided for quick revision.

**Interactive Chat:** Students can continue the conversation and ask follow-up questions.

**Gmail Study Summary:** Students can send their study summary to their Gmail address.

## Technology Used:

**Programming Language:** Python

**Frontend & Application Framework:** Streamlit

**AI Technology:** Google Gemini API

**AI Model:** Gemini Flash Lite

**Email Service:** Gmail SMTP

**Version Control:** Git & GitHub

**Deployment:** Streamlit Community Cloud

## How the Application Works:

1. The student enters their name and Gmail address.
2. The student starts a study session.
3. The student can type a question or upload a study-related image.
4. The application sends the provided content to Google Gemini.
5. Gemini analyzes the content and generates a simple explanation.
6. The response includes important concepts and revision points when appropriate.
7. The student can continue asking questions during the study session.
8. The student can send the study summary to their Gmail.

## Project Structure:

```text
snap-study/
│
├── .streamlit/
│   └── secrets.toml.example
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
└── .gitignore
```

## File / Folder Purpose:

**`app.py`:** Main application file containing the Streamlit interface, Gemini AI integration, image upload and processing, chat functionality, and Gmail summary feature.

**`prompts.py`:** Contains the system prompt, welcome message, and study-summary prompt used by the application.

**`requirements.txt`:** Contains the Python packages required to run the application.

**`.streamlit/secrets.toml.example`:** Provides the required secret names for configuring the Gemini API and Gmail credentials without exposing actual credentials.

**`.gitignore`:** Prevents sensitive files, virtual environments, and unnecessary files from being uploaded to GitHub.

**`README.md`:** Contains project information, setup details, technologies, and documentation.

## Security:

API keys and Gmail credentials are stored using **Streamlit secrets** and are not included in the public GitHub repository.

## Future Scope:

* Voice-based study assistance
* Automatic quiz and flashcard generation
* Personalized learning recommendations
* Study progress tracking
* Multi-language learning support



## Conclusion:

Snap & Study demonstrates how **Generative AI can be integrated into an interactive educational application** to help students understand study material more effectively. By combining text questions, image understanding, conversational learning, and Gmail-based study summaries, the project provides a simple and practical AI-assisted learning experience.
