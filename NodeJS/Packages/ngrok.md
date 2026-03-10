## Installation
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null

echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list

sudo apt update && sudo apt install ngrok
```

```bash
npm install -g ngrok;
ngrok http 3000;
```
- you will get a public URL like

```bash
ngrok config add-authtoken <YOUR_AUTHTOKEN>
```

```txt
https://c12345abc.ngrok.io → http://localhost:3000
```

> [!NOTE]
> `ngrok config edit` opens with `neno` editor for opening with vim `export EDITOR=vim`