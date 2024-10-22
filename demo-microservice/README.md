# FastAPI Microservice for GCP

## Description
FastAPI microservice. It accepts a JSON message via the `/receive` endpoint, saves the message as a file in Google Cloud Storage, and publishes it to a Pub/Sub topic. The service is designed to run statelessly and can be deployed on Google Cloud Run.

## How to Run Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI Application**:
 Set environment variables for BUCKET_NAME, PUBSUB_TOPIC, and PROJECT_ID.


```
export BUCKET_NAME=<your-bucket-name>
export PUBSUB_TOPIC=<your-topic-name>
export PROJECT_ID=<your-project-id>

uvicorn main:app --reload
```

3. **Test the API**: You can use curl or Postman to send a POST request to the /receive endpoint.

```
curl -X POST "http://127.0.0.1:8000/receive" -H "Content-Type: application/json" -d '{"message": "Hello World"}'
```


4. **Build the Docker image**:

```
docker build -t fastapi-microservice .
```


5. **Run the Docker container**:

```
docker run -p 8080:8080 fastapi-microservice
```


6. **Deployment on Google Cloud Run**:

Push the Docker image to artifact registry

```
docker tag fastapi-microservice gcr.io/<your-project-id>/fastapi-microservice:latest
docker push europe-west4-docker.pkg.dev/<your-project-id>/<your-repository>/fastapi-microservice:latest
```

7. **Deploy to Cloud Run**: You can deploy the microservice to Cloud Run using the following command:

```
gcloud run deploy fastapi-microservice \
    --image europe-west4-docker.pkg.dev/<your-project-id>/<your-repository>/fastapi-microservice:latest \
    --platform managed \
    --region europe-west4 \
    --allow-unauthenticated \
    --update-env-vars BUCKET_NAME=<your-bucket-name>,PUBSUB_TOPIC=<your-topic-name>,PROJECT_ID=<your-project-id>
```

Environment Variables

BUCKET_NAME: The name of the Cloud Storage bucket.

PUBSUB_TOPIC: The name of the Pub/Sub topic.

PROJECT_ID: Google Cloud project ID.
