from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, base_url: str, cookies: str):
        self._session = ClientSession(
            base_url=base_url,
            cookies=cookies
        )

class BuffHTTPClient(HTTPClient):
    async def parse_page(self, page_num: int, category: str):
        async with self._session.get(f"/api/market/goods?game=csgo&category={category}&page_num={page_num}") as resp:
            result = await resp.json()
            return result