# main.tf — IaC пример: локальный файл как ресурс (не нужен облачный аккаунт)
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

# Переменные
variable "app_name" {
  default = "devops-app"
}

variable "replicas" {
  default = 2
}

variable "port" {
  default = 5000
}

# Ресурс: генерируем .env файл для приложения
resource "local_file" "app_env" {
  filename = "${path.module}/.env"
  content  = <<-EOT
    APP_NAME=${var.app_name}
    APP_PORT=${var.port}
    REPLICAS=${var.replicas}
  EOT
}

# Ресурс: генерируем README с текущей конфигурацией
resource "local_file" "config_readme" {
  filename = "${path.module}/CURRENT_CONFIG.md"
  content  = <<-EOT
    # Текущая конфигурация (управляется Terraform)

    - **Приложение:** ${var.app_name}
    - **Порт:** ${var.port}
    - **Реплики:** ${var.replicas}
  EOT
}

# Output — выводим информацию после apply
output "app_name" {
  value = var.app_name
}

output "app_port" {
  value = var.port
}

output "message" {
  value = "Конфигурация применена: ${var.replicas} реплик на порту ${var.port}"
}
