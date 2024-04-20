
## What are forks ?

### A quick explanation

To make it simple, forks are copies of a repository you want to work on. This way, you can work on your version of the repository, create branches, experiment stuff, commit and pull request.

On many repositories you will not have the write access. Yet, you can still propose changes by forking the repository, working on it, and when finished, pull requesting the original repository you made the fork from.

### How to make one

To make a fork from a repository you want to work on, nothing more simple :
You can simply go on the github repository page, an press the designated button!

For instance, if you want to propose changes for our game [**Haunted Chronicles**](https://github.com/iScsc/Haunted-Chronicles), you can do it this way :

![](fork-creation-1.png)

They will ask to name the fork repository but it have no importance, you can keep the original name.

![](fork-creation-2.png)

When it is done, you will have created a new repository on your own github :

![](fork-creation-3.png)

We can see the original repository it has been forked from, and you can quickly access it through this link.

## Working with forks

Now that you have forked the repository you want to work on, you simply have to experiment on your fork!

First, clone your fork on your computer to work on it with the link of your repository.

```git clone <link_to_your_fork>```

In this example, `<link_to_your_fork>` would be `git@github.com:ZynoXelek/Haunted-Chronicles.git` :
![](working-on-your-fork-1.png)
Using the ssh url first requires to have set up your SSH key with your github account. If you have not done it yet, you should probably read [Github - Create a SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [GitHub - add a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) first.

Then, you can create a new branch by using the command :
```git branch <your_branch_name>```

You can then place your git `HEAD` on this new branch by using the command :
```git checkout <your_branch_name>```

When this is done, you can then work on your code !

Once you have finished your work - or your session - don't forget to commit your changes after adding your new changes! To do so, first check the differences between your local repository and the remote one with ```git status```

Then, you can selectively chose which files you want to add to your commit with ```git add <file1> <file2> ...``` or you can add them all with ```git add .```

If you have made a mistake, you can revert a `git add` by using `git reset <file1> <file2> ...` or `git reset` to unstage them all. This will keep your local changes.

Don't hesitate to use `git status` between each command to clearly see the actual state of your commit! You can also use the magic command `git log --graph --oneline --all --decorate` to see the actual state of your local and distant repositories in the nicest way!

Be careful, `git rm <file>` exists but it will permanently remove the file from the repository!

When you have finished staging all your changes, you can commit by using the `commit` command :
```git commit -m <your_commit_name>```

Note that this will just commit your changes on your local branch.
When you want to send these changes to the remote repository, you shall use the `push` command :

```git push origin <your_branch>```

(Git commands are also integrated into some code editors such as `vs code`, but you should know that it may sometimes do some strange things, and using the terminal commands may make it easier to understand what really happens.)

## Pull requesting

When you have finished coding and you want to propose your changes to the origin repository, you will need to pull request.

To do so, you must first push your branch to the remote repository.
When it is done, simply go on the origin repository github page, and you will have the possibility to pull request your changes.

[Insert image here]

## Update your fork

Once your pull request have been accepted on the remote origin repository, you may update your fork to the new state of the origin repository.

To do so, you shall :

* 1 - Go on your fork page on github and press the update fork button :
[Insert image here]
* 2 - Then, to update your local copy, you should use these 3 commands :
* 2.1 - `git fetch origin` To download the remote state of the repository to your local github.
* 2.2 - `git checkout main` To put your git `HEAD` on your `main` branch before pulling the changes.
* 2.3 - `git rebase origin/main` To move your local main to remote reference you have just downloaded.
