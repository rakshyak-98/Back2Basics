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

### Installation
[Hashicorp installation linux](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
```shell
sudo apt install -y gnupg software-properties-common curl

```

```shell
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

```

```shell
sudo apt update && sudo apt install -y terraform
```

```shell
terraform -install-autocomplete;
```
