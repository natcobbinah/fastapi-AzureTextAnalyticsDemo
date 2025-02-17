from environs import env
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

env.read_env()  # read .env file, if it exists
# required variables
ENDPOINT = env.str("ENDPOINT")
API_KEY = env.str("API_KEY")

text_analytics_client = TextAnalyticsClient(
    ENDPOINT, AzureKeyCredential(API_KEY))

def call_text_analytics_api(document):
    result = text_analytics_client.analyze_sentiment(
            document, show_opinion_mining=True)

    docs = [doc for doc in result if not doc.is_error]

    return docs