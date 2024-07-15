import time

from celery.result import AsyncResult
from flask import Blueprint
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
        yield f"data: {result.status}\n"
        time.sleep(5)

    if result.status == "SUCCESS":
        return f"data: {result.result}\n"
    else:
        return "data: {FAIL}\n"



@bp.get("/sse/<id>")
def result_sse(id):
    return Response(poll_result(id), mimetype='text/event-stream')


@bp.post("/add")
def add():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = tasks.add.delay(a, b)
    return {"result_id": result.id}