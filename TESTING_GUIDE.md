# Testing Guide - How to Test the App with Your Phone Number

## 🇮🇳 Testing with Indian Numbers

### Step 1: Create Your Test File

Create a simple CSV file with your phone number. You can use Excel or any text editor:

**Option A: Using Excel**
1. Open Excel
2. Create columns: `customer_name`, `phone_number`, `company`
3. Add your data:
   ```
   customer_name    phone_number    company
   Your Name        9876543210      Test Co
   ```
4. Save as `my_test.csv`

**Option B: Using Text Editor**
Create a file called `my_test.csv` with this content:
```csv
customer_name,phone_number,company
Akshay,9876543210,AHC
```

**Important:** 
- Use your actual 10-digit Indian mobile number (without +91)
- Don't include spaces or special characters in the phone number

### Step 2: Configure the App

1. **Run the app:**
   ```bash
   streamlit run sms_sender.py
   ```

2. **In the sidebar:**
   - ✅ API Key will be loaded automatically (if configured in secrets)
   - 📱 **Select "🇮🇳 India (+91)"** from the country dropdown
   - 📝 Enter Sender Name (e.g., "AHC" or "Test")
   - ✏️ Write your test message:
     ```
     Hi {name}, this is a test SMS from {company}! If you receive this, the app works perfectly!
     ```

### Step 3: Upload and Preview

1. **Upload your CSV file** (`my_test.csv`)
2. **Map columns:**
   - Select `phone_number` as Phone Number Column
   - Select `customer_name` as Name Column
3. **Check the preview:**
   - It should show: `Hi Akshay, this is a test SMS from AHC! If you receive this, the app works perfectly!`
   - Your number should show as valid (not invalid)

### Step 4: Send Test SMS

1. Click **"📨 Send Personalized SMS to All"**
2. Watch the real-time progress
3. Check your phone for the SMS!

**Expected Result:**
- Status: ✅ Sent
- You should receive the SMS on your phone within seconds
- Message ID will be shown in the results

### Step 5: Verify

After sending, check:
- ✅ Your phone received the SMS
- ✅ Message is personalized with your name
- ✅ No errors in the results table
- ✅ Download the CSV results for record

---

## 🇺🇸 Testing with US/Canada Numbers

Same process, but:
- Select **"🇺🇸 United States/Canada (+1)"** 
- Use 10-digit US number: `1234567890`
- App will format it as: `11234567890`

---

## 🌍 Testing with Other Countries

### UK (+44)
```csv
customer_name,phone_number
John Smith,7911123456
```
10 digits, formatted as: `447911123456`

### Australia (+61)
```csv
customer_name,phone_number
Sarah Jones,412345678
```
9 digits, formatted as: `61412345678`

### Singapore (+65)
```csv
customer_name,phone_number
Wei Lin,91234567
```
8 digits, formatted as: `6591234567`

### UAE (+971)
```csv
customer_name,phone_number
Ahmed Ali,501234567
```
9 digits, formatted as: `971501234567`

---

## 💡 Quick Test Template

Copy this and modify with your details:

```csv
customer_name,phone_number,company
YOUR_NAME,YOUR_10_DIGIT_NUMBER,Test Company
```

**Test Message:**
```
Hi {name}, testing SMS from {company}! Reply OK if received.
```

---

## ⚠️ Troubleshooting

### "Invalid Phone Number"
- ✅ Check you selected the correct country
- ✅ Verify number length (10 digits for India)
- ✅ Remove any spaces, dashes, or special characters
- ✅ Don't include +91 or country code in the CSV

### "Bad Request" or API Error
- ✅ Check your Brevo API key is correct
- ✅ Verify your Brevo account is active
- ✅ Check you have SMS credits in Brevo
- ✅ Sender name should be max 11 characters

### SMS Not Received
- ✅ Check if status shows "✅ Sent" (not "❌ Failed")
- ✅ Wait 1-2 minutes (sometimes delayed)
- ✅ Check your phone's SMS/message app
- ✅ Check if number is correct in the results CSV
- ✅ Verify the formatted number starts with 91 (for India)

### Preview Not Showing
- ✅ Make sure you've uploaded the file
- ✅ Selected the correct columns
- ✅ Written a message with variables like `{name}`

---

## 📊 Sample Test File Included

The repository includes `test_india_contacts.csv` with sample Indian numbers. You can:
1. Download it
2. Replace the numbers with yours
3. Upload and test

**File contains:**
```csv
customer_name,phone_number,company
Akshay Sihag,9876543210,Tech Solutions
Priya Sharma,8765432109,Digital India
Rahul Kumar,7654321098,Smart Systems
```

---

## 🎯 Best Practices for Testing

1. **Start Small**: Test with just 1-2 numbers first
2. **Use Your Own Number**: Test with your phone before sending to clients
3. **Check Preview**: Always verify the message preview looks correct
4. **Monitor Results**: Watch the real-time results table
5. **Save Results**: Download the CSV results for records
6. **Test Variables**: Make sure `{name}` and other variables are replaced correctly

---

## ✅ Success Checklist

Before sending to real customers:

- [ ] Tested with your own phone number
- [ ] Received the test SMS successfully
- [ ] Message personalization works (`{name}` shows actual name)
- [ ] Phone numbers formatted correctly (starts with country code)
- [ ] No errors in the results
- [ ] Message content is appropriate
- [ ] Sender name is recognizable (max 11 chars)
- [ ] All variables in message are replaced (no `{` `}` in final SMS)

---

## 🚀 Ready to Send!

Once you've successfully tested:
1. Prepare your full contact list
2. Double-check all phone numbers
3. Review your message one more time
4. Upload and send!

**Need Help?** Check the main README.md or PERSONALIZATION_GUIDE.md for more details.

