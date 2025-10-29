# Bulk SMS Sender - Brevo API

A Streamlit application for sending bulk SMS messages using the Brevo (formerly Sendinblue) API.

## Features

- 📤 Upload phone numbers from CSV or TXT files
- 📱 Automatic phone number validation and formatting
- 🚀 Bulk SMS sending with real-time progress tracking
- 📊 Live status updates for each SMS sent
- 💾 Download results as CSV
- ⚙️ Configurable sender name, message content, and tags
- ✅ Support for 10 and 11 digit phone numbers (US/Canada)

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

3. **Configure API Key (Recommended - More Secure):**

   **Option A: Using Streamlit Secrets (Recommended)**
   
   For local development:
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit .streamlit/secrets.toml and add your API key
   # BREVO_API_KEY = "your-actual-api-key-here"
   ```
   
   For Streamlit Cloud deployment:
   - Go to your app settings in Streamlit Cloud
   - Click on "Secrets" in the left sidebar
   - Add: `BREVO_API_KEY = "your-actual-api-key-here"`
   - Click "Save"
   
   **Option B: Manual Entry (Alternative)**
   
   You can also enter the API key manually in the app sidebar when you run it.

## Usage

1. **Run the Streamlit app:**
```bash
streamlit run sms_sender.py
```

2. **Configure the app:**
   - If using secrets: API key will be automatically loaded ✅
   - If not using secrets: Enter your Brevo API Key in the sidebar
   - Set the Sender Name (max 11 characters for alphanumeric)
   - Write your SMS message content
   - Optionally add a tag for tracking

3. **Upload phone numbers:**
   - **CSV File**: Upload a CSV file and select the column containing phone numbers
   - **TXT File**: Upload a text file with one phone number per line

4. **Phone Number Format:**
   - 10 digits: `1234567890` → Converted to `11234567890` (adds +1)
   - 11 digits starting with 1: `11234567890` → Kept as is
   - Other formats will be marked as invalid

5. **Send SMS:**
   - Review the valid/invalid numbers count
   - Click "Send SMS to All Numbers"
   - Watch real-time progress and results
   - Download results as CSV when complete

## File Format Examples

### CSV Format
```csv
phone_number,name
1234567890,John Doe
11234567891,Jane Smith
9876543210,Bob Johnson
```

### TXT Format
```
1234567890
11234567891
9876543210
```

## Features Explained

### Real-time Progress
- Live progress bar showing sending status
- Real-time table updates with each SMS sent
- Status indicators (✅ Sent / ❌ Failed)

### Phone Number Validation
- Automatically removes non-digit characters
- Validates length (10 or 11 digits)
- Adds US country code (+1) when needed
- Shows invalid numbers before sending

### Results Tracking
- Message ID for each successful SMS
- Error messages for failed SMS
- Timestamp for each message
- Downloadable CSV report

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

- **✅ Use Streamlit Secrets**: Store your API key in `.streamlit/secrets.toml` (automatically gitignored)
- **Never commit your API key** to version control
- The `secrets.toml` file is protected by `.gitignore`
- For Streamlit Cloud: Use the built-in Secrets management in app settings
- Manual entry option available as fallback (password field - hidden input)

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

