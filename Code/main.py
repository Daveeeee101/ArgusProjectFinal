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
import Logging


async def main():
    async with OpenseaSession() as sess:
        out = await sess.sendEventPollHistoryRequest(OpenSeaEventHistoryPollQuery().collections(['cryptopunks']))
        print(out)


if __name__ == '__main__':
    asyncio.run(main())
