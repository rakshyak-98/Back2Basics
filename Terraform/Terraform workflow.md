### Terraform commands

| Step       | Command             | Purpose                                     |
| ---------- | ------------------- | ------------------------------------------- |
| Initialize | `terrafrom init`    | Prepare the directory, downloads providers. |
| Plan       | `terraform plan`    | Shows what changes will be made.            |
| Apply      | `terraform apply`   | Deploy the infrastructure.                  |
| Destroy    | `terraform destroy` | Deletes the infrastructure.                 |
### Querying available providers
```shell
terraform providers;
terraform providers | grep aws;
terraform providers scheam -json;
terraform providers schema -json | jq 
```

```txt
│ Error: No configuration files
│ 
│ The directory /home/ubuntu/GitHub/Playground/terraform-playground contains no Terraform configuration files.
╵

```
- The error "No configuration files" means terraform couldn't find a `.tf` file in your directory.
- there should be a `.tf` file `main.tf`
```hcl
provider "aws" {
	region = "us-east-1"
}

```
- then initialize the terraform
```shell
terraform init
```
