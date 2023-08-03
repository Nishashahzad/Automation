import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_mail', 'your_password')

subject = "Congrats - you're now a Product Tester!"
msg_template = '''<html>
<body>
<p>Hi {NAME},</p>
<p>We value your opinion and appreciate your previous purchase and review of our product. That's why we're thrilled to invite you to join our exclusive Product Testing Program!</p>
<p>As a selected Product Tester, you'll have the opportunity to receive a FREE item of your choice from our latest collection, along with a $25 reward.</p>
<p>You can choose ONE of these products to try for FREE: {PRODUCTS_TO_OFFER}</p>
<p><img src="cid:image1" alt="" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}"></p>  <!-- Set width and height attributes -->
<p>To ensure a secure and hassle-free experience, the entire transaction process will be conducted through Amazon.</p>
<p>To confirm your participation as a Product Tester, simply reply to this email. We have limited spots available, so make sure to respond promptly.</p>
<p>Thank you for being a valued customer and for your ongoing support. We can't wait to hear what you think about our latest product!</p>
<p>Best,<br>
{AGENT_NAME}, Trusted Helper At {PRODUCT_BRAND}</p>
</body>
</html>'''

sender = 'your_mail'

with open("file1.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row['NAME']
        email = row['EMAIL']
        products_to_offer = row['PRODUCTS_TO_OFFER']
        product_brand = row['PRODUCT_BRAND']
        agent_name = row['AGENT_NAME']
        image_path = row['GRAPHICS']  # Path to the image file

        # Create a multipart message
        email_msg = MIMEMultipart("alternative")
        email_msg['From'] = sender
        email_msg['To'] = email
        email_msg['Subject'] = subject

        # Load the HTML content of the message
        html_content = msg_template.format(
            NAME=name,
            PRODUCTS_TO_OFFER=products_to_offer,
            PRODUCT_BRAND=product_brand,
            AGENT_NAME=agent_name,
            IMAGE_WIDTH="200",
            IMAGE_HEIGHT="200"
        )

        # Create the HTML message part
        html_part = MIMEText(html_content, "html")
        email_msg.attach(html_part)

        # Load the image and attach it to the email
        with open(image_path, "rb") as image_file:
            image = MIMEImage(image_file.read())
        image.add_header("Content-ID", "<image1>")
        email_msg.attach(image)

        # Send the email
        server.send_message(email_msg)
        print(f'Sent to {name}')

server.quit()
