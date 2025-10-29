import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Bulk SMS Sender - Brevo",
    page_icon="📱",
    layout="wide"
)

# Title and description
st.title("📱 Bulk SMS Sender")
st.markdown("Send transactional SMS messages in bulk using Brevo API")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# API Key - Load from Streamlit secrets only
try:
    api_key = st.secrets["BREVO_API_KEY"]
    st.sidebar.success("🔐 API Key loaded securely")
except (FileNotFoundError, KeyError):
    st.sidebar.error("❌ API Key not found in secrets!")
    st.sidebar.warning("Please configure BREVO_API_KEY in Streamlit secrets to use this app.")
    st.stop()

# Sender name input
sender_name = st.sidebar.text_input(
    "Sender Name",
    max_chars=11,
    help="Max 11 characters for alphanumeric, 15 for numeric"
)

# SMS Content
st.sidebar.header("📝 Message Content")
sms_content = st.sidebar.text_area(
    "SMS Message",
    height=150,
    help="If more than 160 characters, will be sent as multiple messages"
)

# Character count
char_count = len(sms_content)
sms_count = (char_count // 160) + 1 if char_count > 0 else 0
st.sidebar.info(f"Characters: {char_count} | SMS Parts: {sms_count}")

# Optional parameters
st.sidebar.header("🔧 Optional Settings")
tag = st.sidebar.text_input("Tag (Optional)", help="Tag for tracking messages")
unicode_enabled = st.sidebar.checkbox("Unicode Enabled", value=True)

# Function to validate and format phone number
def format_phone_number(phone):
    """
    Format phone number based on length and country code.
    Returns formatted number with country code or None if invalid.
    """
    # Remove any non-digit characters
    phone = re.sub(r'\D', '', str(phone))
    
    # Check if it's 11 digits and starts with 1 (US/Canada)
    if len(phone) == 11 and phone.startswith('1'):
        return phone  # Keep as is: 1XXXXXXXXXX
    # Check if it's 10 digits (assume US/Canada, add +1)
    elif len(phone) == 10:
        return '1' + phone  # Add country code: 1XXXXXXXXXX
    else:
        return None  # Invalid format

# Function to send SMS via Brevo API
def send_sms(api_key, sender, recipient, content, sms_type="marketing", tag=None, unicode_enabled=True):
    """
    Send SMS using Brevo API
    Returns: (success: bool, message_id: str, error: str)
    """
    url = "https://api.brevo.com/v3/transactionalSMS/sms"
    
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": sender,
        "recipient": recipient,
        "content": content,
        "type": sms_type,
        "unicodeEnabled": unicode_enabled
    }
    
    if tag:
        payload["tag"] = tag
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            return True, data.get("messageId", "N/A"), None
        else:
            error_msg = response.json().get("message", response.text)
            return False, None, error_msg
    except Exception as e:
        return False, None, str(e)

# Main content area
st.header("📤 Upload Phone Numbers")

# File upload
uploaded_file = st.file_uploader(
    "Upload a CSV or TXT file with phone numbers",
    type=["csv", "txt"],
    help="CSV should have a column with phone numbers. TXT should have one number per line."
)

phone_numbers = []

if uploaded_file is not None:
    try:
        # Try to read as CSV first
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.write("**Preview of uploaded file:**")
            st.dataframe(df.head(), use_container_width=True)
            
            # Let user select the column with phone numbers
            phone_column = st.selectbox(
                "Select the column containing phone numbers:",
                options=df.columns.tolist()
            )
            
            if phone_column:
                phone_numbers = df[phone_column].tolist()
        else:
            # Read as text file (one number per line)
            content = uploaded_file.read().decode('utf-8')
            phone_numbers = [line.strip() for line in content.split('\n') if line.strip()]
            st.write(f"**Found {len(phone_numbers)} phone numbers in the file**")
            
        # Show sample of phone numbers
        if phone_numbers:
            st.write("**Sample phone numbers:**")
            st.write(phone_numbers[:5])
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Process and send SMS
if phone_numbers:
    st.header("🚀 Send SMS")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Numbers", len(phone_numbers))
    
    # Validate all numbers first
    formatted_numbers = []
    invalid_numbers = []
    
    for phone in phone_numbers:
        formatted = format_phone_number(phone)
        if formatted:
            formatted_numbers.append((phone, formatted))
        else:
            invalid_numbers.append(phone)
    
    with col2:
        st.metric("Valid Numbers", len(formatted_numbers))
    with col3:
        st.metric("Invalid Numbers", len(invalid_numbers))
    
    # Show invalid numbers if any
    if invalid_numbers:
        with st.expander("⚠️ Invalid Phone Numbers", expanded=False):
            st.write(invalid_numbers)
    
    # Validation before sending
    ready_to_send = True
    error_messages = []
    
    if not api_key:
        error_messages.append("⚠️ Please enter your Brevo API Key")
        ready_to_send = False
    
    if not sender_name:
        error_messages.append("⚠️ Please enter a Sender Name")
        ready_to_send = False
    
    if not sms_content:
        error_messages.append("⚠️ Please enter SMS message content")
        ready_to_send = False
    
    if len(formatted_numbers) == 0:
        error_messages.append("⚠️ No valid phone numbers to send to")
        ready_to_send = False
    
    # Display errors
    if error_messages:
        for msg in error_messages:
            st.error(msg)
    
    # Send button
    if st.button("📨 Send SMS to All Numbers", type="primary", disabled=not ready_to_send):
        st.header("📊 Sending Progress")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Results tracking
        results = []
        
        # Create a placeholder for real-time results
        results_placeholder = st.empty()
        
        # Send SMS to each number
        for idx, (original_number, formatted_number) in enumerate(formatted_numbers):
            status_text.text(f"Sending to {original_number} ({idx + 1}/{len(formatted_numbers)})...")
            
            success, message_id, error = send_sms(
                api_key=api_key,
                sender=sender_name,
                recipient=formatted_number,
                content=sms_content,
                sms_type="marketing",
                tag=tag,
                unicode_enabled=unicode_enabled
            )
            
            # Record result
            result = {
                "Original Number": original_number,
                "Formatted Number": formatted_number,
                "Status": "✅ Sent" if success else "❌ Failed",
                "Message ID": message_id if success else "N/A",
                "Error": error if error else "",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
            
            # Update progress
            progress = (idx + 1) / len(formatted_numbers)
            progress_bar.progress(progress)
            
            # Display real-time results
            results_df = pd.DataFrame(results)
            results_placeholder.dataframe(results_df, use_container_width=True)
            
            # Small delay to avoid rate limiting (adjust as needed)
            time.sleep(0.5)
        
        # Final status
        status_text.text("✅ All messages processed!")
        
        # Summary
        st.header("📈 Summary")
        success_count = sum(1 for r in results if "✅" in r["Status"])
        failed_count = len(results) - success_count
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sent", len(results))
        with col2:
            st.metric("Successful", success_count, delta=None)
        with col3:
            st.metric("Failed", failed_count, delta=None)
        
        # Download results
        st.header("💾 Download Results")
        results_df = pd.DataFrame(results)
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"sms_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with Streamlit | Powered by Brevo API</p>
    </div>
    """,
    unsafe_allow_html=True
)

