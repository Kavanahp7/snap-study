import time
import streamlit as st
import smtplib
from email.mime.text import MIMEText

from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)


# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚",
    layout="centered",
)


# -----------------------------
# Secrets
# -----------------------------

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GMAIL_ADDRESS = st.secrets.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = st.secrets.get("GMAIL_APP_PASSWORD", "")

# Primary model
MODEL_NAME = "gemini-3.8-flash"


# -----------------------------
# Gemini client
# -----------------------------

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


if GEMINI_API_KEY:
    gemini_client = get_gemini_client()
else:
    gemini_client = None


# -----------------------------
# Gmail function
# -----------------------------

def send_email(to_address, subject, body):

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(message)


# -----------------------------
# Session state
# -----------------------------

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Onboarding
# -----------------------------

if not st.session_state.onboarded:

    st.title("📚 Snap & Study")

    st.subheader("Learn. Understand. Remember.")

    st.write(
        "Upload a question, diagram, textbook page, "
        "or handwritten notes and get a simple explanation."
    )

    name = st.text_input("Enter your name")

    email = st.text_input("Enter your Gmail address")

    if st.button("Start Studying"):

        if not name or not email:

            st.warning(
                "Please enter your name and Gmail address."
            )

        elif not GEMINI_API_KEY:

            st.error(
                "Gemini API key is not added yet."
            )

        else:

            st.session_state.name = name
            st.session_state.email = email

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            welcome_message = WELCOME_MESSAGE_TEMPLATE.format(
                name=name
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "kind": "text",
                    "content": welcome_message,
                }
            )

            st.session_state.onboarded = True

            st.rerun()


# -----------------------------
# Chat interface
# -----------------------------

else:

    st.title("📚 Snap & Study")

    st.caption(
        f"Study session for {st.session_state.name}"
    )


    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["kind"] == "text":

                st.write(message["content"])

            elif message["kind"] == "image":

                st.image(message["content"])


    # -----------------------------
    # Gemini function with retry
    # -----------------------------

    def ask_gemini(parts):

        max_attempts = 3

        for attempt in range(max_attempts):

            try:

                response = st.session_state.chat.send_message(
                    parts
                )

                return response.text

            except Exception as error:

                error_text = str(error)

                # Retry temporary server errors
                if "503" in error_text or "UNAVAILABLE" in error_text:

                    if attempt < max_attempts - 1:

                        time.sleep(3)

                        continue

                    return (
                        "Gemini is temporarily experiencing high demand. "
                        "Please wait a moment and try again."
                    )

                return (
                    f"Sorry, something went wrong: {error}"
                )


    # -----------------------------
    # Study input
    # -----------------------------

    user_input = st.chat_input(
        "Ask a question or upload a study image",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
    )


    if user_input:

        photo = (
            user_input["files"][0]
            if user_input["files"]
            else None
        )

        text = user_input["text"]

        parts = []


        # -----------------------------
        # Image input
        # -----------------------------

        if photo:

            image_bytes = photo.getvalue()

            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=photo.type,
            )

            parts.append(image_part)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "kind": "image",
                    "content": image_bytes,
                }
            )

            with st.chat_message("user"):

                st.image(image_bytes)


        # -----------------------------
        # Text input
        # -----------------------------

        if text:

            parts.append(text)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "kind": "text",
                    "content": text,
                }
            )

            with st.chat_message("user"):

                st.write(text)


        # -----------------------------
        # Image-only request
        # -----------------------------

        if photo and not text:

            parts.append(
                "Explain this study material in simple language. "
                "Identify the main topic, explain the important "
                "concepts, and give useful revision points."
            )


        # -----------------------------
        # Get Gemini response
        # -----------------------------

        if parts:

            answer = ask_gemini(parts)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "kind": "text",
                    "content": answer,
                }
            )

            with st.chat_message("assistant"):

                st.write(answer)


    # -----------------------------
    # Email summary
    # -----------------------------

    if st.session_state.messages:

        st.divider()

        if st.button("📧 Send Study Summary to Gmail"):

            if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:

                st.error(
                    "Gmail settings are not added yet."
                )

            else:

                conversation = []

                for message in st.session_state.messages:

                    if message["kind"] == "text":

                        role = message["role"].capitalize()

                        conversation.append(
                            f"{role}: {message['content']}"
                        )


                conversation_text = "\n\n".join(
                    conversation
                )


                try:

                    summary_response = (
                        st.session_state.chat.send_message(
                            SUMMARY_REQUEST_PROMPT
                        )
                    )

                    summary = summary_response.text

                except Exception:

                    summary = conversation_text


                email_body = (
                    f"Snap & Study - Study Summary\n\n"
                    f"Student: {st.session_state.name}\n\n"
                    f"{summary}"
                )


                try:

                    send_email(
                        st.session_state.email,
                        "Snap & Study - Study Summary",
                        email_body,
                    )

                    st.success(
                        "Study summary sent to your Gmail!"
                    )

                except Exception as error:

                    st.error(
                        f"Could not send the email: {error}"
                    )