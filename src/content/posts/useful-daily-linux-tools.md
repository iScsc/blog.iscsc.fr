---
title: "Say goodbye to GUI and welcome terminal in your Linux life"
summary: "A non-exhaustive list of tools I use every day to make my life easier"
date: 2023-05-12T13:03:19-02:00
lastUpdate: 2023-05-12T13:03:19-02:00
tags: ["linux","tools"]
author: ctmbl
draft: false
---

Recently we've introduced some members of the iScsc to cybersecurity, we've helped them (you guys!) solve their first challenges.   
It was amazing but it also remembered me dark memories from the time I wasn't comfortable in a terminal, time as come for **you** to pass that step too!!

So here is a non-exhaustive and to-be-completed list of tools you **need** to use to make yourself at home in a terminal.

### TL;DR
 - [`autojump`](https://github.com/wting/autojump): a cd command that learns and guess locations
 - [`tldr`](https://github.com/tldr-pages/tldr#what-is-tldr-pages): community maintained command cheatsheet to learn a command use in a second
 - [`liquidprompt`](https://github.com/nojhan/liquidprompt#examples): a prompt that "shows you *what* you need *when* you need it"

## do not walk, jump instead
You all know the `cd` command (for change-directory), but it can be quite a pain to use when the path is long, especially when you always go to the same folder, you wish you could do it more easily...

**Now** you can!  
[`autojump`](https://github.com/wting/autojump) is a wonderfull tool that could sometime replace your old `cd`, as stated in the repo's about it is "A cd command that learns - easily navigate directories from the command line" and it's used with an amazingly but extremely clear shortcut: `j` for jump of course.

Let's see an example:
```
[ctmbl:/home/ctmbl] $ j isc
/home/ctmbl/Documents/iSCSC/iscsc.fr
[ctmbl:/home/ctmbl/Documents/iSCSC/iscsc.fr] $
```
It literally learns the locations you often go and guess them!!! Awesome.

> install it on Ubuntu with `sudo apt install autojump` then **enable** it reading `cat /usr/share/doc/autojump/README.Debian`

## too long; didn't read
You know every Linux command? I personally don't, but that's no reason to be afraid of terminals.  
Because reading the `man`ual is a real pain, [`tldr`](https://github.com/tldr-pages/tldr#what-is-tldr-pages) you'll love it!

It's basically a tool  to get cheatsheet for every (or almost every) command you'll ever use.

Quick example:
```
$ # Ow f*** I forget how to make a file executable...
$ tldr chmod

  chmod

  Change the access permissions of a file or directory.
  More information: https://www.gnu.org/software/coreutils/chmod.

  - Give the [u]ser who owns a file the right to e[x]ecute it:
    chmod u+x path/to/file

  - Give the [u]ser rights to [r]ead and [w]rite to a file/directory:
    chmod u+rw path/to/file_or_directory

  - Remove e[x]ecutable rights from the [g]roup:
    chmod g-x path/to/file

... (you got it)
```
Now you know every Linux command :wink:  
You'll never (hmm...) read the `man` or google a command again!

> install it on Ubuntu with `sudo apt install tldr`

> /!\ after installation do not forget to `tldr -u` to update it (`tldr tldr` if you forget it :upside_down:)

## beautify your prompt so that you terminal feels like home

The "prompt" is what comes before you type anything in your terminal it usually looks like (at least in my memory on Ubuntu):  
`username@computer:~/Documents $` 

> Disclaimer: a good prompt is really a matter of taste so what's following is only **my** taste not a standard at all

It's great but not really beautiful nor useful...  
So say hello to [`liquidprompt`](https://github.com/nojhan/liquidprompt#examples)!

As stated by the repo's [README](https://github.com/nojhan/liquidprompt#why-liquidprompt) it is designed to  
"display **meaningful** information with *minimal visual clutter* and **maximum readability**"  
And that's why I love it.

It can prints your CPU temperature/use percentage (but only when they are over a configurable value), `git` repo info (but only if they are relevant), background running tasks...  
And of course it is fully configurable.

Anyway, whether you like it or not you can't deny it doesn't try to be the prettiest but the most useful!  
*(and whether you want it or not I strongly advise you choose a better prompt than the default on most distros!)*

> install it on Ubuntu with `sudo apt install liquidprompt`


## Conclusion
And that's it, I considered that these three are the most (tiny) useful tools I use on a daily basis.  
Of course there are many other commands/tools that you should use:
 - `git` and `gh`
 - `htop` and `ncdu`
 - `gparted`
 - `bash` :upside_down:
 - [`complete-alias`](https://github.com/cykerway/complete-alias)
 - other prompts
 - a good terminal
 - a good desktop environment
 - ... and many other I probably don't even know

But we can't talk about every of them, I don't use them all and most of the time it's a matter of taste.

Thanks for reading and hope you'll love them too!!
