# Using bind mounts to build a persistent log system with Docker

_FireFrozen - 2023/09/19_

Before reading this article, it's recommended to have a minimum knowledge of docker. See the previous blog on docker : [Get Started with Docker](https://iscsc.fr/blog/64601d94963f4a68d30f5795) by _ctmbl_

## Why do we need bind mounts?

Docker containerization is very useful on lots of points for development but it's very annoying if your application need to produce persistent data like logs. Because if you kill your container (to update it for example) or if it crash, you lose everything that where inside and understanding why your application crashed without its logs is very complicated.

So we need to find a way to keep certain files after the container's death and that can be done with a bind mounts.

## What is a bind mounts?

A bind mounts is the action of mounting an existing file or directory of the host (the computer running the container) machine into a container. To rephrase, it enables a container to share a memory space with the host. So both the container and the user can access and modify it in real time and because it's not "contained" in the container but only mounted, it persists after container's death.

## How to make a bind mounts?

To make a bind mounts, you need to add a specific argument for the "docker run" command. There is two different arguments to make a bind mounts which are really similar in their uses. Those are "--mount" and "--volume". Both can be used to make bind mounts or to create volumes (more advanced way to create and use persistent data with docker). For the bind mounts part, they only differs in one behavior : if you enter a non existing file to mount, "--volume" will create it when "--mount" will return an error. Moreover "--volume" needs less arguments so that's the solution I'm going to describe here.

The exact syntax is :

```
docker run (other args) --volume PATH_TO_HOST_FILE:PATH_TO_CONTAINER_FILE:(optional args)
```

* Note that you can use "-v" instead of "--volume" to make it shorter.
* Note that you can use mount a directory instead of a file with the same method (just replace PATH_TO_xxx_FILE with the PATH_TO_xxx_DIRECTORY)

Optional args must be separated by comas, they are not used very often but lets detail the most useful one quickly :
* ro : if used, the mounts will be in read only mode for the containers.

Concrete example with the code of the site bot:
```
HOST_LOG_FILE=$(realpath -P ${LOG_FILE})

[...]

docker run --detach --rm --interactive --tty \
    --name ${NAME} \
    --volume ${HOST_LOG_FILE}:/opt/iscsc.fr-notify-bot/${LOG_FILE} \
    ${NAME}:latest
```
In this example LOG_FILE is a environment variable defined in the .env

> **WARNING : Be careful that the bot/application running in the container have the right permission to modify the file/directory**

## Other utility of bind mounts

* The same volume can be shared by multiple containers. It can be useful if you want to share a database with applications running on different containers or to centralized logs of multiple application in the same log file.
* In development you can use bind mount to enable code modification of the application without having to restart the container.