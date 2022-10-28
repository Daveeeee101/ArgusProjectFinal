import time
from typing import Dict
from Event import Event
from OpenSeaDataClasses import *
from Account import Account
from Collection import Collection
from Asset import Asset
from OpenseaSession import OpenseaSession


class OpenSeaManager:

    def __init__(self):
        self.eventDict: Dict[OpenSeaEvent, Event] = {}
        self.accountDict: Dict[OpenSeaAccount, Account] = {}
        self.collectionDict: Dict[OpenSeaCollection, Collection] = {}
        self.assetDict: Dict[OpenSeaAsset, Asset] = {}
        self.session = OpenseaSession()
        self.lastEventUpdate = time.time()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def close(self):
        await self.session.close()










