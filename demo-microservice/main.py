from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage, pubsub_v1
import os
import json

app = FastAPI()

# Load environment variables 
BUCKET_NAME = os.getenv("BUCKET_NAME")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")
PROJECT_ID = os.getenv("PROJECT_ID")

# Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_NAME)

# Google Cloud Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)

# Validate the incoming JSON payload
class Message(BaseModel):
    message: str

@app.post("/receive")
async def receive_message(payload: Message):
    try:
        # Save to cloud storage bucket
        blob = bucket.blob(f"{payload.message}.json")
        blob.upload_from_string(json.dumps(payload.dict()), content_type="application/json")
        
        # Publish the message to a Pub/Sub topic
        future = publisher.publish(topic_path, data=payload.message.encode("utf-8"))
        future.result()  

        return {"status": "Message received and processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
