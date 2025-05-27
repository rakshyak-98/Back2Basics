```hcl
variable "variable_name" {
	tyep = <type>
	default = <value>
	description = "..."
}
```

```hcl
variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region to deploy to"
}
```

```hcl
variable "azs" {
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}
```

```hcl
variable "tags" {
  type = map(string)
  default = {
    Env = "dev"
    Owner = "team"
  }
}
```

```hcl
variable "app_config" {
  type = object({
    name     = string
    version  = string
    replicas = number
  })
}
```