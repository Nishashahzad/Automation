import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_mail', 'your_password')

sender = 'fariyaprinces028@gmail.com'

with open("file.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row['NAME']
        email = row['EMAIL']
        products_to_offer = row['PRODUCTS_TO_OFFER']
        product_brand = row['PRODUCT_BRAND']
        agent_name = row['AGENT_NAME']
        image_path = row['GRAPHICS']
        email_subject = row['SUBJECT']  # Adding SUBJECT column to the CSV file
        email_body = row['EMAIL_BODY'].format(name=name)
        email_body2 = row['EMAIL_BODY2']
        email_body3 = row['EMAIL_BODY3']

        # Create the multipart message
        email_msg = MIMEMultipart("alternative")
        email_msg['From'] = sender
        email_msg['To'] = email
        email_msg['Subject'] = email_subject  # Set the subject for the email

        # Create the HTML message part
        html_content = f'''<html>
                            <body>
                                <p>{email_body}</p>
                                <img src="cid:image1" alt="Image">
                                <p>{email_body2}</p>
                                <p>{email_body3}</p>
                            </body>
                          </html>'''
        html_part = MIMEText(html_content, "html")
        email_msg.attach(html_part)

        with open(os.path.join(image_path), "rb") as image_file:
            image = MIMEImage(image_file.read())
            image.add_header("Content-ID", "<image1>")
            email_msg.attach(image)
        
        # Send the email
        server.send_message(email_msg)
        print(f'Sent to {name}')

server.quit()
