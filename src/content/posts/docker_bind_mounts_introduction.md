---
title: "Use Docker's bind mounts to build a persistent log system"
summary: "Persist data after container's death and share data with the host or accross containers through Docker's bind mounts feature"
date: 2023-09-19T12:00:00+0200
lastUpdate: 2024-05-03T20:00:00+0200
tags: ["docker", "volume", "bind mounts", "logs"]
author: FireFrozen
draft: false
---

*Co-Authored with [ctmbl](https://iscsc.fr/author/ctmbl/)*

Before reading this article, it's recommended to have a minimum knowledge of `docker`.  
See, for example, the previous blog on docker: [Get Started with Docker](https://iscsc.fr/posts/short-docker-introduction/) by `ctmbl`.

Also I **strongly** recommend you to read [the Disclaimer](#a-brief-disclaimer).

## A brief disclaimer

**TLDR**:  
Volumes and bind mounts aren't the same thing.  
We can **confuse `--volume` and `--mount`** BUT **we can't** confuse the **concepts of volumes and bind mounts**.  
Volumes aren't only managed by `--volume`, bind mounts aren't only managed by `--mount`.  

This article addresses the concept of bind mounts.

---

In Docker, two ways exist to persist/share data: **volumes** (named and anonymous) and **bind mounts**.  

What we're talking about in this blog aren't volumes at all, they are bind mounts.  
We'll name them *bind mounts* **but be aware that** often on Internet you'll encounter the word *volume* while the author is actually speaking of a bind mount.  
This is certainly due to the fact that **options `--volume` and `--mount` can be used almost interchangeably**.  

> Even in [docker's doc the naming is confusing](https://docs.docker.com/storage/volumes/#differences-between--v-and---mount-behavior)

Key differences exist between bind mounts and volumes, for more information see [Manage data in Docker](https://docs.docker.com/storage/).

## What is a Docker's bind mount?

A docker's *bind mount* is the action of **mounting an existing file or directory** of the host (the computer running the container) **into a container**. To rephrase, it enables a container to **share a memory space with the host**. So both the container and the user can access and modify it in real time and because it's not "contained" in the container but only mounted, it'll **persist after the container's death**.

## Why do we need bind mounts?

Docker containerization is very useful on lots of points for development but it's very annoying if your application **needs to produce persistent data**, like logs. Indeed if you **kill** your container (to update it for example) or if it **crashes**, you **lose everything that was inside** and understanding why your application crashed without its logs can be very complicated or even impossible.

So we need to find a way to **keep certain files after the container's death** and that can be **achieved with bind mounts**.

It's also interesting to notice another really good usecase for *bind mounts*: during development you can share source code to execute it within the container while editing it in your IDE in the host

## How to create a bind mount?

To create a bind mount, you need to add a specific argument to the `docker run` command *([similar syntax](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) exists for `docker-compose.yml`)*.

There is two different arguments which are really similar in their use. Those are `--mount` and `--volume`, both can be used to create bind mounts (but volumes too, see [Disclaimer](#a-brief-disclaimer) above).  
However they slightly differ: if you enter a non existing file to mount, `--volume` will create it when `--mount` will return an error, also `--volume` needs fewer arguments.  
For these reason and because we focus on simplicity in this post we'll describe the `--volume` argument. 

The exact syntax is:
```bash
docker run <other args> --volume path/in/host:path/in/container:<optional args>
```

> Note that you can use `-v` instead of `--volume`

> Note that you can mount a directory instead of a file with the same method

> A [similar syntax](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) exists for `docker-compose.yml`

Optional args must be separated by comas, they are not used very often but lets detail the most useful one quickly :
- `ro` : if used, the mounted file/folder will be in read-only mode inside the container

A concrete example with the [code of our RootMe discord bot](https://github.com/iScsc/RootPythia/blob/2681ca26286ea5063371536e995a5e3cf39734a5/run.sh#L12):
```bash
source ./.env.prod

docker run --rm --interactive --tty \
  --detach \
  --volume $(realpath -P ${LOG_FOLDER}):/opt/${NAME}/logs \
  --env-file .env.prod \
  --name ${NAME} \
  ${NAME}:latest
```
In this example `LOG_FOLDER` is an environment variable defined in the `.env.prod` file.  
The code will write transparently to `/opt/${NAME}/logs/<log file>` but because this folder is shared with the host, logs will **be available in the host** and survive potential application crashes or updates.

> **WARNING : Be careful that the bot/application running in the container must have the right permission to modify the file/directory**

## Resources to go further

About *volumes* VS *bind mounts*:
- [Manage data in Docker](https://docs.docker.com/storage/)
- [Choose the right type of mount](https://docs.docker.com/storage/#choose-the-right-type-of-mount)

About *bind mounts* specifically:
- [Start a container with a bind mount](https://docs.docker.com/storage/bind-mounts/#start-a-container-with-a-bind-mount)
- [Bind mounts use cases](https://docs.docker.com/storage/#good-use-cases-for-bind-mounts)

Other sources:
- [Volumes in Docker compose file](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes)
- https://dev.to/doziestar/a-comprehensive-guide-to-docker-volumes-4d9h
- https://www.baeldung.com/ops/docker-volumes
- [Never mess with `/var/lib/docker` docker forum](https://forums.docker.com/t/write-from-host-to-volume/47274)
- [Volumes use cases](https://docs.docker.com/storage/#good-use-cases-for-volumes)
