from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage, pubsub_v1
import os
import json

app = FastAPI()

# Load environment variables (set via Docker or GCP Cloud Run)
BUCKET_NAME = "simple-assignment-bucket"
PUBSUB_TOPIC = "simple-topic"
PROJECT_ID = "my-app-361806"

# Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_NAME)

# Google Cloud Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)

# Pydantic model to validate the incoming JSON payload
class Message(BaseModel):
    message: str

@app.post("/receive")
async def receive_message(payload: Message):
    try:
        # 1. Save the JSON payload to a file in the cloud storage bucket
        blob = bucket.blob(f"{payload.message}.json")
        blob.upload_from_string(json.dumps(payload.dict()), content_type="application/json")
        
        # 2. Publish the message to a Pub/Sub topic
        future = publisher.publish(topic_path, data=payload.message.encode("utf-8"))
        future.result()  # Ensure the publish succeeded

        return {"status": "Message received and processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
