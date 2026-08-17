[[common commands]] [[CLI]] [[Linux process commands]] [[ps]] [[top]] [[Linux network commands]] [[ss]] [[dig]] [[ip]] [[Services commands]] [[systemctl]] [[journalctl]] [[INDEX]]

# Linux CLI

> Consolidated Linux CLI reference — commands grouped by incident job, with deep-dive links to leaf notes.

---

## Shell & daily ops

From [[common commands]].

```bash
cd -
pwd -P
realpath ./relative
mkdir -p a/b/c

find . -type f -size +100M -printf '%s %p\n' | sort -rn | head
find /var/log -type f -name '*.log' -mtime +14 -ls
du -sh */ | sort -hr | head

grep -R --exclude-dir={.git,node_modules,dist} 'pattern' .
grep -RIn 'ERROR' /var/log/app/ --include='*.log'
rg 'pattern' --glob '!node_modules'

ps aux --sort=-%mem | head -20
df -hT
lsof +D /path/to/dir 2>/dev/null

find . -name '*.tmp' -print
find . -name '*.tmp' -delete

tar czf backup-$(date +%F).tar.gz --exclude=node_modules project/
chmod -R u+rwX,go-rwx sensitive_dir/

date -u +%Y-%m-%dT%H:%M:%SZ
id; groups; whoami
```

From [[CLI]].

```bash
man grep
grep --help
sudo systemctl restart nginx
test -f /etc/hosts && echo "exists" || echo "missing"
output=$(hostname -f)
```


## Process & resources

From [[Linux process commands]].

```bash
pgrep -af nginx
pidof java
ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | head

top
pidstat 1 5

lsof -p <pid>
sudo lsof -iTCP:8080 -sTCP:LISTEN
ls -l /proc/<pid>/fd

kill -TERM <pid>
kill -KILL <pid>
pkill -TERM -f 'my-worker'
kill -l

renice -n 5 -p <pid>

systemctl status foo.service
systemctl restart foo.service
```

From [[ps]].

```bash
ps aux
ps -ef
ps -eo pid,ppid,user,stat,tty,rss,pcpu,cmd --sort=-rss | head
ps -p <pid> -o user,pid,ppid,stat,tty,wchan:20,cmd
ps -u "$USER" -o pid,stat,cmd
ps -efH
pstree -p <pid>
ps -L -p <pid> -o pid,tid,psr,stat,pcpu,cmd
pmap -x <pid>
kill -s TERM <pid>
```

From [[top]].

```bash
top
top -bn1 | head -n 20
top -p <pid>
top -u <user>
mpstat 1
vmstat 1
nproc
```


## Networking

From [[Linux network commands]].

```bash
ss -lntup
ss -tnp | head
sudo lsof -iTCP:443 -sTCP:LISTEN

ip route get 1.1.1.1
nc -zv -w 3 host 443
dig +short example.com
resolvectl query example.com

sudo tcpdump -ni eth0 port 443
sudo ufw status verbose
```

From [[ss]].

```bash
ss -luntp
ss -tan
ss -s
ss -lntp 'sport = :443'
sudo ss -lntp 'sport = :443'
ss -tn dst 10.0.1.50 and dport = 5432
ss -ti
ss -tan state time-wait
ss -tan state established
ss -tan state syn-recv
ss -tan state close-wait
```

From [[dig]].

```bash
dig example.com
dig +short example.com
dig @8.8.8.8 example.com A
dig example.com AAAA
dig example.com MX
dig example.com CNAME
dig example.com NS

dig +trace example.com
dig @ns1.example.net example.com A

resolvectl status
dig example.com.          # trailing dot = FQDN, no search

dig @$(dig +short example.com NS | head -1) example.com A
```

From [[ip]].

```bash
ip link show
ip link set dev ens5 up
ip link set dev ens5 mtu 9000
ip -s link show ens5

ip addr show dev ens5
ip addr add 10.0.0.5/24 dev ens5
ip addr del 10.0.0.5/24 dev ens5

ip route show
ip -d route show
ip route show table all
ip rule list
ip route get 8.8.8.8
ip route replace default via 192.168.1.1
ip route add 10.20.0.0/16 via 10.0.0.1 dev eth0

ip neigh show
ip neigh flush dev eth0

ip link add link eth0 name eth0.100 type vlan id 100
```


## Services & systemd

From [[Services commands]].

```bash
systemctl --failed
systemctl status nginx.service
systemctl list-units --type=service --state=running

sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx

sudo systemctl enable nginx
sudo systemctl disable nginx
sudo systemctl is-enabled nginx

sudo systemctl daemon-reload
sudo systemctl restart myapp.service

sudo systemctl mask foo.service
sudo systemctl unmask foo.service
systemctl list-dependencies nginx.service

busctl list
journalctl -u nginx.service -b --no-pager
journalctl -u nginx.service -f
journalctl -p err -b

sudo service nginx status               # legacy wrapper
```

