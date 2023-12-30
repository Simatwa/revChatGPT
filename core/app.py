from flask import Flask, request, jsonify, render_template, Response
from WebChatGPT import ChatGPT
from functools import wraps
from json import dumps, loads
import logging

application = Flask(
    __name__,
    static_folder="static/openai/_next/static",
    static_url_path="/_next/static",
    template_folder="templates",
)

application.config.from_pyfile("config.py")

indentation_level = application.config["INDENTATION_LEVEL"]

hunter = logging.getLogger(application.config["LOGGER_NAME"])
hunter.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(application.config["LOGGING_FILE"])
file_handler.setLevel(application.config["LOGGING_LEVEL"])

formatter = logging.Formatter(
    "%(asctime)s - %(name)s : %(levelname)s - %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S (%s)",
)
file_handler.setFormatter(formatter)

hunter.addHandler(file_handler)


openai = ChatGPT(
    application.config["OPENAI_COOKIE_FILE"],
)

chatgpt_site = "https://chat.openai.com"


class Payload:
    @staticmethod
    def get_payload():
        if request.method == "GET":
            resp = request.args.to_dict()
        else:
            if request.is_json:
                resp = dict(request.json)
            else:
                resp = dict(request.form)

        hunter.info(
            f"PAYLOAD - {request.method} - {request.full_path} - {dumps(resp, indent=indentation_level)}"
        )
        return resp


def format_response(func):
    """Decorator - formats response as required  - `requests` objects"""

    @wraps(func)
    def main(*args, **kwargs):
        resp = func(*args, **kwargs)
        content_type = resp.headers.get("content-type")
        data = resp.text
        try:
            hunter.info(
                f"RESPONSE - {request.method} - {request.full_path} - {dumps(loads(data), indent=indentation_level) if 'json' in content_type else data } "
            )
        except:
            pass
        return Response(
            data,
            content_type=content_type,
            status=resp.status_code,
        )

    return main


@application.route("/")
def index():
    hunter.info("Serving Index")
    return render_template("index.html", user_auth=dumps(openai.auth))
