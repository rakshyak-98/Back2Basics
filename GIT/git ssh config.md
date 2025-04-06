### Relation Between `Host github-personal` and `git@github-personal`

1. **Host Entry in `~/.ssh/config`**:  
   - The `Host github-personal` in your SSH config file acts as an alias for connecting to GitHub.  
   - It defines a set of configurations (like `HostName`, `IdentityFile`, etc.) that SSH will use whenever the alias `github-personal` is referenced.  

2. **Usage in Git Commands**:  
   - When you use `git@github-personal` in Git commands, it tells Git to connect via SSH using the `Host` alias defined in the config file.
   - SSH replaces `github-personal` with the corresponding configuration, such as:  
     - `HostName`: The actual domain (e.g., `github.com`).  
     - `IdentityFile`: The specific SSH private key (e.g., `~/.ssh/id_rsa_personal`).  

3. **How Git Uses It**:  
   - For example, when you run:  
     ```bash
     git clone git@github-personal:username/repo.git
     ```  
     - Git invokes SSH with `github-personal` as the host.  
     - SSH looks up the `Host github-personal` entry in `~/.ssh/config` and applies its settings (e.g., `IdentityFile` for authentication).  
     - The connection is established using the corresponding private key (`id_rsa_personal` in this case).  

---

### Why Is This Important?  
It ensures that:  
- Git commands for multiple GitHub accounts can use the correct SSH key automatically.  
- You avoid conflicts when pushing, pulling, or committing code across different repositories.  


### Summary

1. **SSH Config File**: Configure SSH keys for both GitHub accounts.
2. **Repository-Level Config**: Set up Git credentials for repositories to pull, push, and commit code with the correct keys.

---

### Steps to Create SSH Config File

1. **Open or create the SSH config file**:
```bash
    nano ~/.ssh/config
```
    
2. **Add the configuration for both GitHub accounts**:  
```plaintext
	 Host github-personal
		HostName github.com
		User git
		IdentityFile ~/.ssh/id_rsa_personal
	
	Host github-work
		HostName github.com
		User git
		IdentityFile ~/.ssh/id_rsa_work
		
```
    
3. **Save and exit**:
    - Press `CTRL+O`, then `CTRL+X`.

---

### Repository-Level Configuration

1. **Clone each repository using the specific Host**:
    
    - Personal account:
        
        ```bash
        git clone git@github-personal:username/repo.git
        ```
        
    - Work account:
        
        ```bash
        git clone git@github-work:username/repo.git
        ```
        
2. **Set user credentials for each repository**:  
    Inside each repository folder, configure the corresponding username and email:
    
    ```bash
    git config user.name "Personal or Work Name"
    git config user.email "personal_or_work_email@example.com"
    ```
    

---

### Verification

1. Test pushing code to each repository to ensure the correct key is used:
    
    ```bash
    git push origin main
    ```
    
2. If you encounter issues, debug SSH using:
    
    ```bash
    ssh -T github-personal
    ssh -T github-work
    ```

## How does git identify the alias

- Git itself doesn’t directly "know" the alias. Instead, **SSH** handles the alias through its configuration in the `~/.ssh/config` file. Here's how it works step-by-step:

---

### How Git and SSH Work Together

1. **Git Command with SSH URL**:
    
    - When you run a command like:
        
        ```bash
        git clone git@github-personal:username/repo.git
        ```
        
2. **Git Passes the URL to SSH**:
    
    - Git identifies `git@github-personal` as an SSH URL and hands it over to the SSH client for connection.
3. **SSH Resolves the Alias**:
    
    - SSH checks its `~/.ssh/config` file for an entry named `Host github-personal`.
    - It finds the settings (e.g., `HostName`, `IdentityFile`) under `Host github-personal`.
4. **SSH Establishes the Connection**:
    
    - Using the `HostName` (e.g., `github.com`), it connects to GitHub.
    - The `IdentityFile` (e.g., `id_rsa_personal`) ensures the right private key is used.
5. **Git Completes the Operation**:
    
    - Once SSH establishes the connection, Git handles the rest of the repository operation (clone, push, pull, etc.).

---

### Example

Suppose your `~/.ssh/config` contains:

```plaintext
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_personal
```

- When Git sees `git@github-personal`, it:
    - Passes `github-personal` to SSH.
    - SSH resolves `github-personal` to `HostName github.com` and uses the specified key (`id_rsa_personal`).

---

### Key Points
- Git relies on SSH to resolve aliases.
- SSH aliases allow you to abstract host configurations, making it easier to manage multiple accounts or keys.

### Github official fingerprint error
```txt
The authenticity of host 'github.com (...)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.

```
- if the prompt matches, it's safe to type
```txt
+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU

```

to avoid prompt in future
```sh
ssh-keygen github.com >> ~/.ssh/known_hosts;

```
- this adds Github's host key to your known hosts and suppresses future trust prompts.