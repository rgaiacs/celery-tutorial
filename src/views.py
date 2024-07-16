import json
import time

from celery.result import AsyncResult

from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response

import tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.get("/result/<id>")
def result(id):
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


def poll_result(id):
    result = AsyncResult(id)

    while result.status in ["PENDING", "STARTED"]:
        data = {"status": result.status}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(5)

        # Update for while
        result = AsyncResult(id)

    if result.status == "SUCCESS":
        data = {"status": result.status, "result": result.result}
        return f"data: {json.dumps(data)}\n\n"
    else:
        data = {"status": result.status}
        return f"data: {json.dumps(data)}\n\n"


@bp.get("/sse/<id>")
def result_sse(id):
    return Response(poll_result(id), mimetype="text/event-stream")


@bp.post("/add")
def add():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = tasks.add.delay(a, b)
    return {"result_id": result.id}


@bp.post("/all")
def all():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = tasks.all.delay(a, b)
    return {"result_id": result.id}
