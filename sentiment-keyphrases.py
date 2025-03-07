from environs import env
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

env.read_env()  # read .env file, if it exists
# required variables
ENDPOINT = env.str("ENDPOINT")
API_KEY = env.str("API_KEY")

text_analytics_client = TextAnalyticsClient(
    ENDPOINT, AzureKeyCredential(API_KEY))

documents = [
    """I had the best day of my life. I decided to go sky-diving and it made me appreciate my whole life so much more.
    I developed a deep-connection with my instructor as well, and I feel as if I've made a life-long friend in her.""",
    """This was a waste of my time. All of the views on this drop are extremely boring, all I saw was grass. 0/10 would
    not recommend to any divers, even first timers.""",
    """This was pretty good! The sights were ok, and I had fun with my instructors! Can't complain too much about my experience""",
    """I only have one word for my experience: WOW!!! I can't believe I have had such a wonderful skydiving company right
    in my backyard this whole time! I will definitely be a repeat customer, and I want to take my grandmother skydiving too,
    I know she'll love it!"""
]

result = text_analytics_client.analyze_sentiment(
    documents, show_opinion_mining=True)
docs = [doc for doc in result if not doc.is_error]
print(type(docs))
print(docs)
print()

print("Let's visualize the sentiment of each of these documents")
for idx, doc in enumerate(docs):
    print(f"Document text: {documents[idx]}")
    print(f"Overall sentiment: {doc.sentiment}")
