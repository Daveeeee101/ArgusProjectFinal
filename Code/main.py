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
    async with OpenseaSession() as sess:
        request = OpenSeaFloorHistoryQuery().collection('steady-stack-titans-official').startDate("2022-06-26T00:00:00+00:00")
        out = await sess.sendRequest(request)
        print(out)


if __name__ == '__main__':
    asyncio.run(main())
