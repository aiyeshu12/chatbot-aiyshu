import streamlit as st
import ollama
import base64

# Page setup
st.set_page_config(page_title="Mental Health Chatbot", layout="centered")

# Function to encode background image
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load background
try:
    bin_str = get_base64("backgrounda.jpg")
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
except FileNotFoundError:
    st.warning("Background image not found. Make sure 'backgrounda.jpg' exists.")

# Initialize session history
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

# Function to generate chatbot responses
def generate_response(user_input):
    st.session_state["conversation_history"].append({"role": "user", "content": user_input})
    response = ollama.chat(model="llama3.1:8b", messages=st.session_state["conversation_history"])
    
    ai_response = response["message"]["content"]
    st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
    return ai_response

# Function to generate positive affirmation
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# Function to generate guided meditation
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# App Title
st.title("🧘 Tranquil Mind support  Agent")

# Show past conversation
for msg in st.session_state["conversation_history"]:
    role = "You" if msg["role"] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# User input
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Buttons for extra features
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("🧘 Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
