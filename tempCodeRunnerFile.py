def send_email_alert():
    sender_email = "kushbajpai2003@gmail.com"
    receiver_email = "kushbajpai20003@gmail.com"                                                 
    password = "obpe abrh ocrn yczt"

    subject = "Animal Intrusion Alert"
    body = "An animal intrusion has been detected by the system. Please take necessary action.🚨🚨🆘🆘😮😮😮"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")