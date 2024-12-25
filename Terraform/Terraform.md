Terraform scripts are not limited to AWS and GCP. Terraform is a cloud-agnostic Infrastructure as Code (IaC) tool that can manage resources across a wide rage of providers. It works by using providers, which are plugins for specific services or platforms.

---
Kubernetes:
```hcl
provider "kubernetes" {
	config_path = "~/.kube/config"
}
resource "kubernetes_namespace" "exmaple" {
	metadata {
		name = "exmaple-namespace"
	}
}
```