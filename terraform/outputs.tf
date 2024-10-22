output "bucket_name" {
  value = google_storage_bucket.my_microservice_bucket.name
}

output "pubsub_topic_name" {
  value = google_pubsub_topic.my_microservice_topic.name
}

output "cloud_run_service_url" {
  value = google_cloud_run_service.microservice_cloudrun.status[0].url
}
