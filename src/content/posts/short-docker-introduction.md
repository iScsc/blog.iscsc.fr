---
title: "Get Started with Docker"
summary: "A short introduction to what Docker is to give you the basic knowledge of what images and containers are"
date: 2023-05-13T23:30:28-02:00
lastUpdate: 2023-05-13T23:30:28-02:00
tags: ["docker","introduction"]
author: ctmbl
draft: false
---

**TL;DR**:
 - `docker` is a containerization tool, allowing you to **wrap your application whole environment** and easily install it on different OSs/environments [Portability section](#portability)
 - images are a **snapshot** of your wrapped application [images section](#images)
 - containers are a "running image" [containers section](#containers)
 - you **build** an image and **run** a container
 - containers are **essential** for large services/websites ([scalability section](#scalability)), **extremely useful** for smaller projects (development **and** installation)
 - containers and VMs are **not the same** [What about Virtual Machines](#what-about-virtual-machines)

## Why Docker
Yes sure that looks like a good start.  
So why the f\*\*\* do we need docker??
Applications are working quite well without it.

### Keep your host clean
This is maybe the first and one of the best arguments, at least to me: who hasn't one day said "I should really clean up my laptop".
Folders, dependencies, running processes, all these things are one day used/developped and then abandonned, messing your laptop and lowering free disk space, performances or battery health.  
Docker, containerization actually, solves quite well this issue by wrapping you're whole application and making it easy to be stored, stopped, or removed with only a few commands.

### Portability
This is for sure my second best arguments, but maybe the reason why `docker` has been written in the first place, who knows??? [[1]](#1-why-docker).

Thanks to Docker wrapping your application, libraries and dependencies, you can easily install it on every platform no matter the OS or the distro, in fact you're really **sharing the whole environment which includes everything that your application needs**!  
The only requirement is to have `docker` installed.

Your application is no longer dependant on the host OS libraries or version, say goodbye to these headaches debugging the famous "it works on my machine"!

### Scalability
This last point doesn't concern us at all, but let's see the bigger picture anyway.
Imagine you're GitHub (or any other ultra-visited website) dealing with millions of connection per day, do you **really** think it exists a single computer on this planet capable of handling it? If yes you'd be a fool!
Of course, this kind of traffic is way too huge to be handled by a single machine.

Then these companies have no other choices but to dispatch traffic on multiple servers (and databases), that need to be connected, and synchronized, and at the same version, and able to redirect users between them???
You start to see the whole problem: this is a very hard to do and bug-prone.
And there comes containerization, making it easy to specialize some containers, start and stop them to adapt to traffic, update the code version, and assemble them into networks.

Only remember this: at this level containerization is a necessity.

## How Docker??
Docker is build on top of a Linux feature: Linux Containers.
Without Linux Containers there would be no Docker, they provide the raw material to build containerized environment [[2]](#2-linux-containers).

> to know how containers are different from VMs check [What about Virtual Machines](#what-about-virtual-machines)

But what are containers really?  
To answer this let's start with the images!

> Note: the *host* is your computer, the system on which you develop

### images
A Docker image is **litterally** a picture of a system/an environment/an OS.
It's like taking a snapshot of it!
Thus, you only have to build the smallest snapshot that run your application for example:  
For a python application, you'll need `python` ofc, maybe some dependencies like `pygame` or `requests` or `discordpy` if you're building a Discord Bot!  
Every other things would be useless garbage for your application!!

Factually, to create `docker` images you write a `Dockerfile` ([[3]](#3-dockerfile-example) to get an example ;) ):
 - you base it on a base image (a python image, a debian or ubuntu classically) with the keyword `FROM`.
 - then you create the environment you need, maybe run some commands to create folders, install packages? You'll use the `RUN` keyword!
- and finally embed your source code with `COPY` copying the files from the *host* (see the *Note* above) to the images.

And there you have your image "code"!

> Note: Of course there are maaaany more keywords but this is an introduction! see a list of those in the [appendix](#4-list-of-docker-keywords).

The only thing you need know is to "build" your image, it's quite analog to compilation (you know `gcc` for the C language?).
Run `docker build --file Dockerfile .` and then you'll be able to see your newly created image with `docker images`!!

### containers
Containers are nothing more than a running environment/application!

Once you have **built** your image, you can **run** your container.  
There are many things that are configured at the container level (meaning when you **run** it, not when you **build** the image), such as:
 - ports *(to interact with other services or Internet for a website)*
 - volumes *(to share data with the host)*
 - environment files/variables to configure your application
 - ...see the [list in appendix](#5-list-of-docker-run-options) for a longer list

Use `docker run <image name>` (get the `<image name>` with `docker images`) to run/start a container!
As previously said you can pass various flags and options but you'll see later.
And just like that you've run your container/application!  
You can see it using `docker ps --all`.
Alternatively you can use a `docker-compose.yml` file but we'll maybe see it in another blog post, in a nutshell they are to containers what `Dockerfile`s are to image: a configuration file.

## Appendix

#### 1 [Why Docker?](https://www.docker.com/why-docker/)  
#### 2 [Linux Containers](https://docs.docker.com/engine/faq/#what-does-docker-technology-add-to-just-plain-lxc)  
#### 3 [Dockerfile example](https://github.com/iScsc/iscsc.fr-blog-notify/blob/main/Dockerfile)  
#### 4 [List of Docker keywords](https://dockerlabs.collabnix.com/docker/cheatsheet/)
(Dockerfile section); full doc [here](https://docs.docker.com/engine/reference/builder/)  
#### 5 [List of `docker run` options](https://docs.docker.com/engine/reference/commandline/run/#options)  

### What about Virtual Machines
Yes the question is interesting, what differentiate a container from a VM? Why don't we use VMs to isolate our services?

Googling (Ecosiating???) it shows [dozens of results](https://www.ecosia.org/search?q=containers%20vs%20vms&addon=firefox&addonversion=4.1.0&method=topbar) but I'll try to summarize it/give my own.

First point: VMs are way heavier than containers, and this could be a sufficient argument not to use VMs everywhere.  
But the real reason why they are heavier is because **they also abstract the kernel and the OS, while containers don't** (remember they are build **upon** Linux Containers).  
Here is a good representation of it:  
![image is down :( contact me to update it: Clement#9318 on Discord](https://iot.samteck.net/wp-content/uploads/2018/10/vm-vs-docker.jpg)(https://www.ecosia.org/images?q=containers%20vs%20vms#id=705E42FE3FFFCED8FFB0312D1D224BB193BAEC60)

So containers are a **sort of** lighter VMs, but they are under the hood reeaaaaally different, this is a simplified view!

> note however that VMs are used to containers environment because they provide a better security layer separating guest OS from host OS, for example when I do cybersecurity I use a VM, and when you rent a server to AWS or OVH you're given access to a VM running on bigger servers
