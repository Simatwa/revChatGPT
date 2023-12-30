from flask import Blueprint

app = Blueprint(
    "allinone",
    __name__,
)

modded_headers = {
    #'Date': 'Wed, 27 Dec 2023 18:50:08 GMT',
    "Content-Type": "text/event-stream; charset=utf-8",
    "Transfer-Encoding": "chunked",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    # "set-cookie": 'uasid="some-cookies-here',
    "access-control-allow-credentials": "true",
    "access-control-allow-origin": "http://localhost:8000",
    "vary": "Origin",
    "x-envoy-upstream-service-time": "916",
    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
    "CF-Cache-Status": "DYNAMIC",
    "Report-To": '{"endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report\\/v3?s=some-long-values-were-here"}],"group":"cf-nel","max_age":604800}',
    "NEL": '{"success_fraction":0.01,"report_to":"cf-nel","max_age":604800}',
    "X-Content-Type-Options": "nosniff",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Robots-Tag": "nofollow",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'nonce-some-values-here' 'unsafe-inline' 'unsafe-eval'",
    "Server": "cloudflare",
    # "alt-svc": 'h3=":443"; ma=86400',
}
