output "cluster_id" {
  value = ibm_container_vpc_cluster.my_cluster.id
}

output "registry_namespace" {
  value = ibm_container_registry_namespace.my_namespace.name
}
