from core.allinone import app
from core.allinone import modded_headers
from core.app import application
from flask.views import MethodView
from flask import request
from flask import Response
from flask import jsonify
from core.app import Payload
from core.app import format_response
from core.app import chatgpt_site
from core.app import openai
from core.app import hunter
from core.app import dumps
from core.app import indentation_level
from os import path


class ApiTemplate(MethodView, Payload):
    init_every_request = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_url = lambda: chatgpt_site + request.path

    @format_response
    def get(self, **kwargs):
        params = self.get_payload()
        resp = openai.session.get(
            self.get_url(),
            params=params,
        )
        return resp

    @format_response
    def post(self, **kwargs):
        json = self.get_payload()
        resp = openai.session.post(
            self.get_url(),
            json=json,
        )
        return resp

    @format_response
    def patch(self, **kwargs):
        json = self.get_payload()
        resp = openai.session.patch(
            self.get_url(),
            json=json,
        )
        return resp

    @format_response
    def delete(self, **kwargs):
        json = self.get_payload()
        resp = openai.session.delete(
            self.get_url(),
            json=json,
        )
        return resp


class AllInOne(ApiTemplate):
    decorators = []  # Implement verification here if you find a need

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GenerateResponse(MethodView, Payload):
    methods = ["POST"]

    init_every_request = True

    def post(self):
        json = self.get_payload()
        # print(json) Capture the payload to be sent from here

        def stream_content():
            response = openai.session.post(
                url=openai.conversation_endpoint,
                json=json,
                timeout=60,
                stream=True,
            )
            hunter.info(
                f"CONVERSATION - ({response.status_code}, {response.reason}) - {dumps(dict(response.headers), indent=indentation_level)}"
            )
            hunter.debug(
                f"TEXT - {dumps(response.json(), indent=indentation_level) if 'json' in response.headers.get('Content-Type','') else '<SUCCESS>'}"
            )
            if (
                response.ok
                and response.headers.get("content-type")
                == "text/event-stream; charset=utf-8"
            ):
                for count, value in enumerate(
                    response.iter_lines(
                        decode_unicode=True,
                    )
                ):
                    hunter.debug(f"YIELD - ({count}) - {value}")
                    yield value + "\r\n"  # Removing the Carriage Return (\r) and Line feed (\n) will make browser rendering to fail.

        return Response(
            stream_content(),
            status=200,
            content_type="text/event-stream; charset=utf-8",
            # headers=modded_headers,
        )


class Auth(ApiTemplate):
    def get(self):
        return jsonify(openai.auth)


app.add_url_rule("/api/auth/session", view_func=Auth.as_view("auth"))
app.add_url_rule(
    "/backend-api/conversation", view_func=GenerateResponse.as_view("conversation")
)
app.add_url_rule("/<path:openai_endpoint>", view_func=AllInOne.as_view("openai"))
