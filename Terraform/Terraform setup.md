Terraform scripts are not limited to AWS and GCP. Terraform is a cloud-agnostic Infrastructure as Code (IaC) tool that can manage resources across a wide range of providers. It works by using providers, which are plugins for specific services or platforms.

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
[Hashicorp installation Linux](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
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


## File structure
```txt
project-root/
│
├── main.tf         # core resources and module calls
├── variables.tf    # all variable definitions (type, default)
├── outputs.tf      # all output values
├── terraform.tfvars  # actual values for variables
├── backend.tf      # remote state backend (optional but common)
├── provider.tf     # provider block (or include in main.tf)
│
└── modules/        # reusable components
    └── <module-name>/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf

```

### Execution Order
1. Load all `.tf` files in the root (no specific order, just parsed together).
2. Read `variable.tf` + `terraform.tfvars` [[variable file]]


