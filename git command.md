```bash
git reflog; # view git logs (not commit)
git push origin --tags; # push local tag to remote
git branch --unset-upstream; # unset remote tracking branch
```
#### Starter config
```bash
git config user.name <commit author name>;
git config user.email <commit author email>;
git config init.branch main; # main instead of master;
```
### Commands
```bash
git tag -l "v1.*"; # filter tag based on pattern
git tag -a <tagname> -m <message>; # annotate tag with name, email, message
git show <tagname>; # see detailed information about a tag
git tag -d <tagname>; # delete a tag
git push --delete origin <tagname>; # delete remote tag
git push origin --tags; # push all tags
git checkout <tagname>; # go to specific tag
```
### How to use tags to track different versions of code
- use annotated tags to mark important milestones like releases.
- store extra metadata like the author, date and message.
[manage different versions of your code with branching and tagging](https://www.linkedin.com/advice/3/how-can-you-manage-different-versions-your-code-branching)

