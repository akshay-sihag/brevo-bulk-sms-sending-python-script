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
    help="Use variables like {name}, {username}, or any column name from your file. Example: 'Hi {name}, your order is ready!'"
)

# Character count (based on template)
char_count = len(sms_content)
sms_count = (char_count // 160) + 1 if char_count > 0 else 0
st.sidebar.info(f"Template Characters: {char_count} | Estimated SMS Parts: {sms_count}")
st.sidebar.markdown("💡 **Tip**: Use `{name}` or `{username}` for personalization")

# Optional parameters
st.sidebar.header("🔧 Optional Settings")

# Country code selector
country_options = {
    "🇺🇸 United States/Canada (+1)": {"code": "1", "length": 10},
    "🇮🇳 India (+91)": {"code": "91", "length": 10},
    "🇬🇧 United Kingdom (+44)": {"code": "44", "length": 10},
    "🇦🇺 Australia (+61)": {"code": "61", "length": 9},
    "🇸🇬 Singapore (+65)": {"code": "65", "length": 8},
    "🇦🇪 UAE (+971)": {"code": "971", "length": 9},
    "🇸🇦 Saudi Arabia (+966)": {"code": "966", "length": 9},
}

selected_country = st.sidebar.selectbox(
    "Select Country Code:",
    options=list(country_options.keys()),
    index=0,
    help="Choose the country code for your phone numbers"
)

country_code = country_options[selected_country]["code"]
expected_length = country_options[selected_country]["length"]

st.sidebar.info(f"📱 Expected format: {expected_length} digits (without country code)")

tag = st.sidebar.text_input("Tag (Optional)", help="Tag for tracking messages")
unicode_enabled = st.sidebar.checkbox("Unicode Enabled", value=True)

# Function to validate and format phone number
def format_phone_number(phone, country_code, expected_length):
    """
    Format phone number based on length and country code.
    Returns formatted number with country code or None if invalid.
    """
    # Remove any non-digit characters
    phone = re.sub(r'\D', '', str(phone))
    
    # Check if it already has the country code
    if phone.startswith(country_code) and len(phone) == len(country_code) + expected_length:
        return phone  # Already formatted correctly
    
    # Check if it's the expected length (without country code)
    elif len(phone) == expected_length:
        return country_code + phone  # Add country code
    
    # Check if it might be the full number with country code
    elif len(phone) == len(country_code) + expected_length:
        return phone  # Assume it's already complete
    
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

# Function to personalize message
def personalize_message(template, row_data):
    """
    Replace variables in template with actual values from row data.
    Variables format: {column_name}
    """
    message = template
    for key, value in row_data.items():
        placeholder = f"{{{key}}}"
        message = message.replace(placeholder, str(value))
    return message

# Main content area
st.header("📤 Upload Contact List")

# File upload
uploaded_file = st.file_uploader(
    "Upload a file with contact information",
    type=["csv", "xlsx", "xls", "txt"],
    help="Excel/CSV should have columns for name and phone number. TXT should have one number per line."
)

contacts_df = None
phone_numbers = []

if uploaded_file is not None:
    try:
        # Read file based on type
        if uploaded_file.name.endswith('.csv'):
            contacts_df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            contacts_df = pd.read_excel(uploaded_file)
        else:
            # Read as text file (one number per line)
            content = uploaded_file.read().decode('utf-8')
            phone_numbers = [line.strip() for line in content.split('\n') if line.strip()]
            st.write(f"**Found {len(phone_numbers)} phone numbers in the file**")
            st.write("**Sample phone numbers:**", phone_numbers[:5])
        
        # If we have a dataframe (CSV or Excel)
        if contacts_df is not None:
            st.write("**Preview of uploaded file:**")
            st.dataframe(contacts_df.head(), use_container_width=True)
            
            # Column mapping
            st.subheader("📋 Map Your Columns")
            col1, col2 = st.columns(2)
            
            with col1:
                phone_column = st.selectbox(
                    "Select Phone Number Column:",
                    options=contacts_df.columns.tolist(),
                    help="Column containing phone numbers"
                )
            
            with col2:
                name_column = st.selectbox(
                    "Select Name Column (Optional):",
                    options=["None"] + contacts_df.columns.tolist(),
                    help="Column containing names for personalization"
                )
            
            # Show available variables
            if name_column != "None":
                # Extract first name only (before the first space)
                contacts_df['name'] = contacts_df[name_column].apply(
                    lambda x: str(x).split()[0] if pd.notna(x) and str(x).strip() and ' ' in str(x) else str(x)
                )
                contacts_df['username'] = contacts_df['name']
                
                st.info(f"💡 Use `{{name}}` or `{{username}}` for first name only, `{{{name_column}}}` for full name")
            
            # Show all available variables
            available_vars = [f"{{{col}}}" for col in contacts_df.columns]
            st.markdown(f"**Available variables:** {', '.join(available_vars)}")
            
            # Show example of first name extraction
            if name_column != "None" and len(contacts_df) > 0:
                sample_full_name = contacts_df.iloc[0][name_column]
                sample_first_name = contacts_df.iloc[0]['name']
                st.caption(f"Example: Full name `{{{name_column}}}` = \"{sample_full_name}\" → First name `{{name}}` = \"{sample_first_name}\"")
            
            # Preview personalized message
            if sms_content and len(contacts_df) > 0:
                st.subheader("👁️ Message Preview")
                sample_row = contacts_df.iloc[0].to_dict()
                preview_message = personalize_message(sms_content, sample_row)
                st.text_area("Preview (first contact):", preview_message, height=100, disabled=True)
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Process and send SMS
# Determine if we're using dataframe (with personalization) or simple phone list
use_personalization = contacts_df is not None and phone_column is not None
data_available = use_personalization or len(phone_numbers) > 0

if data_available:
    st.header("🚀 Send SMS")
    
    # Prepare contact list
    contact_list = []
    
    if use_personalization:
        # Using dataframe with personalization
        for idx, row in contacts_df.iterrows():
            phone = row[phone_column]
            contact_list.append({
                'phone': phone,
                'data': row.to_dict()
            })
        total_contacts = len(contact_list)
    else:
        # Using simple phone number list
        for phone in phone_numbers:
            contact_list.append({
                'phone': phone,
                'data': {}
            })
        total_contacts = len(contact_list)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Contacts", total_contacts)
    
    # Validate all numbers first
    formatted_contacts = []
    invalid_numbers = []
    
    for contact in contact_list:
        phone = contact['phone']
        formatted = format_phone_number(phone, country_code, expected_length)
        if formatted:
            formatted_contacts.append({
                'original': phone,
                'formatted': formatted,
                'data': contact['data']
            })
        else:
            invalid_numbers.append(phone)
    
    with col2:
        st.metric("Valid Numbers", len(formatted_contacts))
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
        error_messages.append("⚠️ API Key not found")
        ready_to_send = False
    
    if not sender_name:
        error_messages.append("⚠️ Please enter a Sender Name")
        ready_to_send = False
    
    if not sms_content:
        error_messages.append("⚠️ Please enter SMS message content")
        ready_to_send = False
    
    if len(formatted_contacts) == 0:
        error_messages.append("⚠️ No valid phone numbers to send to")
        ready_to_send = False
    
    # Display errors
    if error_messages:
        for msg in error_messages:
            st.error(msg)
    
    # Send button
    send_label = "📨 Send Personalized SMS to All" if use_personalization else "📨 Send SMS to All Numbers"
    if st.button(send_label, type="primary", disabled=not ready_to_send):
        st.header("📊 Sending Progress")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Results tracking
        results = []
        
        # Create a placeholder for real-time results
        results_placeholder = st.empty()
        
        # Send SMS to each contact
        for idx, contact in enumerate(formatted_contacts):
            original_number = contact['original']
            formatted_number = contact['formatted']
            contact_data = contact['data']
            
            # Personalize message if data available
            if use_personalization and contact_data:
                personalized_content = personalize_message(sms_content, contact_data)
                # Use first name for display if available
                if name_column != "None" and 'name' in contact_data:
                    display_name = contact_data['name']  # This is the first name
                else:
                    display_name = contact_data.get(name_column, original_number) if name_column != "None" else original_number
            else:
                personalized_content = sms_content
                display_name = original_number
            
            status_text.text(f"Sending to {display_name} ({idx + 1}/{len(formatted_contacts)})...")
            
            success, message_id, error = send_sms(
                api_key=api_key,
                sender=sender_name,
                recipient=formatted_number,
                content=personalized_content,
                sms_type="marketing",
                tag=tag,
                unicode_enabled=unicode_enabled
            )
            
            # Record result
            result = {
                "Name": display_name if use_personalization else "N/A",
                "Original Number": original_number,
                "Formatted Number": formatted_number,
                "Message Preview": personalized_content[:50] + "..." if len(personalized_content) > 50 else personalized_content,
                "Status": "✅ Sent" if success else "❌ Failed",
                "Message ID": message_id if success else "N/A",
                "Error": error if error else "",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
            
            # Update progress
            progress = (idx + 1) / len(formatted_contacts)
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

