
# Take Home Assignment 


## Terraform scripts 
This Terraform configuration deploys a stateless microservice to Google Cloud Run, provisions a Google Cloud Storage bucket for file storage, and sets up a Pub/Sub topic for message publishing.

## Prerequisites

1. **Install Terraform**: Ensure Terraform is installed on your local machine.
2. **Set up Google Cloud SDK**: Authenticate with your GCP account using the Google Cloud SDK.
   ```bash
   gcloud auth application-default login
   ```
3. **Use a service account**: To run the terraform script use a service account with the necessary permissions to access Cloud Ctorage, Pub/Sub topic and Cloud Run. Create the json key for the service account and set the envrionment variable GOOGLE_APPLICATION_CREDENTIALS
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS=<path to your json file>
  ```

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/rahulreads/cloud-assignment
cd terraform
```

### 2. Edit the Variables

Modify the `variables.tf` file to set your `project_id`, `region`, `bucket_name`, and `pubsub_topic_name`.

### 3. Initialize Terraform

Initialize Terraform by running:

```bash
terraform init
```

### 4. Apply the Terraform Configuration

Apply the configuration to provision the required infrastructure:

```bash
terraform apply
```

This command will create the following resources:
- A Cloud Run service
- A Cloud Storage bucket
- A Pub/Sub topic

### 5. Deploy the Docker Image

Once the infrastructure is set up, you need to deploy the microservice Docker image to Google Cloud Container Registry (GCR). First, build and push the image:

```bash
docker build -t gcr.io/<project-id>/microservice:latest .
docker push gcr.io/<project-id>/microservice:latest
```

### 6. Access the Cloud Run Service

After successful deployment, Terraform will output the URL of the Cloud Run service. You can use this URL to access and test the microservice.

## Testing

You can test the HTTP endpoint of the microservice by sending a JSON payload using `curl`:

```bash
curl -X POST <cloud_run_service_url>/receive \
-H "Content-Type: application/json" \
-d '{"message": "Hello World"}'
```

This will send a POST request to the `/receive` endpoint, where the microservice will handle the request by writing to the Cloud Storage bucket and publishing a message to the Pub/Sub topic.

### 7. Destroy the resources

Once done make sure you destroy the resources created using terraform.

```bash
terraform destroy
```






