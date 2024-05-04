---
title: "Use Docker's bind mounts to build a persistent log system"
summary: "Persist data after container's death and share data with the host or accross containers through Docker's bind mounts feature"
date: 2023-09-19T12:00:00+0200
lastUpdate: 2024-05-03T20:00:00+0200
tags: ["docker", "volume", "log"]
author: FireFrozen
draft: false
---

Before reading this article, it's recommended to have a minimum knowledge of `docker`.  
See, for example, the previous blog on docker: [Get Started with Docker](https://iscsc.fr/posts/short-docker-introduction/) by `ctmbl`.



## A brief disclaimer

Note that in Docker, **two ways exist to persist/share data** with the host: **volumes** and **bind mounts**.  
While some key differences exist between both, they are not relevant in most of our basic use cases.  
We'll then **not distinguish one from the other**, some of what we say might better applied to bind mounts but **we'll only speak of volumes**.  
For more information see [Manage data in Docker](https://docs.docker.com/storage/).

## What is a Docker's bind mount?

A docker's bind mount is the action of **mounting an existing file or directory** of the host (the computer running the container) **into a container**. To rephrase, it enables a container to **share a memory space with the host**. So both the container and the user can access and modify it in real time and because it's not "contained" in the container but only mounted, it'll **persist after the container's death**.

## Why do we need bind mounts?

Docker containerization is very useful on lots of points for development but it's very annoying if your application **needs to produce persistent data**, like logs. Indeed if you **kill** your container (to update it for example) or if it **crashes**, you **lose everything that was inside** and understanding why your application crashed without its logs can be very complicated or even impossible.

So we need to find a way to **keep certain files after the container's death** and that can be **achieved with bind mounts**!.

## How to create a bind mount?

To create a bind mount, you need to add a specific argument to the `docker run` command *([similar syntax](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes) exists for `docker-compose.yml`)*.

TO BE DELETED: > You can also create volumes outside of containers with [`docker volume`](https://docs.docker.com/storage/volumes/#create-and-manage-volumes)

There is two different arguments which are really similar in their use. Those are `--mount` and `--volume`, both can be used to create bind mounts (but volumes too, see [Disclaimer](#a-brief-disclaimer) above).  
However they slightly differ: if you enter a non existing file to mount, `--volume` will create it when `--mount` will return an error, also `--volume` needs fewer arguments. For these reason and because we focused on simplicity in this post we'll describe the `--volume` argument. 

The exact syntax is:
```bash
docker run <other args> --volume PATH_TO_HOST_FILE:PATH_TO_CONTAINER_FILE:<optional args>
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

## Other important use cases of bind mounts

> See [Bind mounts use cases](https://docs.docker.com/storage/#good-use-cases-for-bind-mounts)

* The same volume can be shared by multiple containers.  
  It can be useful if you want to share a database with applications running on different containers or to centralized logs of multiple application in the same log file/folder.
* In development you can use bind mounts to share code with the container (where it runs) while editing it in your IDE in the host.

## Resources to go further

TO BE REWORKED:

- [Key differences between volumes and bind mounts](https://docs.docker.com/storage/#volumes)
  - [Differences between `--volume` and `--mount`](https://docs.docker.com/storage/bind-mounts/#differences-between--v-and---mount-behavior)
  - [Volumes use cases](https://docs.docker.com/storage/#good-use-cases-for-volumes)
  - [Bind mounts use cases](https://docs.docker.com/storage/#good-use-cases-for-bind-mounts)
- [`docker volume` syntax](https://docs.docker.com/storage/volumes/#create-and-manage-volumes)
- [Volumes in Docker compose file](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes)