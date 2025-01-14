import httpx

class MessageRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_messages(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            return data.get("messages", [])
