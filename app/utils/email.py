import smtplib
from email.message import EmailMessage

def send_email_reminder(to_email: str, task_title: str, due_date: str):
    EMAIL_ADDRESS = "ishika190205@gmail.com"
    EMAIL_PASSWORD = "xxgm rdmo odtq ywxw"

    msg = EmailMessage()
    msg['Subject'] = f'Reminder: Task "{task_title}" is due soon!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(
        f"Hello,\n\nThis is a reminder that your task \"{task_title}\" is due on {due_date}.\n\nRegards,\nTask Manager"
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
