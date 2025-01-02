provider "ibm" {
  ibmcloud_api_key = var.ibmcloud_api_key
  region           = var.region
}

resource "ibm_container_vpc_cluster" "my_cluster" {
  name              = var.cluster_name
  region            = var.region
  vpc_id            = var.vpc_id
  worker_count      = var.worker_count
  hardware          = "shared"
  worker_zones      = var.worker_zones
}

resource "ibm_container_registry_namespace" "my_namespace" {
  name = var.registry_namespace
}
