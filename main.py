from aggregator import get_topic_news

from config import VALID_TOPICS, ARTICLES_PER_TOPIC
import json
from datetime import datetime

from emailsetup import send_email


def main():
    # topic = input(f"Valid topics: {VALID_TOPICS}\nChoose a topic: ")
    # num_articles = input(f"Choose a number of articles: ")
    # ARTICLES_PER_TOPIC = int(num_articles)


    for topic in VALID_TOPICS:
        data = get_topic_news(topic=topic)

        # Save to JSON file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"files/articles_{topic.lower()}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Articles saved to {filename}")

        send_email(data)

        print(f"Email {topic} was sent successfully!")

   
    # data = get_topic_news(topic=topic)

    #     # Save to JSON file with timestamp
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"files/articles_{topic.lower()}_{timestamp}.json"

    # with open(filename, 'w', encoding='utf-8') as f:
    #         json.dump(data, f, indent=4, ensure_ascii=False)

    # print(f"Articles saved to {filename}")

    # send_email(data)

    # print("Email was sent successfully!")



if __name__ == "__main__":
    main()
