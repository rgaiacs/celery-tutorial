# Celery Tutorial

My study notes of [Celery](https://github.com/celery/celery)'s [Getting Started](https://docs.celeryq.dev/en/stable/getting-started/index.html).

## Usage

```bash
docker compose up
```

```bash
curl http://localhost:5000
```

```
{
  "status": "OK"
}
```

```bash
curl -X POST http://localhost:5000/tasks/add -d "a=1&b=1"
```

```
{
  "result_id": "3500b5a8-7b1c-4d8f-9663-b4861aadb05a"
}
```

```bash
curl http://localhost:5000/tasks/result/3500b5a8-7b1c-4d8f-9663-b4861aadb05a
```

```
{
  "ready": true,
  "successful": true,
  "value": 2
}
```