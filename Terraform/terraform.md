```hcl
data "<provider>_<data_type>" "<name>" {
	# lookup filters/params
}
```
- `data` -> blocks are used to fetch existing infrastructure or external information read-only (not create/update/delete).

```hcl
data "aws_ami" "ubuntu" {
	most_recent = true
	owners = [""]
	filter {
		name = "name"
		values = [""]
	}
}

resource "aws_instance" "web" {
	ami = data.aws_ami.ubuntu.id
	instance_type = "t2.micro"
}
```

### Registry 
public hub of reusable terraform modules and providers.

providers -> Plugins for cloud APIs (AWS, GCP, GitHub).
Modules -> Pre-built infrastructure configs (VPC, EKS, RDS).

### Configure local with state storage (backend)
- store `terraform.tfstate` remotely (team access, locking etc.)