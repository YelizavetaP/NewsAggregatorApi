import yagmail
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()



TEMPLATE_EMAIL = """    


    """

def format_email(content):


    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=os.getenv('OPENAI_API_KEY'))



    summary = llm.invoke(
        [
            SystemMessage(
                content="""
                Format the content into a email template.
                Latest News Update Email Template:

                Generate an email summarizing the latest news updates in a structured format. 

                """),
            HumanMessage(content=content),
        ]
    )


    return summary.content


def send_email(content, reciver='liz47220@gmail.com'):

    # content = format_email(content)


    yag = yagmail.SMTP(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
    yag.send(to=reciver, subject='Test Email', contents=content)
    print("Email was sent successfully!")

