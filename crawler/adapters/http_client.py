import httpx

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}


def build_client(**kwargs) -> httpx.AsyncClient:
    headers = {**DEFAULT_HEADERS, **kwargs.pop("headers", {})}
    return httpx.AsyncClient(timeout=30.0, headers=headers, **kwargs)
