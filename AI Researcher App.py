import streamlit as st
import requests

# Streamlit App
st.title("AI Research Assistant")

# Form for User Input
with st.form(key='input_form'):
    company_name = st.text_input("Company Name:")
    company_website = st.text_input("Company Website:")
    submit_button = st.form_submit_button(label='Run Research Analysis')

# Function to send data to Make webhook
def send_to_make_webhook(company_name, company_website):
    webhook_url = "https://hook.us2.make.com/oucy3dhjndwdxr4em8qsi3i5lsd6x44b"  # Replace with your Make webhook URL
    payload = {
        "company_name": company_name,
        "company_website": company_website
    }
    try:
        # Send POST request to the webhook
        response = requests.post(webhook_url, json=payload)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Check if the response is empty
        if not response.text:
            st.error("Received an empty response from the webhook.")
            return None

        # Attempt to parse JSON response
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None
    except ValueError:
        st.error("Received invalid JSON response from the webhook.")
        return None

# When form is submitted
if submit_button:
    if company_name and company_website:
        st.write("Running analysis for:", company_name)
        response = send_to_make_webhook(company_name, company_website)
        
        if response:
            # Display the analysis results
            st.write("Analysis results are displayed below.")
            result_placeholder = st.empty()  # Placeholder for results
            result_placeholder.write(response)
        else:
            st.warning("Failed to get a valid response from the webhook.")
    else:
        st.warning("Please enter both Company Name and Website.")
