> [!INFO]
> A user can belong to one primary group + zero or more supplementary (secondary) groups.

> [!INFO]
> Membership is stored in two places:
> - `/etc/passwd` → primary group (GID column)
> - `/etc/group` → list of users who are members of each supplementary group

Add group to user 

```text
usermod -aG <group> <current user>;
```

> [!NOTE]
> When you "add a group to a user" or "add a user to a group", you are modifying the supplementary groups — and both phrases describe the exact same action.

> [!NOTE]
> You need to refresh your session for the group membership to take effect.

```bash
newgrp <group>; # activate the group in current shell session
groups; # Verify it worked
```

`getent group <group>` -> `getent` group only shows users who have this group as a supplementary.
`groups` -> This command shows all effective groups that the user currently belongs to.

Remove group

```bash
gpasswd -d <user> <group>;
```

> [!INFO]
> The `gpasswd` command is used to administer `/etc/group`, and `/etc/gshadow`. Every group can have administrators, members and a password.

|Phrase|What the speaker is usually thinking about|Typical command used|
|---|---|---|
|"add group to user"|"I want this user to gain the privileges/permissions of this group"|`usermod -aG group user`|
|"add user to group"|"I want this group to include this user as a member"|`usermod -aG group user` or `gpasswd -a user group`|