```bash
helm list
helm get values 

```

- The `kind` field is not part of the basic required fields, but it can be added to specify the type of chart. The `kind` field should be used for custom resources, as it helps Helm understand how to process the resource during installation and upgrade