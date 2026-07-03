# gateway/app/main.py
#
# Gateway/router mínimo del ejercicio Strangler Fig: toda ruta que
# empieza con /catalog se desvía al catalog-service nuevo (8001);
# cualquier otra ruta sigue yendo al monolito viejo (8000), intacto.

import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI(title="Mercaloop Gateway")

CATALOG_SERVICE_URL = "http://localhost:8001"
MONOLITH_URL = "http://localhost:8000"

client = httpx.AsyncClient()

# Headers que no deben reenviarse tal cual (son específicos de la
# conexión hop-by-hop, no del contenido de la respuesta/petición).
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
    "host",
}


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}


@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
async def proxy(full_path: str, request: Request):
    if full_path.startswith("catalog"):
        target_base = CATALOG_SERVICE_URL
    else:
        target_base = MONOLITH_URL

    target_url = f"{target_base}/{full_path}"

    forward_headers = {
        k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS
    }
    body = await request.body()

    upstream_response = await client.request(
        method=request.method,
        url=target_url,
        params=request.query_params,
        headers=forward_headers,
        content=body,
    )

    response_headers = {
        k: v
        for k, v in upstream_response.headers.items()
        if k.lower() not in HOP_BY_HOP_HEADERS
    }

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
        media_type=upstream_response.headers.get("content-type"),
    )
