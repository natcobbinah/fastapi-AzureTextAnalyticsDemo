from environs import env
import utils
from fastapi import FastAPI
from pydantic import BaseModel
import  logging 
from opencensus.ext.azure.log_exporter import AzureLogHandler

env.read_env()  # read .env file, if it exists
# required variables
INSTRUMENTATION_KEY = env.str("INSTRUMENTATION_KEY")


logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'))


app = FastAPI()


class Model(BaseModel):
    text_to_analyze: list


@app.post("/")
def analyze_text(text: Model): 
    data= []
    
    no_of_text = len(text.text_to_analyze)

    for i in range(no_of_text):
        documents = {
            "id": i+1,
            "language": "en",
            "text": text.text_to_analyze[i],
        }
        data.append(documents)

    sentiment_result = utils.call_text_analytics_api(data)
   
    grouped_sentiment_result = []

    for  result in sentiment_result:
        response = {
            "id": result.id,
            "sentiment": result.sentiment,
            "sentence":result.sentences[0].text
        }

        log_data = {
            "custom_dimensions":{
                "text_id": result.id,
                "text": result.sentences[0].text,
                "text_sentiment":result.sentiment,
            }
        }
        logger.info("Text processed successfully", extra=log_data)

        grouped_sentiment_result.append(response)

    
    return grouped_sentiment_result

  
    