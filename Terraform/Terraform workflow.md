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
terraform providers scheam -json | jq | head;
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

##### Query the schema
```shell
terraform providers schema -json | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas | keys'

```

```shell
terraform providers schema -json | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["aws_instance"]'

```
- Check details of a specific resource
- view EC2 `aws_instance` resource details.

### Querying Data Sources (Read-Only Resources)
- data sources let you query existing infrastructure.
- useful when working with pre-existing AWS resources.

```hcl

```

#### What happens If you type "yes" for `terraform apply`?
```txt
➜ terraform-playground $ terraform apply
data.aws_instances.all: Reading...
data.aws_instances.all: Read complete after 1s [id=ap-south-1]

Changes to Outputs:
  + ec2_instances = []

You can apply this plan to save these new output values to the Terraform state, without changing any real
infrastructure.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

```
- terraform is using a data source `data.aws_instances.all` to fetch existing EC2 instances in the region `ap-south-1`. 
- since terraform fetched the instance list successfully, it updates the Terraform state file `terraform.tfstate` whit the new value `ect_instances = []`
- in this Terraform will not create, modify, or delete any AWS resources it will only update its internal state.

> [!INFO] Terraform applies the changes only to the local state file `terraform.tfstate`.
-  AWS infrastructure remains unchanged.

### What is the purpose of `terraform.tfstate` file?
- Track resources, helps terraform understand what exists vs what need to change.
- Enables change detection -> `terraform plan` compares the state file with the `.tf` config to show what changes will be made.
- When using remote state storage (e.g., S3, Terraform Cloud), multiple team members can work on the same infrastructure safely.