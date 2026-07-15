```bash
sudo usermod -s /bin/bash <username>;

# Rename user 
sudo usermod -l <new name> <old name>; 

# Change home directory
sudo usermod -d /new/home -m <username>;

# Change primary group
sudo usermod -g <group> <username>;

# Add user to supplementrary group
sudo usermod -aG <group> <username>;
```