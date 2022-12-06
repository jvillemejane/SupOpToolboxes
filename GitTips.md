# Git Tips

*from https://gist.github.com/luismts/*

## Properly Configure your `~/.gitconfig`

- Properly configure your user information
GitHub tracks your changes by using the information provided by your `~/.gitconfig`. If you work on more than one machine and your `~/.gitconfig` is not properly configured, you will probably end up with duplicated commits and disorganized history. Here are the lines you will have to modify according to your GitHub credentials.

```
[user]
	name = Guilherme M. Trein
	email = valid@email.com
```

## Cheat Sheet

### Create


| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| Clone an existing repository  | `$ git clone ssh://user@domain.com/repo.git`|
| Create a new local repository | `$ git init`                                |

### Local Changes

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| Changed files in your working directory | `$ git status` |
| Changes to tracked files | `$ git diff` |
| Add all current changes to the next commit | `$ git add .` |
| Add some changes in <file> to the next commit | `$ git add -p <file>` |
| Commit all local changes in tracked files | `$ git commit -a` |
| Commit previously staged changes | `$ git commit` |


### Commit History

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| Show all commits, starting with newest | `$ git log` |
| Show changes over time for a specific file | `$ git log -p <file>` |

### Branches and Tags

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| List all existing branches | `$ git branch` |
| Switch HEAD branch | `$ git checkout <branch>` |
| Create a new branch based on your current HEAD | `$ git branch <new-branch>` |
| Create a new tracking branch based on a remote branch | `$ git checkout --track <remote/branch>` |
| Delete a local branch | `$ git branch -d <branch>` |

### Update and Publish

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| List all currently configured remotes | `$ git remote -v` |
| Show information about a remote | `$ git remote show <remote>` |
| Add new remote repository, named <remote> | `$ git remote add <remote> <url>` |
| Download all changes from <remote>, but don‘t integrate into HEAD | `$ git fetch <remote>` |
| Download changes and directly merge/ integrate into HEAD | `$ git pull <remote> <branch>` |
| Publish local changes on a remote | `$ git push <remote> <branch>` |
| Delete a branch on the remote | `$ git branch -dr <remote/branch>` |
| Publish your tags | `$ git push --tags` |

### Merge and Rebase

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| Merge <branch> into your current HEAD | `$ git merge <branch>` |
| Rebase your current HEAD onto <branch> (__Don‘t rebase published commits!__) | `$ git rebase <branch>` |
| Abort a rebase | `$ git rebase --abort` |
| Continue a rebase after resolving conflicts | `$ git rebase --continue` |
| Use your configured merge tool to solve conflicts | `$ git mergetool` |
| Use your editor to manually solve con- flicts and (after resolving) mark file as resolved | `$ git add <resolved-file> $ git rm <resolved-file>` |

### Undo

| Operation                                      | Command                    |
|------------------------------------------------|----------------------------|
| Discard all local changes in your working directory | `$ git reset --hard HEAD` |
| Discard local changes in a specific file | `$ git checkout HEAD <file>` |
| Revert a commit (by producing a new commit with contrary changes) | `$ git revert <commit>` |
| Reset your HEAD pointer to a previous commit and discard all changes since then | `$ git reset --hard <commit>` |
| Reset your HEAD pointer to a previous commit and preserve all changes as unstaged changes | `$ git reset <commit>` |
| Reset your HEAD pointer to a previous commit and preserve uncommitted local changes | `$ git reset --keep <commit>` |