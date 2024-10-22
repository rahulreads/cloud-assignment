provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google" {
  alias   = "storage"
  project = var.project_id
  region  = var.region
}

# Terraform backend configuration
terraform {
  backend "gcs" {
    bucket = "my-terraform-statefile"  # Replace with your bucket name
    prefix = "terraform/state"       # Optional folder path within the bucket
  }
}
