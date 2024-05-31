import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class GraphQLClientWrapper:
    def __init__(self, endpoint: str):
        self.transport = AIOHTTPTransport(url=endpoint)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def fetch_data(self, query: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.transport.url, json={'query': query}) as response:
                return await response.json()
