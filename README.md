# blog.iscsc.fr: a blog built with HUGO framework

## TODO
Non-exhaustive TODO-list:
 - [ ] print a `lastUpdate` or `updated` date param on posts
 - [ ] show posts which `draft` param is `true` in dev mode (if possible)
 - [ ] add a comments engine
 - [X] write a workflow that prevents merging if website doesn't build
 - [ ] write a workflow warning if the new content is still draft
 - [X] fix nginx.conf and run_nginx.sh properly
 - [ ] add https
 - [ ] check when building (with builder target) that git submodule is updated

## Deployment

### Production

Create the blog directory, **it must be writable by the user that will write to it: you, builder target, CI user...**
```sh
mkdir build/blog
chmown <make it writable by the appropriate user/group>
chmod <make it writable by the appropriate user/group>
```

> you should check first the consistency of the server name (iscsc.fr/localhost) in those files: `nginx.conf`, ...

Start the nginx container to serve requests:
```sh
docker compose build blog
docker compose up --detach blog
```

> Note: before the next step make sure when cloning the repository you also updated the git submodule!

Then builds the static website, `./build/blog` is a volume shared with both containers so 
building the website will automatically "update" it for nginx.
```sh
docker compose up builder
```

### Development

```
cd src
hugo server
```