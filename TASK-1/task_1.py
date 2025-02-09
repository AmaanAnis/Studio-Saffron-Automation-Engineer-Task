import pandas as pd
import datetime

data_csv = pd.read_csv("TASK-1/tasks.csv")

data_csv["Due Date"] = pd.to_datetime(data_csv["Due Date"]).dt.date


today = datetime.date.today()


data_pending = data_csv.drop(
    data_csv[(data_csv["Status"] == "Completed") & (data_csv["Due Date"] < today)].index
)


tasks_sorted_by_earliest_due_date = data_pending.sort_values(by="Due Date")

# print(tasks_sorted_by_earliest_due_date.head())

tasks_sorted_by_earliest_due_date.to_csv("TASK-1/cleaned_tasks.csv")

cleaned_csv = pd.read_csv("TASK-1/cleaned_tasks.csv")

number_of_pending_tasks = len(cleaned_csv)


most_urgent_task = cleaned_csv["Due Date"].min()

overdue_tasks_count = data_csv[data_csv["Due Date"] < today].shape[0]

print(cleaned_csv.head())
from fpdf import FPDF

# Create PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Task Summary Report", ln=True, align="C")

pdf.ln(10)

pdf.set_font("Arial", size=12)
pdf.cell(200, 10, f"Total Pending Tasks: {number_of_pending_tasks}", ln=True)

pdf.cell(200, 10, f"Most Urgent Task: {most_urgent_task}", ln=True)

pdf.cell(200, 10, f"Overdue Tasks Removed: {overdue_tasks_count}", ln=True)

pdf.output("TASK-1/task_summary_report.pdf")

print("PDF report generated: task_summary_report.pdf")


import smtplib
import email.message


def send_email_with_attachment(
    sender_email, sender_password, receiver_email, subject, body, attachment_path
):
    msg = email.message.EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = attachment_path.split("/")[-1]
    msg.add_attachment(
        file_data, maintype="application", subtype="pdf", filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


send_email_with_attachment(
    sender_email="your_email@gmail.com",
    sender_password="your_email_password",
    receiver_email="recipient@example.com",
    subject="Task Summary Report",
    body="Please find attached the task summary report.",
    attachment_path="task_summary_report.pdf",
)
