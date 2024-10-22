resource "google_storage_bucket" "my_microservice_bucket" {
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

resource "google_pubsub_topic" "my_microservice_topic" {
  name = var.pubsub_topic_name
}

resource "google_cloud_run_service" "microservice_cloudrun" {
  name     = "microservice-serverless-app"
  location = var.region

  template {
    spec {
      containers {
        image = "europe-west4-docker.pkg.dev/my-app-361806/my-demo-app/fastapi-microservice:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "BUCKET_NAME"
          value = google_storage_bucket.my_microservice_bucket.name
        }
        env {
          name  = "PUBSUB_TOPIC"
          value = google_pubsub_topic.my_microservice_topic.name
        }
      }
    }
  }

  autogenerate_revision_name = true
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = var.region
  service     = google_cloud_run_service.microservice_cloudrun.name

  policy_data = <<EOF
{
  "bindings": [
    {
      "role": "roles/run.invoker",
      "members": [
        "allUsers"
      ]
    }
  ]
}
EOF
}

output "cloud_run_url" {
  value = google_cloud_run_service.microservice_cloudrun.status[0].url
}
