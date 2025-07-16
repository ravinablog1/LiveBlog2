from fastapi import FastAPI, HTTPException
import httpx
import asyncio

app = FastAPI(title="LiveBlog API Gateway")

# Service URLs
USER_SERVICE_URL = "http://user-service:8000"
LIVEBLOG_SERVICE_URL = "http://liveblog-service:8000"
NOTIFICATION_SERVICE_URL = "http://notification-service:8000"

@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_user_service(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{USER_SERVICE_URL}/api/users/{path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=await request.body()
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

@app.api_route("/api/liveblog/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_liveblog_service(path: str, request: Request):
    # Similar proxy logic for liveblog service
    pass