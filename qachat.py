from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Indian Healthcare Supply Chain Assistant",
    page_icon="🏥",
    layout="wide"
)

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# System prompt to specialize the chatbot
SYSTEM_PROMPT = """You are a specialized healthcare supply chain management assistant for the Indian healthcare system. 
Your primary functions include:
1. Analyzing state-wise population data for budget allocation
2. Providing insights on healthcare resource distribution
3. Suggesting optimal supply chain strategies
4. Monitoring healthcare inventory requirements
5. Recommending budget allocation based on population density and healthcare needs

Please provide detailed, data-driven responses focusing on:
- Population-based resource allocation
- State-wise budget distribution
- Supply chain optimization
- Healthcare infrastructure requirements
- Inventory management solutions
"""

chat = model.start_chat(history=[])
chat.send_message(SYSTEM_PROMPT)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# UI Elements
st.title("🏥 Indian Healthcare Supply Chain Management Assistant")
st.markdown("""
### Features:
- State-wise budget allocation recommendations
- Population-based resource distribution
- Supply chain optimization suggestions
- Healthcare infrastructure planning
""")

# Sidebar for state selection and population input
with st.sidebar:
    st.header("Quick Access")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Budget Allocation", "Supply Chain Optimization", "Infrastructure Planning", "Resource Distribution"]
    )
    
    st.subheader("State-wise Population Data")
    # Complete list of Indian states and Union Territories
    indian_states = [
        # States (28)
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
        # Union Territories (8)
        "Andaman and Nicobar Islands",
        "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi",
        "Jammu and Kashmir",
        "Ladakh",
        "Lakshadweep",
        "Puducherry"
    ]
    selected_state = st.selectbox("Select State/UT", indian_states)

def get_gemini_response(question):
    # Enhance the prompt with healthcare context
    enhanced_question = f"""Context: Indian Healthcare Supply Chain Management
State: {selected_state}
Analysis Type: {analysis_type}

Question: {question}

Please provide specific recommendations considering:
1. Population-based resource allocation
2. Geographic distribution
3. Healthcare infrastructure needs
4. Supply chain optimization
5. Budget allocation metrics"""
    
    response = chat.send_message(enhanced_question, stream=True)
    return response

# Main chat interface
st.header("💬 Chat Interface")
input_text = st.text_input("Ask your healthcare supply chain question:", key="input")
submit = st.button("Submit Question")

if submit and input_text:
    response = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))
    
    st.subheader("Response:")
    response_placeholder = st.empty()
    full_response = ""
    
    for chunk in response:
        full_response += chunk.text
        response_placeholder.markdown(full_response)
    
    st.session_state['chat_history'].append(("Assistant", full_response))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"**User:** {text}")
    else:
        st.markdown(f"**Assistant:** {text}")
    



    
