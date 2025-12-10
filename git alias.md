```bash
git ls-files --ignored --exclude-standard --others | cut -d '/' -f1 | sort -u
```

> Add these as alias

```bash
git config --global alias.ignored 'ls-files --ignored --exclude-standard --others'
git config --global alias.ignoredtop '!git ignored | cut -d "/" -f1 | sort -u'
```

> user it like this

```bash
git ignoreedtop
```