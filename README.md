# blog.iscsc.fr: a blog built with HUGO framework

TODO pour cette PR: virer le todo à la fin et mettre les features


## TODO
Non-exhaustive TODO-list:
 - [X] write a workflow that prevents merging if website doesn't build
 - [X] fix nginx.conf and run_nginx.sh properly
 - [X] Add automatic deployment on push to src/**
 - [ ] write a workflow warning if the new content is still draft
 - [X] add https
 - [X] add posts from previous website
 - [ ] add a comments engine
 - [X] fix baseUrl and "iScsc" sidebar brand name not redirecting
 - [ ] print a `lastUpdate` or `updated` date param on posts
 - [X] show posts which `draft` param is `true` in dev mode (if possible)
 - [ ] check when building (with builder target) that git submodule is updated


## Features
- renders emojis https://emojibase.dev/shortcodes/?

## NOTES:
- possible other choices for themes, other than git submodules: HUGO modules
  - at least remove useless empty folders
- hugo docker image: custom image rather than klakegg one's: more control over hugo's version 


## Deployment

### Production

#### Create SSL certification

To set up HTTPS, you will need valid SSL certificates. If you deploy the app for the first time, follow these instructions:

- Comment or delete the whole server section about 443 in the `nginx.conf` file.

```diff
- server {
- listen 443 default_server ssl http2;
- ...
- }
```

> This step is required because the certificates don't exist yet, so they cannot be loaded in the nginx configuration.  
> **The website has to run with http to respond to certbot challenge**

- (Re)Start the `blog` container:

```bash
docker compose up --detach --build blog
```

- Create the certificates with the `certbot` container:

```bash
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d yourdomainname.com
```

- Restore the original `nginx.conf` (with `git restore nginx.conf` for example)
- Stop the `blog` container:

```bash
docker compose down
```

The certificates should have been generated in `certbot/conf/live/yourdomainname.com/`.

#### Renew SSL certification

If you just want to renew existing certificates you should use the designed script:
```bash
./scripts/renewssl.sh
```
> Note that this script uses hardcoded absolute path designed for the iScsc VPS

If you want to here are the detailed steps:
```bash
# List existing certificates
docker compose run certbot certificates
# Renew certificates
docker compose run --rm certbot renew
# Restart blog
docker compose stop blog
docker compose up --detach blog
```

#### Deploy the website itself

Create the blog/prod and blog/dev directory, **they must be writable by the user/group that will write to it: you, builder target, CI user...**
```sh
mkdir -p build/blog/prod
mkdir -p build/blog/dev
sudo chown -R <user>:<group> build/blog
sudo chmod -R g+w build/blog
```

> you should check first the consistency of the server name (iscsc.fr/localhost) in those files: `nginx.conf`, ...

Start the nginx container to serve requests:
```sh
docker compose build blog
docker compose up --detach blog
```

> Note: before the next step make sure that when cloning the repository you also fetched the git submodule!

Then build the static website, `./build/blog/prod` is a volume shared with both containers so building the website will automatically "update" it for nginx.
```sh
docker compose up builder
```

After doing this last step, files might have been created with the wrong permissions/owners (it depends if you use the setgid bit, modify the builder container, and even what YOU consider being the right permissions/owners). If needed you might re-do what we've previously:
```sh
sudo chown -R <user>:<group> build/blog
sudo chmod -R g+w build/blog
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

> it requires `hugo` [installed](https://gohugo.io/installation/) locally!
```sh
cd src
hugo server --buildDrafts --buildFuture
```
> `--buildFuture` is also used in production, `--buildDrafts` only in development  
> `--buildExpired` can be used too

This will build sources and start a basic development server that listens on http://localhost:1313.

The HUGO server **automatically watches sources**, so if you create a new post while it's running it will automatically rebuild the website and serve the new post.
