import aiohttp
from graphqlclient import GraphQLClient

class GraphQLClientWrapper:
    def __init__(self, endpoint: str):
        self.client = GraphQLClient(endpoint)

    async def fetch_data(self, query: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.client.endpoint, json={'query': query}) as response:
                return await response.json()
