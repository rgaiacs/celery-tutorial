import json
import time

from celery.result import AsyncResult

from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response
from flask import stream_with_context

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


# To debug,
#
# @stream_with_context
# def poll_result(id):
#     current_app.logger.error(result)
@stream_with_context
def poll_result(id):
    # This is a generator and yield should be used to return data
    result = AsyncResult(id)

    while result.state != "SUCCESS":
        data = {"state": result.state, "info": result.info}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

        # Update for while
        result = AsyncResult(id)
        current_app.logger.error(result.parent)

    if result.state == "SUCCESS":
        data = {"state": result.state, "info": result.info, "result": result.result}
        yield f"data: {json.dumps(data)}\n\n"
    else:
        data = {"state": result.state}
        yield f"data: {json.dumps(data)}\n\n"

    # Connection ends here.


@bp.get("/sse/<id>")
def result_sse(id):
    return Response(poll_result(id), mimetype="text/event-stream")


@bp.post("/mul")
def mul():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = tasks.mul.delay(a, b)
    return {"result_id": result.id}


@bp.post("/all")
def all():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    lazy_chain = tasks.all(a, b)
    result = lazy_chain.apply_async()
    return {"result_id": result.id}
