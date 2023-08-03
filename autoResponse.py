import imaplib
import email
import smtplib
from email.mime.text import MIMEText
import os
import re

# Email account credentials
recipient_email = "fariyaprinces028@gmail.com"
recipient_password = "thnwlolbvvwjwpsw"

# Function to extract recipient name from email address
def extract_recipient_name(email_address):
    # Use regular expression to extract the name part from the email address
    name = re.search(r'(.+?)\s*<.*>', email_address)
    if name:
        return name.group(1)
    return email_address.split("@")[0]

# Function to send an auto-reply email
def send_auto_reply(sender_email):
    subject = "Auto Reply: Thank you for your email"
    recipient_name = extract_recipient_name(sender_email)
    body = f"""Dear {recipient_name},\nThank you for reaching out to us. We appreciate your patience and understand that you may have questions or concerns regarding your purchase.

Please be assured that a customer service representative will be in touch with you shortly to assist you. Our team is dedicated to providing you with the best possible service and resolving any issues you may encounter.

We value your business and are committed to ensuring your satisfaction. Thank you for choosing to shop with us.

Best Regards,
[Your Name]
[Your Seller Name]"""

    message = MIMEText(body)
    message["From"] = recipient_email
    message["To"] = sender_email
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(recipient_email, recipient_password)
        server.sendmail(recipient_email, sender_email, message.as_string())

# Function to decode email content
def decode_email_content(part):
    try:
        return part.get_payload(decode=True).decode('utf-8')
    except UnicodeDecodeError:
        return part.get_payload(decode=True).decode('latin-1')

# Function to check if an email ID has been replied to
def is_email_replied(email_id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    replied_ids_file = os.path.join(script_dir, "replied_ids.txt")

    if os.path.exists(replied_ids_file):
        with open(replied_ids_file, "r") as f:
            replied_ids = f.read().splitlines()
    else:
        replied_ids = []

    return email_id in replied_ids

# Function to mark an email ID as replied
def mark_email_as_replied(email_id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    replied_ids_file = os.path.join(script_dir, "replied_ids.txt")

    with open(replied_ids_file, "a") as f:
        f.write(email_id + "\n")

# Connect to the IMAP server and check for new emails
with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
    mail.login(recipient_email, recipient_password)
    mail.select("INBOX")
    
    # Search for all unseen emails
    status, email_ids = mail.search(None, "(UNSEEN)")
    email_ids = email_ids[0].split()
    
    # List to store the details of unseen emails in the inbox
    inbox = []
    
    # Check if there are any unseen emails
    if not email_ids:
        print("No unseen emails.")
    else:
        for email_id in email_ids:
            _, email_data = mail.fetch(email_id, "(RFC822)")
            raw_email = email_data[0][1]
            message = email.message_from_bytes(raw_email)
            
            # Get the sender's email address
            sender_email = message["From"]
            # Get the email subject
            subject = message["Subject"]
            # Get the email body
            body = ""
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = decode_email_content(part)
                        break
            else:
                body = decode_email_content(message)
            
            # Check if the email ID has been replied to
            if not is_email_replied(email_id.decode()):
                # Store the email details in the inbox
                inbox.append({"Sender": sender_email, "Subject": subject, "Body": body})
                
                # Mark the email as replied
                mark_email_as_replied(email_id.decode())
    
    # Print the inbox of unseen mail
    if inbox:
        print("Inbox of Unseen Mail:")
        for index, email_details in enumerate(inbox, start=1):
            print(f"Email {index}:")
            print("Sender:", email_details["Sender"])
            print("Subject:", email_details["Subject"])
            print("Body:", email_details["Body"])
            print("-" * 30)
            
            # Send auto-reply to the sender
            send_auto_reply(email_details["Sender"])
    else:
        print("No unseen emails in the inbox.")
    
    print("Auto-reply process completed.")
