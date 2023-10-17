# blog.iscsc.fr: a blog built with HUGO framework

## TODO
Non-exhaustive TODO-list:
 - print a `lastUpdate` or `updated` date param on posts
 - show posts which `draft` param is `true` in dev mode (if possible)
 - add a comments engine

## Deployment

### Production

> you should check first the consistency of the server name (iscsc.fr/localhost) in those files:
- Dockerfile
- nginx.conf
- src/config.toml (if needed)
- .env.prod (if used)

Start the nginx container to serve requests:
```
docker-compose build blog
docker-compose up blog --detach
```

Then builds the static website, ./build/blog is a volume shared with both containers so 
building the website will automatically "update" it for nginx.

### Development

```
cd src
hugo server
```