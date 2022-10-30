import asyncio
import logging
from OpenseaSession import OpenseaSession
from OpenseaRequests import EventTypes
from OpenseaRequests import OpenSeaEventHistoryPollQuery
from OpenseaRequests import OpenSeaOrdersQuery
from OpenseaRequests import Chains
from OpenseaRequests import OpenSeaOrderActivityQuery
from OpenseaRequests import OpenSeaAssetQuery
from OpenseaRequests import OpenSeaSelectAssetQuery
from OpenseaRequests import OpenSeaCollectionActivityQuery
from OpenseaRequests import OpenSeaPriceHistoryQuery
from OpenseaRequests import OpenSeaFloorHistoryQuery
import Logging


async def main():
    nftAddress = "0x495f947276749ce646f68ac8c248420045cb7b5e"
    tokenId = 105459361334571136243493281122501276861891817147204613658540988352430499430401
    async with OpenseaSession() as sess:
        request1 = OpenSeaEventHistoryPollQuery().eventTypes(EventTypes.CREATED).nft(tokenId, nftAddress).count(10)
        out1 = await sess.sendEventPollHistoryRequest(request1)
        request2 = OpenSeaOrdersQuery().nft(tokenId, nftAddress).count(10)
        out2 = await sess.sendOrderRequest(request2)
        print(out1)
        print("\n")
        print(out2)


if __name__ == '__main__':
    asyncio.run(main())
