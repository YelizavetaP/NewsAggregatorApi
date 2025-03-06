import requests
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import unquote
from googlenewsdecoder import gnewsdecoder
import trafilatura

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import (
    GOOGLE_NEWS_BASE_URL,
    VALID_TOPICS,
    ARTICLES_PER_TOPIC
)

import os
from dotenv import load_dotenv

load_dotenv()

def url_decode(url: str) -> str:
        """Decode Google News URL to get the actual article URL"""
        try:
            interval_time = 1  # interval between requests
            decoded_url = gnewsdecoder(url, interval=interval_time)

            if decoded_url.get("status"):
               print(f"Successfully decoded URL: {decoded_url['decoded_url']}")
               return decoded_url["decoded_url"]
            else:
                print(f"Failed to decode URL: {decoded_url["message"]}")
                return url

        except Exception as e:
            print(f"Error decoding URL {url}: {str(e)}")
            return url
        
def extract_article_content(url: str):
        """Extract article content using trafilatura"""
        try:
            print(f"Extracting content from: {url}")

            # Download the webpage content
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                # print(f"Failed to download content from: {url}")
                return None

            # Extract the main text content
            text = trafilatura.extract(downloaded)
            if not text:
                # print(f"No text content extracted from: {url}")
                return None

            # print(f"Successfully extracted content from: {url}")
            return text

        except Exception as e:
            print(f"Error extracting article content: {str(e)}")
            return None



def get_summary(story_contents, story_headlines):
    """Get summary of the story"""

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=os.getenv('OPENAI_API_KEY'))



    print('Starting content combination')


    combined_text = ""
    for content in story_contents:
        # print(type(content))
        if content: combined_text += '\n' + content


    summary = llm.invoke(
        [
            SystemMessage(
                content="""Create a summary in 500 words of the story based on the content provided that captures the key points from multiple related news articles."""),
            HumanMessage(content=combined_text),
        ]
    )

    print('Starting headlines generation')

    combined_headlines = ""
    for headline in story_headlines:
        # print(type(headline))
        combined_headlines += ', ' + headline

    headline = llm.invoke(
        [
            SystemMessage(
                content="""Create a headline for the story based on the provided headline examples. Do not add any aditional formating symbols at the begining and the end."""),
            HumanMessage(content=combined_headlines),
        ]
    )

    # headline = llm.invoke(
    #     [
    #         SystemMessage(
    #             content="""Create a headline for the story based on the provided article contetnt"""),
    #         HumanMessage(content=summary.content),
    #     ]
    # )


    return summary.content, headline.content



def get_rss_feed(topic: str):
        """Fetch RSS feed for a specific topic using BeautifulSoup"""
        try:
            url = f"{GOOGLE_NEWS_BASE_URL}{topic}"

            print('-'*20)
            print(f"Fetching RSS feed from: {url}")
            print('-'*20)

            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            if not soup:
                print("Failed to parse RSS feed")
                return None

            items = soup.find_all('item')
            if not items:
                print(f"No entries found in RSS feed for topic: {topic}")
                return None

            data = {'topic': topic, 'articles': []}
            for item in items[:ARTICLES_PER_TOPIC]:

                story = []
                story_urls = []
                story_contents = []
                story_headlines = []

                description = item.description.text if item.description else ''
                desc_soup = BeautifulSoup(description, 'html.parser')

                for li in desc_soup.find_all('li'):

                    encoded_link = li.find('a')['href']
                    publisher = li.find('font').text.strip() if li.find('font') else 'Unknown'

                    # save all the headlines
                    headline = li.text.strip()
                    story_headlines.append(headline)


                    # save all the urls
                    decoded_url = url_decode(encoded_link)
                    story_urls.append(decoded_url)

                    # save all the contents
                    # mb change to combined text
                    article_content = extract_article_content(decoded_url)
                    story_contents.append(article_content)

                print('Starting summary generation')
                story_summary, story_headline = get_summary(story_contents, story_headlines)

                story = {
                            'headline': story_headline,
                            'summary': story_summary,
                            'urls': story_urls
                            # 'contents': story_contents,
                            # 'headlines': story_headlines,
                        }

                if story:  # Only add if we found related stories
                    # data.append({'section': story})
                    data['articles'].append(story)

                print(f"Successfully fetched {len(data)} sections for topic: {topic}")

            return data

        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error fetching RSS feed for topic {topic}: {str(e)}")
            return None




def get_topic_news(topic: str):
        """Get news for a specific topic"""
        print(f"Fetching news for topic: {topic}")

        if topic not in VALID_TOPICS:
            print(f"Invalid topic requested: {topic}")
            return {"error": "Invalid topic"}

        result = get_rss_feed(topic)

        if not result:
            print(f"Failed to fetch RSS feed for topic: {topic}\nValid topics are: {VALID_TOPICS}")
            return {"error": "Failed to fetch RSS feed"}

        return result