import aiohttp
from OpenseaRequests import OpenSeaRequest
from OpenseaRequests import OpenSeaEventHistoryPollQuery
from OpenseaResponse import OpenseaEventHistoryPollResponse
from OpenseaRequests import OpenSeaOrdersQuery
from OpenseaResponse import OpenSeaOrderResponse
from OpenseaRequests import OpenSeaOrderActivityQuery
from OpenseaResponse import OpenSeaOrderActivityResponse


class OpenseaSession:
    """Class for the handling of sending and receiving http requests and responses to opensea"""
    URL = "https://api.opensea.io/graphql/"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.sess.close()

    def __init__(self):
        self.sess = aiohttp.ClientSession()

    async def close(self):
        await self.sess.close()

    async def sendRequest(self, req: OpenSeaRequest) -> str:
        """sends a request to opensea and returns the string result"""
        async with self.sess.post(self.URL, data=req.getBody(), headers=req.header) as resp:
            text_response = await resp.text()
            return text_response

    async def sendEventPollHistoryRequest(self, req: OpenSeaEventHistoryPollQuery) -> OpenseaEventHistoryPollResponse:
        text = await self.sendRequest(req)
        return OpenseaEventHistoryPollResponse(text)

    async def sendOrderRequest(self, req: OpenSeaOrdersQuery) -> OpenSeaOrderResponse:
        text = await self.sendRequest(req)
        return OpenSeaOrderResponse(text)

    async def sendOrderActivityRequest(self, req: OpenSeaOrderActivityQuery) -> OpenSeaOrderActivityResponse:
        text = await self.sendRequest(req)
        return OpenSeaOrderActivityResponse(text)
