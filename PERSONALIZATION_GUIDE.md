# SMS Personalization Guide

## 🎯 How to Send Personalized SMS Messages

This guide explains how to use dynamic variables to personalize your SMS messages for each recipient.

## Quick Start

### Step 1: Prepare Your Contact File

Create an Excel or CSV file with your contacts. Include columns for:
- **Phone Number** (required)
- **Name** (for personalization)
- Any other data you want to include in messages

**Example Excel/CSV:**
```
name          | phone_number | company        | appointment_date
------------- | ------------ | -------------- | ----------------
John Doe      | 1234567890   | ABC Corp       | March 15
Jane Smith    | 9876543210   | XYZ Inc        | March 16
Bob Johnson   | 5551234567   | Tech Ltd       | March 17
```

### Step 2: Upload and Map Columns

1. Upload your file to the app
2. Select which column contains **phone numbers**
3. Select which column contains **names** (optional)

### Step 3: Write Your Message with Variables

Use curly braces `{}` to insert variables from your columns:

**Example 1: Basic Personalization**
```
Hi {name}, your appointment is confirmed for {appointment_date}. See you soon!
```

**Example 2: Multiple Variables**
```
Hello {name}, thank you for choosing {company}! Your order #12345 is ready for pickup.
```

**Example 3: Without Name Column**
```
Your appointment is confirmed for {appointment_date}. Reply CONFIRM to verify.
```

## Available Variables

### Auto-Aliasing with Smart First Name Extraction

When you select a name column, these aliases are automatically created with **first name only**:
- `{name}` → **First name only** from your selected name column
- `{username}` → **First name only** from your selected name column

**Example:**
- Your column has: "John Doe"
- `{name}` becomes: "John"
- `{username}` becomes: "John"

If you want the **full name**, use the original column name (e.g., `{full_name}` or whatever your column is called).

### Any Column Name

You can use **any column** from your file as a variable:
- `{phone_number}` - The phone number
- `{company}` - Company name
- `{appointment_date}` - Appointment date
- `{order_id}` - Order ID
- `{amount}` - Amount due
- etc.

**Rule:** Column name must match exactly (case-sensitive)

## Message Preview

Before sending, the app shows a **live preview** using data from the first contact in your file.

**Your Template:**
```
Hi {name}, your {company} order is ready!
```

**Preview (First Contact):**
```
Hi John Doe, your ABC Corp order is ready!
```

## First Name vs Full Name Examples

**Your Excel/CSV has:**
```
customer_name      | phone_number
------------------ | ------------
John Doe           | 1234567890
Sarah Smith        | 9876543210
Robert Johnson     | 5551234567
```

### Using First Name Only (Recommended)
**Message:**
```
Hi {name}, your order is ready for pickup!
```

**Results:**
- "Hi John, your order is ready for pickup!"
- "Hi Sarah, your order is ready for pickup!"
- "Hi Robert, your order is ready for pickup!"

### Using Full Name
**Message:**
```
Dear {customer_name}, thank you for your business.
```

**Results:**
- "Dear John Doe, thank you for your business."
- "Dear Sarah Smith, thank you for your business."
- "Dear Robert Johnson, thank you for your business."

## Real-World Examples

### 1. Appointment Reminders
```
Hi {name}, reminder: Your appointment with Dr. {doctor} is on {date} at {time}. Reply C to confirm.
```
*Note: {name} will be "John" not "John Doe"*

### 2. Order Notifications
```
Hello {name}! Your order #{order_id} from {company} has shipped. Track: {tracking_url}
```

### 3. Payment Reminders
```
Dear {name}, your payment of ${amount} for invoice #{invoice_id} is due on {due_date}. Pay now: {payment_link}
```

### 4. Event Invitations
```
Hi {name}! You're invited to {event_name} on {event_date}. RSVP: {rsvp_link}
```

### 5. Promotional Messages
```
Exclusive for you, {name}! Get {discount}% off at {store_name}. Use code: {promo_code}. Valid until {expiry_date}.
```

## Tips for Best Results

### ✅ Do's

1. **Test with small batch first**: Upload a file with 2-3 contacts to test
2. **Check preview**: Always verify the preview looks correct
3. **Use meaningful column names**: `customer_name` instead of `col1`
4. **Include fallback text**: Don't rely only on variables
5. **Keep it concise**: Remember SMS character limits (160 chars per message)

### ❌ Don'ts

1. **Don't use variables that don't exist**: Make sure column names match
2. **Don't forget curly braces**: Use `{name}` not `name`
3. **Don't use special characters in column names**: Stick to letters and underscores
4. **Don't make messages too long**: Longer messages = multiple SMS = higher cost

## Character Count

The app shows estimated SMS parts based on your **template**. Actual count may vary per contact depending on:
- Length of personalized data
- Use of special characters (emojis use more space)

**Example:**
- Template: `Hi {name}, welcome!` (18 chars)
- For "John Doe": `Hi John Doe, welcome!` (21 chars)
- For "Alexander Smith": `Hi Alexander Smith, welcome!` (29 chars)

## Troubleshooting

### Issue: Variable not replaced

**Problem:** Message shows `{name}` instead of actual name
**Solution:** 
- Check column name spelling (case-sensitive)
- Ensure column exists in your file
- Verify you selected the name column in the app

### Issue: Some messages have empty variables

**Problem:** Message shows `Hi , welcome!` (missing name)
**Solution:**
- Check if some rows have empty values in that column
- Fill in missing data in your Excel/CSV file
- Or adjust message to handle empty values: `Hi there, welcome!`

### Issue: Message preview not updating

**Solution:**
- Re-upload the file
- Change the SMS message content
- Refresh the browser page

## Sample Template Files

Download and modify these templates:
- `sample_contacts_template.xlsx` - Excel template
- `sample_contacts_template.csv` - CSV template

Both include example data showing:
- name
- phone_number  
- company

Add more columns as needed for your use case!

## Advanced Usage

### Using Multiple Data Points

You can use as many variables as you want:

```
{name}, your {product} order is ready! 
Pickup at {store_location} on {pickup_date}. 
Total: ${total_amount}. Ref: {order_id}
```

Just make sure your Excel/CSV has all these columns!

### Conditional-like Messages (Manual)

Since the app doesn't support conditional logic, prepare different files for different message types:

**File 1: VIP_Customers.xlsx**
```
Hi {name}, as a VIP member, enjoy exclusive early access to our sale!
```

**File 2: Regular_Customers.xlsx**
```
Hi {name}, our sale starts tomorrow. Don't miss out!
```

Upload and send separately.

## Need Help?

- Check the preview before sending
- Test with 1-2 contacts first
- Verify all column names are spelled correctly
- Make sure all required columns have data

Happy sending! 🚀

