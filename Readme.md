# Staff Promotion API

## Build Docker Image

```
docker build -t staff-promotion-api .
```

## Run Docker Image
```
docker run -p 9000:80 -e PORT=80 -e API_KEY="xxxx" staff-promotion-api
```