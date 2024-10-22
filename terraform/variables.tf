variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Cloud Storage bucket name"
  type        = string
}

variable "pubsub_topic_name" {
  description = "Pub/Sub topic name"
  type        = string
}
