---
title: "Publish your own post! (in Markdown)"
summary: "How to write in markdown and publish an article on the iScsc blog through GitHub's pull requests"
date: 2023-11-30T17:52:09-02:00
lastUpdate: 2023-11-30T17:52:09-02:00
tags: ["iscsc","blog","posts","markdown"]
author: ctmbl
draft: false
---

This blog aims to be open to everyone, not only iScsc members.  
Here is a little tutorial to show how to publish your own post :wink:

## 1- Write your post

Of course this is the first step, write an article in markdown format (the format used in GitHub, Discord,...): `.md`.  
Basically the only things you need to know are:
 - Huge titles with: `# My HUGE Title`, lesser big with `## Still big title`, and so one up to `###### really small title`
 - **bold** with `**bold**`, *italics* with `*italics*`
 - lists with 
```
My list:
 - blabla
 - blala 2
```
 - next paragraph by letting an **empty line**
 - [hyperlinks](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_are_hyperlinks) with `[some blabla](http://blabla.com)`
 - inline `code` with \`inline code\`
 - code section with:  
```
`` `py  
import pwn   
   
\# python code you got it  
`` `
Note: remove the whitespace : `` ` -> ``` I write it that way because it would be interpreted as code section otherwise... 
```
An online markdown editor to get used to it: https://stackedit.io/  
There is also a VSCode extension to render markdown in VSCode.

## 2- Write the header
**NOTE**: if this step bothers you go to the next one and we'll firgure it out later on the review process

The header contains all the information about your post: author, title, date,...  
It has basically this format:
```yml
---
title: "Publish your own post! (in Markdown)"
summary: "How to write in markdown and publish an article on the iScsc blog through GitHub's pull requests"
date: 2023-11-30T17:52:09-02:00
lastUpdate: 2023-11-30T17:52:09-02:00
tags: ["iscsc","blog","posts","markdown"]
author: ctmbl
draft: false
---
```
These are the mandatory information, please fill in with your information and place right at the very beginning of the file!

## 3- Publish your post!
To publish your post you'll only need one thing: a [GitHub](https://github.com) account.

Once you've created it, go to https://github.com/iScsc/blog.iscsc.fr click on `Fork` on the top-right corner, approve by clicking `Create fork`: you've created your own copy of the blog!

Now click `Add file` then `Upload files`
![](../upload-files.png)

Then drag your new post in the box  
click create branch and click `Propose changes`


