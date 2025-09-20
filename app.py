import streamlit as st
import google.generativeai as genai
import os

# Set the title and icon of the Streamlit app page
st.set_page_config(page_title="Legal Document Simplifier", page_icon="⚖️")

# A conversational and informative header for the app
st.header("Legal Document Simplifier ⚖️")
st.markdown("Easily understand complex legal text by getting a simplified summary.")
st.markdown("---")

# ----------------------------------------------------
# STEP 1: Handle API Key securely.
# In a real-world app, you would use st.secrets.
# For this example, we'll ask the user to enter their API key.
# ----------------------------------------------------

# Get the Google AI API key from the user
api_key = st.text_input("Enter your Google AI API Key:", type="password", help="You can get your API key from Google AI Studio.")

# Initialize the Gemini model once the API key is available
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error configuring the API key: {e}")
        st.stop()
else:
    st.info("Please enter your Google AI API Key to proceed.")
    st.stop()


# ----------------------------------------------------
# STEP 2: Create the user interface for input.
# ----------------------------------------------------

user_input = st.text_area(
    "Paste your legal document here:",
    height=300,
    help="The chatbot will simplify and summarize the text you enter.",
)

# ----------------------------------------------------
# STEP 3: Define the core function to simplify the document.
# This logic is adapted from your Google Colab notebook.
# ----------------------------------------------------

def simplify_document(text):
    """
    Calls the Gemini model to simplify a legal document.
    """
    # The prompt from your notebook is a very good starting point for guiding the model.
    prompt = f"""
    You are a chatbot that simplifies legal documents. You should provide a concise, easy-to-understand summary of the following legal document without using technical legal jargon. The summary should be easy for a complete beginner to understand.

    Legal Document:
    {text}

    Simplified Summary:
    """
    
    try:
        # Use a spinner to show that the app is processing
        with st.spinner("Processing document... Please wait..."):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        st.error(f"An error occurred while simplifying the document: {e}")
        return None

# ----------------------------------------------------
# STEP 4: Trigger the simplification on button click.
# ----------------------------------------------------

if st.button("Simplify Document"):
    if user_input:
        simplified_output = simplify_document(user_input)
        if simplified_output:
            st.success("Here is the simplified legal document:")
            st.markdown(simplified_output)
    else:
        st.warning("Please paste a document to simplify.")

# Add a footer with a link to get an API key
st.markdown("---")
st.markdown("Need an API key? Get one for free at [Google AI Studio](https://aistudio.google.com/app/apikey).")