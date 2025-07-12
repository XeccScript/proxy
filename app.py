import requests

TARGET_BASE_URL = "http://203.160.182.100:9999"

def handler(request):
    try:
        url = TARGET_BASE_URL + request.path
        headers = dict(request.headers)
        method = request.method
        data = request.body if method in ["POST", "PUT", "PATCH"] else None

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        return {
            "statusCode": response.status_code,
            "headers": {
                "Content-Type": response.headers.get("Content-Type", "text/plain")
            },
            "body": response.text
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Proxy error: {str(e)}"
        }
      
