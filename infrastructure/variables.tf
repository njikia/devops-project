variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "West Europe"
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "devops-project"
}
