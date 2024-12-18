```shell
terraform providers;
terraform search <provider name>
terraform providers mirror <directory>; # Display providers installed locally 
```

```shell
terraform providers schema -provider=<provider-name>
terraform providers schema -provider=registry.terraform.io/hashicorp/aws
```

```shell
terraform providers schema -provider=<provider-name> -resource=<resource-type>
terraform providers schema -provider=registry.terraform.io/hashicorp/aws -resource=aws_instance
```
- Describes resource attributes, required fields, and usage.