From [[systemctl]].

```bash
systemctl status nginx --no-pager
sudo systemctl restart nginx
sudo systemctl enable --now nginx
systemctl is-enabled nginx
systemctl list-units --failed
sudo systemctl daemon-reload
systemctl cat nginx
journalctl -u nginx -b --no-pager | tail
systemctl reload ssh
systemctl reload-or-restart ssh
systemctl edit ssh
systemctl show ssh -p FragmentPath
systemctl reset-failed
systemctl list-unit-files --type=service
systemctl get-default
systemctl list-dependencies ssh.service
systemd-analyze blame
systemd-analyze critical-chain
```

From [[journalctl]].

```bash
journalctl -u nginx.service -b --no-pager
journalctl -u myapp.service -f
journalctl -u myapp -n 100 --no-pager

journalctl -u sshd --since "1 hour ago"
journalctl --since "2024-03-01" --until "2024-03-18"
journalctl -p err -b
journalctl -u myapp -p err..crit

# Boot navigation
journalctl -b -1                   # previous boot (crash analysis)
journalctl --list-boots
journalctl -b <boot id>            # specific boot id

# Kernel only
journalctl -k

journalctl _EXE=/usr/bin/nginx
journalctl _UID=1000 --since today

journalctl -u myapp -o json | jq .
journalctl --utc --no-pager

journalctl --disk-usage
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=1week
```


## Users & authentication

From [[Authentication command]].

```bash
ssh-keyscan hostname
ssh-keyscan -p 2222 hostname
ssh-keygen -R hostname

ssh-keygen -t ed25519 -C "you@example"
ssh-copy-id user@remote-host
ssh-add -l
ssh -v user@hostname

sudo apt install gnupg
gpg --full-gen-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <keyid>

git config --global user.signingkey <keyid>
git config --global commit.gpgsign true
git commit -S -m "signed"
git log --show-signature
```

From [[useradd]].

```bash
sudo useradd -m -s /bin/bash -c "SDE team" alice
sudo passwd alice
sudo usermod -aG sudo alice
sudo useradd --system --home /var/lib/myapp --shell /usr/sbin/nologin myapp
sudo usermod -d /home/alice -m alice
sudo cp -a /etc/skel/. /home/alice/
sudo chown -R alice:alice /home/alice
sudo adduser bob
```

From [[passwd]].

```bash
passwd
sudo passwd deploy
sudo passwd -l compromised_user
sudo passwd -u compromised_user
sudo passwd -e contractor
echo 'user:NewSecurePass' | sudo chpasswd
sudo chage -l username
sudo chage -M 90 username
sudo chage -W 14 username
sudo chage -E 2026-12-31 username
sudo passwd -S username
getent shadow username | cut -d: -f1-2
```


## Files & search

From [[Find command]].

```bash
find . -name '*.txt'
find /var/log -type f -name '*.log'
find /path -type d -empty
find /path -type f -empty

find /home -mtime -30
find . -mtime -7
find . -size +10M
find /srv -user root
find . -perm 644

find . -name '*.log' -print          # preview
find . -name '*.log' -delete
find . -type f -exec chmod 644 {} +
find . -name '*.log' -exec rm -f {} +

find /path -maxdepth 2 -mindepth 1 -type d
```

From [[grep]].

```bash
grep -i error /var/log/syslog
journalctl -u nginx --no-pager | grep -E 'error|crit|emerg'

grep -rn 'PasswordAuthentication' /etc/ssh/
grep -r --include='*.conf' 'listen' /etc/nginx/
grep -A2 -B1 'Exception' app.log
grep -F '$HOME' script.sh
grep -rl 'API_KEY' /opt/app/config/

ss -lntp | grep ':443'
grep -c 'FAILED' /var/log/auth.log
grep -v '^#' /etc/app.conf | grep -v '^$'

grep -E 'error|warn|fatal' app.log
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' access.log
grep -r --exclude-dir={.git,node_modules} PATTERN .
```

From [[rsync]].

```bash
rsync -avhn --delete /data/app/ /backup/app-$(date +%F)/
rsync -avh --delete /data/app/ /backup/app-$(date +%F)/

rsync -avz -e "ssh -i ~/.ssh/deploy -p 2222" \
  ./dist/ user@host:/var/www/app/

rsync -av --exclude='node_modules' --exclude='.git' \
  project/ user@host:/opt/project/

rsync -avnc --delete staging/ prod/
rsync -av --bwlimit=5000 src/ dest/
rsync -avP src/ dest/
```


## Packages (Debian/Ubuntu)

From [[APT policy]].

```bash
apt policy
apt policy nginx
apt-cache policy nginx
apt list -a nginx
```
