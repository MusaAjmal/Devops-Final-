terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.70"
    }
  }

  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}
}

# -------------------
# Resource Group
# -------------------
resource "azurerm_resource_group" "rg" {
  name     = "rg-infra"
  location = "centralindia"
}

# -------------------
# Virtual Network + Subnets
# -------------------
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-infra"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "subnet-infra"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# -------------------
# Network Security Group
# -------------------
resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-infra"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "subnet_nsg" {
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# -------------------
# AKS Cluster (Kubernetes)
# -------------------
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "aksinfra"

  default_node_pool {
    name           = "default"
    node_count     = 2
    vm_size        = "Standard_B2s_v2"
    vnet_subnet_id = azurerm_subnet.subnet.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }
}

# -------------------
# Aiven PostgreSQL Connection Info
# -------------------
variable "aiven_pg_host" {
  type    = string
  default = "pg-35318557-cuilahore-63ed.j.aivencloud.com"
}

variable "aiven_pg_port" {
  type    = number
  default = 5432
}

variable "aiven_pg_user" {
  type    = string
  default = "avnadmin"
}

variable "aiven_pg_password" {
  type    = string
  default = "AVNS_OQ0K1gICnzak5iV_ukC"
}

variable "aiven_pg_db" {
  type    = string
  default = "defaultdb"
}

# Output the connection info for use in your apps
output "aiven_postgres_connection" {
  value = {
    host     = var.aiven_pg_host
    port     = var.aiven_pg_port
    user     = var.aiven_pg_user
    password = var.aiven_pg_password
    database = var.aiven_pg_db
  }

  sensitive = true
}

# Output AKS kubeconfig
output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}
