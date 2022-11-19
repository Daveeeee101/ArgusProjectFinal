import asyncio
import logging
import time

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
from OpenseaRequests import OpenSeaInactiveOrders
from OpenseaRequests import OpenSeaManagerOrders
from OpenseaRequests import CancelOrdersBulk
from OpenseaRequests import BulkPurchaseQuery
from OpenseaRequests import AssetSort
from OpenseaResponse import NodeConversionException
from OpenSeaManager import OpenSeaManager


async def main():
    collection = "otherdeed"
    async with OpenseaSession() as sess:
        out = await sess.sendRequest(OpenSeaEventHistoryPollQuery().eventTypes([EventTypes.CREATED, EventTypes.SUCCESSFUL, EventTypes.CANCELLED]).collections([collection]).count(1))
        print(out)

if __name__ == '__main__':
    asyncio.run(main())
