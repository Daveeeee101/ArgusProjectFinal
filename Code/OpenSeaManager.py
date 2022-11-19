import time
from typing import Dict
from typing import List
from Event import Event
from OpenSeaDataClasses import *
from Account import Account
from Collection import Collection
from Asset import Asset
from OpenseaSession import OpenseaSession
from OpenseaRequests import OpenSeaEventHistoryPollQuery, InferredEventTypes
from OpenseaRequests import EventTypes


class OpenSeaManager:

    def __init__(self):
        self.eventDict: Dict[OpenSeaEvent, Event] = {}
        self.accountDict: Dict[OpenSeaAccount, Account] = {}
        self.collectionDict: Dict[OpenSeaCollection, Collection] = {}
        self.assetDict: Dict[OpenSeaAsset, Asset] = {}
        self.session = OpenseaSession()
        self.lastEventUpdateDict = {
            EventTypes.CREATED: time.time(),
            EventTypes.CANCELLED: time.time(),
            EventTypes.SUCCESSFUL: time.time()
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def close(self):
        await self.session.close()

    def setUpdateTimeTestMethod(self, t: int):
        self.lastEventUpdateDict[EventTypes.CREATED] = t
        self.lastEventUpdateDict[EventTypes.CANCELLED] = t
        self.lastEventUpdateDict[EventTypes.SUCCESSFUL] = t

    def addNewCollectionTestMethod(self, collectionSlug: str):
        newData = OpenSeaCollection(collectionSlug, collectionSlug, "")
        self.collectionDict[newData] = Collection(newData, set())

    def getCollectionSlugs(self) -> List[str]:
        return [openSeaColl.slug for openSeaColl in self.collectionDict]

    def getListedAssetsIter(self, collectionSlug: str):
        return (asset for asset in self.assetDict.values()
                if asset.isListed and asset.data.collection.slug == collectionSlug)

    def inferEventType(self, event: OpenSeaEvent) -> InferredEventTypes:
        if event.type == EventTypes.SUCCESSFUL:
            if event.asset not in self.getListedAssetsIter(event.getCollectionInfo().slug):
                return InferredEventTypes.INVALID
            else:
                return InferredEventTypes.SOLD
        elif event.type == EventTypes.CREATED:
            if event.asset in self.getListedAssetsIter(event.getCollectionInfo().slug):
                return InferredEventTypes.RELISTED
            else:
                return InferredEventTypes.LISTED
        elif event.type == EventTypes.CANCELLED:
            return InferredEventTypes.DELISTED

    async def getEventsSinceLastQuery(self) -> List[Event]:
        """Gets the events from the last time this method was queried. Is also responsible for correctly updating
           the event times based on the response"""
        out = []
        for key, value in self.lastEventUpdateDict.items():
            query = OpenSeaEventHistoryPollQuery()\
                    .collections(self.getCollectionSlugs())\
                    .eventTypes(key)\
                    .fromTime(datetime.fromtimestamp(value))
            response = await self.session.sendEventPollHistoryRequest(query)
            """get the last event time"""
            outList = response.toOpenSeaEventList()
            if outList:
                lastResponse = outList[0]
                unixTime = lastResponse.timestamp.timestamp()
                self.lastEventUpdateDict[key] = unixTime
            out += [Event(evt, inferredType=self.inferEventType(evt)) for evt in outList]
        return out

    async def updateFromOpenSea(self):
        # 1) Get event history data from poll query
        newEvents = await self.getEventsSinceLastQuery()
        # 2) Validate with asset data sorted by sales/listings

        # 3) Do some other bullshit to update account info
        # 4) Update relations between dictionaries











