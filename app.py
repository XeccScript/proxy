import requests
from flask import Flask, request, Response

app = Flask(__name__)

PROXY_TARGET = "http://213.142.135.46:9999"

@app.before_request
def before_request():
    # Maintain full path with query string if present
    url = f"{PROXY_TARGET}{request.full_path if request.query_string else request.path}"

    # Filter headers (Host should not be forwarded)
    headers = {key: value for key, value in request.headers if key.lower() != "host"}

    try:
        # Forward request to target server
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        )
    except requests.RequestException as e:
        return Response(f"Upstream error: {str(e)}", status=502)

    # Build response
    response = Response(resp.content, status=resp.status_code)
    excluded_headers = {"content-encoding", "transfer-encoding", "content-length"}
    for key, value in resp.headers.items():
        if key.lower() not in excluded_headers:
            response.headers[key] = value

    return response

if __name__ == "__main__":
    app.run(debug=True)

