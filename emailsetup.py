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
    # Check if content has the expected structure
    if not isinstance(content, dict) or 'topic' not in content or 'articles' not in content:
        raise ValueError("Invalid content structure. Expected dict with 'topic' and 'articles' keys")
    
    topic = content['topic']
    articles = content['articles']
    
    if not articles:
        raise ValueError("No articles found in the content")
    
    # Create HTML template
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 30px;
            }}
            .topic {{
                color: #2c3e50;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .article {{
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .headline {{
                color: #1a73e8;
                font-size: 20px;
                margin-bottom: 15px;
            }}
            .summary {{
                color: #666;
                margin-bottom: 15px;
            }}
            .urls {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
            }}
            .urls a {{
                color: #1a73e8;
                text-decoration: none;
                display: block;
                margin-bottom: 5px;
            }}
            .urls a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="topic">Latest News: {topic}</h1>
        </div>
    """
    
    for article in articles:
        if not isinstance(article, dict) or 'headline' not in article or 'summary' not in article or 'urls' not in article:
            print(f"Skipping invalid article structure: {article}")
            continue
            
        html_content += f"""
        <div class="article">
            <h2 class="headline">{article['headline']}</h2>
            <div class="summary">{article['summary']}</div>
            <div class="urls">
                <strong>Related Links:</strong><br>
                {''.join(f'<a href="{url}">{url}</a><br>' for url in article['urls'])}
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content


# def send_email(content, receiver='liz47220@gmail.com'):
def send_email(content, receiver='dafstar@zebratruth.com'):

    try:
        html_content = format_email(content)
        
        yag = yagmail.SMTP(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        yag.send(
            to=receiver,
            subject=f'Latest News Update: {content["topic"]}',
            contents=html_content
        )
        # print("Email was sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise

