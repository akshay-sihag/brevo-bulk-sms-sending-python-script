# Streamlit Cloud Setup Guide

## How to Configure Secrets on Streamlit Cloud

Follow these steps to securely hide your API key and remove the input field from the sidebar:

### Step 1: Access Your App Settings
1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. Find your deployed app: `brevo-bulk-sms-sending-python-script`
3. Click on the **menu icon (⋮)** next to your app
4. Select **"Settings"**

### Step 2: Configure Secrets
1. In the settings page, look for **"Secrets"** in the left sidebar
2. Click on **"Secrets"**
3. You'll see a text editor

### Step 3: Add Your API Key
Copy and paste the following into the secrets editor (replace with your actual API key):

```toml
BREVO_API_KEY = "your-brevo-api-key-here"
```

**Note:** Replace `"your-brevo-api-key-here"` with your actual Brevo API key from your Brevo dashboard (SMTP & API → API Keys).

### Step 4: Save
1. Click the **"Save"** button
2. Your app will automatically restart
3. The API Key input field will disappear from the sidebar
4. You'll see **"🔐 API Key loaded from secrets"** instead

## Result

After configuration:
- ✅ API key is securely stored and encrypted
- ✅ Input field is hidden from sidebar
- ✅ No one can see your API key in the UI
- ✅ You don't need to enter it every time

## Troubleshooting

**Q: I still see the input field**
- Make sure you saved the secrets correctly
- Refresh your browser
- Check that the format is exactly as shown above

**Q: App shows error**
- Double-check the API key is correct
- Make sure there are no extra spaces or quotes
- The format should be: `BREVO_API_KEY = "your-key-here"`

**Q: How do I update the API key?**
- Go back to Settings → Secrets
- Edit the value
- Click Save
- App will restart automatically

