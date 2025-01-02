variable "ibmcloud_api_key" {
  description = "IBM Cloud API key"
  type        = string
}

variable "region" {
  description = "Region for resources"
  type        = string
  default     = "us-south"
}

variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for cluster"
  type        = string
}

variable "worker_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}

variable "worker_zones" {
  description = "Worker zones"
  type        = list(string)
  default     = ["us-south-1", "us-south-2"]
}

variable "registry_namespace" {
  description = "Container registry namespace"
  type        = string
}
