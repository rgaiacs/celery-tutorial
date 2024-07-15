# Celery Tutorial

My study notes of [Celery](https://github.com/celery/celery)'s [Getting Started](https://docs.celeryq.dev/en/stable/getting-started/index.html).

## Usage

```bash
docker compose up
```

Now, you can access the Docker container using

```bash
docker compose exec -it app /bin/bash
```

```bash
cd src
```

```bash
pixi run python
```

```python
from tasks import add

result = add.delay(4, 4)

result.ready()
result.get()
```