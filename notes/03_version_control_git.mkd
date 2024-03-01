# Version Control with Git
no detailed notes as it is daily business

- Developers working on the same code
- Code is hosted centrally
- Every developer has an entire copy locally
- Code is fetched from remote remo and pushed to code repo

## Merge conflicts
-> when git cannot merge changes automatically
must be solved manually

Best practice: push and pull often to avoid conflicts
= Continuous Integration

Every code change and file is tracked

SVN = alternative to git

## Basic concepts
Remote Git Repo: where code lives
Local Git Repo: local copy of the code
History: git log -> history of code changes
Staging: changes to commit


## Git remote repository
- Github vs Gitlab
- companies have own git servers
- private vs public (f.e. open source, libs)

## Setup (with SSH key)
- create repo on gitlab or github
- generate ssh key on machine ( ssh-keygen -t rsa -b 4096 -C "your_email@example.com")
- see github guide, but needed on linux is also to have ss-agent running and key added
- add public key to github/gitlab

## Working with Git

Working locally -> Staging -> Committed

create local repository: git init
create remote project
add remote project: git remote add origin ...
git push --set-upstream origin master

## Branches

best practice: feature branches
git checkout my-existing-branch
git  checkout -b my-new-branch (be sure to be on right branch when creating -> will branch from current branch)

common practice: master & develop branch
-> merge feature to develop, after each sprint merge develop into master = Feature Driven Development

always merge feature to master = Trunk Based Development -> every single feature/bug fix is deployed (best practice from DevOps perspective)

## Delete Branch
git branch -d BRANCH

Delete remote branch on remote

## Rebase

to avoid merge branch commits

git pull -r <-- rebase flag
pulls changes, stacks our changes on top of it

if conflict: fix the conflict do git rebase --continue
git push

## Git ignore

To add a file/folder to gitignore that is already staged/committed:

1. adapt .gitignore file
2. git status -> should tell changes not staged for commit -> now do git rm -r --cached FOLDER (or . for all files)
3. git add
4. git commit & push

## Git stash

git stash -> all working changes to stash
git stash pop -> get the changes back


## Git history

each commit has specific hash

git log -> see history
git checkout COMMITHASH -> mostly used for testing or seeing when a bug was introduced

-> detached head state; we can create a new branch from this version as an example

head = latest commit state

## Undoing commits

git reset --hard HEAD~1 -> undo the last 1 commit; completely reset the changes

if we do not want to discard the changes, but change it

git reset HEAD~1 -> without the --hard flag the change is still there, but the commit is gone (change can be found in status, proably unstaged)

git commit -ammend -> to update the last commit that was made in local repository. Scenario committed, but later added a change that is also needed in prev commit -> changes are merged in the last commit

commit was completely wrong and we want to remove it:
git reset --hard HEAD~1
git push --force -> never do this in develop/main/branche where lot of people are working -> if others have already pulled changes from remote it causes troubles (history messed up)

## Undo commit in main/develop (revert)
git revert HASH -> creates a new commit that revert the old commit's changes
git push

## Merge
git merge BRANCH (take chances from BRANCH and merge into current branch)
git push

## Git for DevOps

f.e. K8s config files need to be managed somewhere
Terraform, Ansible configuration
Bash, Python scripts

should be tracked (history), shareable and securely stored

- Infrastructure as Code ^
- CI/CD Pipeline & Build automation
  Setup integration between build automation tool and git repo



