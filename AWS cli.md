## Installation aws cli
[aws cli installation linux](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
```shell
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

```

- setup autocomplete
```shell
sudo apt install -y bash-completion;
complete -C "$(command -v aws_completer)" aws; 
echo 'complete -C "$(command -v aws_completer)" aws' >> ~/.bashrc
```

```shell
aws configure; # start configuring access key, secret, region
```
- output format to one of the following json, table, text, yaml
```shell
aws configure get output;
aws configure set output table;
```

> [!INFO] AWS does not allow direct viewing of stored secrets for security reasons.
- you can retrieve them if they are stored in AWS secret manager or your local AWS credentials file.

```shell
cat ~/.aws/credentials;
aws configure get aws_secret_access_key;
```
### Query
```shell
aws ec2 descripbe-regions --query "Regions[].RegionName"
```