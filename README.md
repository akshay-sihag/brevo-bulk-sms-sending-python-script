# Bulk SMS Sender - Brevo API

A Streamlit application for sending bulk SMS messages using the Brevo (formerly Sendinblue) API.

## Features

- 📤 Upload contact lists from **Excel, CSV, or TXT** files
- 🎯 **Personalized SMS** with dynamic variables (e.g., `{name}`, `{username}`)
- 📱 Automatic phone number validation and formatting
- 🌍 **Multi-country support**: US/Canada (+1), India (+91), UK (+44), Australia, Singapore, UAE, Saudi Arabia
- 🚀 Bulk SMS sending with real-time progress tracking
- 📊 Live status updates for each SMS sent
- 👁️ **Message preview** showing personalized content
- 💾 Download detailed results as CSV
- ⚙️ Configurable sender name, message content, and tags
- 🔐 Secure API key management via Streamlit secrets

## Prerequisites

1. **Brevo Account**: Sign up at [Brevo](https://www.brevo.com/)
2. **API Key**: Get your API key from Brevo Dashboard → SMTP & API → API Keys
3. **Python 3.7+**: Make sure Python is installed on your system

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. **Configure API Key (Required):**

   The API key must be configured in Streamlit secrets for security. There is no manual input field.
   
   **For local development:**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit .streamlit/secrets.toml and add your API key
   # BREVO_API_KEY = "your-actual-api-key-here"
   ```
   
   **For Streamlit Cloud deployment:**
   - Go to your app settings in Streamlit Cloud
   - Click on "Secrets" in the left sidebar
   - Add: `BREVO_API_KEY = "your-actual-api-key-here"`
   - Click "Save"
   
   See `STREAMLIT_CLOUD_SETUP.md` for detailed instructions with screenshots.

## Usage

1. **Run the Streamlit app:**
```bash
streamlit run sms_sender.py
```

2. **Configure the app:**
   - API key will be automatically loaded from secrets ✅
   - **Select your country code** from the dropdown (e.g., 🇮🇳 India +91, 🇺🇸 US/Canada +1)
   - Set the **Sender Name** (max 11 characters) - This appears as the SMS sender
   - Optionally set **Organization Prefix** - Your brand name added before message (e.g., "AHC:")
   - Write your SMS message content
   - Optionally add a tag for tracking

3. **Upload contact list:**
   - **Excel File (.xlsx, .xls)**: Upload with columns for name and phone number
   - **CSV File**: Upload with columns for name and phone number
   - **TXT File**: Upload with one phone number per line (no personalization)

4. **Map your columns (for Excel/CSV):**
   - Select which column contains phone numbers
   - Select which column contains names (optional, for personalization)
   - Available variables will be shown (e.g., `{name}`, `{username}`, or any column name)

5. **Write your message with personalization:**
   - Example: `Hi {name}, your appointment is confirmed!`
   - Use any column from your file as a variable: `{columnname}`
   - Preview shows how the message will look for the first contact

6. **Phone Number Format:**
   
   The app automatically formats phone numbers based on the selected country:
   
   **For India (+91):**
   - 10 digits: `9876543210` → Converted to `919876543210`
   - 12 digits with code: `919876543210` → Kept as is
   
   **For US/Canada (+1):**
   - 10 digits: `1234567890` → Converted to `11234567890`
   - 11 digits with code: `11234567890` → Kept as is
   
   **For other countries:** Select from dropdown and use appropriate format
   - Numbers without country code will have it added automatically
   - Numbers with country code will be validated and kept as is

7. **Send SMS:**
   - Review the valid/invalid numbers count
   - Preview personalized message
   - Click "Send Personalized SMS to All"
   - Watch real-time progress with names and personalized content
   - Download detailed results as CSV when complete

## File Format Examples

📥 **Download Sample Templates:**
- `sample_contacts_template.xlsx` - Excel template
- `sample_contacts_template.csv` - CSV template

### Excel/CSV Format (with Personalization)
```csv
customer_name,phone_number,company
John Doe,1234567890,ABC Corp
Jane Smith,11234567891,XYZ Inc
Bob Johnson,9876543210,Tech Ltd
Alice Williams,15551234567,Global Solutions
```

**Example SMS Message (Using First Name):**
```
Hi {name}, thank you for choosing {company}! Your order is ready for pickup.
```

**Result for first contact:**
```
Hi John, thank you for choosing ABC Corp! Your order is ready for pickup.
```

**Example SMS Message (Using Full Name):**
```
Dear {customer_name}, your order from {company} is ready.
```

**Result for first contact:**
```
Dear John Doe, your order from ABC Corp is ready.
```

### CSV Format (Basic)
```csv
phone_number
1234567890
11234567891
9876543210
```

### TXT Format (No Personalization)
```
1234567890
11234567891
9876543210
```

## Features Explained

### Personalized Messaging
- **Dynamic variables**: Use `{columnname}` to insert data from your file
- **Smart name extraction**: `{name}` and `{username}` automatically use **first name only** from full names
  - Example: "John Doe" → `{name}` = "John"
  - Use `{full_column_name}` to get the complete name if needed
- **Any column**: Use any column from your Excel/CSV as a variable
- **Live preview**: See exactly how messages will look before sending

### Real-time Progress
- Live progress bar showing sending status
- Real-time table updates with each SMS sent
- Shows recipient names and message previews
- Status indicators (✅ Sent / ❌ Failed)

### Phone Number Validation
- Automatically removes non-digit characters
- Validates length (10 or 11 digits)
- Adds US country code (+1) when needed
- Shows invalid numbers before sending

### Results Tracking
- Recipient name and phone number
- Personalized message preview for each SMS
- Message ID for each successful SMS
- Error messages for failed SMS
- Timestamp for each message
- Downloadable CSV report with all details

## 📛 Sender Name & Organization Prefix

### Sender Name
The **Sender Name** field (max 11 characters) determines who the SMS appears to be from. This is your SMS sender ID.

### Organization Prefix (Recommended)
The **Organization Prefix** is a brand name that Brevo adds **before** your message content. This is especially recommended by U.S. carriers to ensure recipients recognize you.

**Example:**

**Configuration:**
- Sender Name: `AHC`
- Organization Prefix: `AHC`
- Message: `Hi {name}, your order is ready!`

**What recipient sees:**
```
From: AHC
Message: AHC: Hi John, your order is ready!
```

**Important:** Keep your total message length (prefix + message) under 160 characters to avoid splitting into multiple SMS.

**Why use Organization Prefix?**
- ✅ Better brand recognition
- ✅ Higher trust from recipients  
- ✅ Recommended by carriers
- ✅ Helps preserve sender name on some routes (like India)

---

## Testing with Your Phone Number

### For Indian Numbers (+91)

1. **Create a test CSV file** with your number:
```csv
customer_name,phone_number,company
Your Name,9876543210,Test Company
```
(Use your actual 10-digit Indian mobile number)

2. **In the app:**
   - Select **"🇮🇳 India (+91)"** from the country dropdown
   - Upload your test CSV file
   - Write a test message: `Hi {name}, this is a test from {company}!`
   - Review the preview
   - Send to test!

3. **Number format:** Indian numbers are 10 digits (without +91)
   - App will format `9876543210` → `919876543210` for Brevo API

### For Other Countries

Simply select your country from the dropdown and use the appropriate number format:
- 🇺🇸 US/Canada: 10 digits
- 🇬🇧 UK: 10 digits
- 🇦🇺 Australia: 9 digits
- 🇸🇬 Singapore: 8 digits
- 🇦🇪 UAE: 9 digits
- 🇸🇦 Saudi Arabia: 9 digits

A test file `test_india_contacts.csv` is included in the repository for reference.

## API Rate Limits

Be aware of Brevo's rate limits. The app includes a 0.5-second delay between messages to avoid hitting rate limits. You can adjust this in the code if needed.

## Troubleshooting

**Issue**: "Bad Request" error
- **Solution**: Check your API key is correct and active

**Issue**: SMS not sending
- **Solution**: Ensure sender name is max 11 characters and message content is provided

**Issue**: All numbers showing as invalid
- **Solution**: Check phone numbers are in correct format (10 or 11 digits)

## Security Notes

- **🔐 Secure by Design**: API key is loaded exclusively from Streamlit secrets
- **No visible input fields**: API key is never exposed in the UI
- **Never commit your API key** to version control
- The `secrets.toml` file is protected by `.gitignore`
- For Streamlit Cloud: Use the built-in Secrets management in app settings
- If secrets are not configured, the app will not run (shows error message)

## Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation and CSV handling
- `requests`: HTTP library for API calls

## Support

For issues with:
- **This app**: Check the code comments and error messages
- **Brevo API**: Visit [Brevo Developer Documentation](https://developers.brevo.com/docs)

## License

This project is open source and available for personal and commercial use.

