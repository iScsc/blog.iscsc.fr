# blog.iscsc.fr: a blog built with HUGO framework

## TODO
Non-exhaustive TODO-list:
 - [X] write a workflow that prevents merging if website doesn't build
 - [X] fix nginx.conf and run_nginx.sh properly
 - [X] Add automatic deployment on push to src/**
 - [ ] write a workflow warning if the new content is still draft
 - [ ] add https
 - [ ] add posts from previous website
 - [ ] add a comments engine
 - [ ] print a `lastUpdate` or `updated` date param on posts
 - [ ] show posts which `draft` param is `true` in dev mode (if possible)
 - [ ] check when building (with builder target) that git submodule is updated

## Deployment

### Production

Create the blog directory, **it must be writable by users that will write to it: you, builder target, CI user...**
```sh
mkdir build/blog
chmod <make it writable by the appropriate user/group>
chmown <make it owned by the appropriate user/group>
```

> you should check first the consistency of the server name (iscsc.fr/localhost) in those files: `nginx.conf`, ...

Start the nginx container to serve requests:
```sh
docker compose build blog
docker compose up --detach blog
```

> Note: before the next step make sure that when cloning the repository you also updated the git submodule!

Then builds the static website, `./build/blog` is a volume shared with both containers so 
building the website will automatically "update" it for nginx.
```sh
docker compose up builder
```

### Automatic deployment
The repository contains a GitHub Actions which automatically:
 1. **builds the website**: allow to check that nothing is broken, publish an artifact which can be downloaded or reused
 2. IF push to main AND `src/*` modified, **deploys the build**: download the artifact, create and setup ssh key, send build to server through ssh (with `rsync`)

This requires a server (a VPS) ready to receive the build *(and to be useful, running a http server serving this build)*, and, of course, to set some mandatory GitHub secrets (ssh key, CI username on server, path,...).


Sources I used:
- [Scott W. Harden's tuto](https://swharden.com/blog/2022-03-20-github-actions-hugo/)
- [HUGO deocumentation](https://gohugo.io/hosting-and-deployment/deployment-with-rsync/)
- [GitHub Actions documentation](https://docs.github.com/en/actions/learn-github-actions/contexts#steps-context)

### Development

```sh
cd src
hugo server
```
> it requires `hugo` installed locally!

This will build sources and start a basic development server that listens on http://localhost:1313.  
The HUGO server automatically watches sources, so if you create a new post while it's running it will automatically rebuild the website and serve the new post.
