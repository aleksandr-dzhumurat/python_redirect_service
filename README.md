# python_redirect_service

Build docker

```shell
make build
```

Rename `.env.template` to `.env`

Replace `SHORTENER_PREFIX` in `.env` to actual service url

```shell
SHORTENER_PREFIX=http://127.0.0.1:8000/
```

Run service

```shell
make run
```

Test service
```shell
curl -X POST -H "Content-Type: application/json" -d '{"source_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' http://127.0.0.1:8000/add
```

Visualize links
```shell
http://127.0.0.1:8000/explore
```