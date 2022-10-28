from typing import Dict
from Event import Event
from OpenSeaDataClasses import *
from Account import Account
from Collection import Collection
from Asset import Asset


class OpenSeaManager:

    def __init__(self):
        self.eventDict: Dict[OpenSeaEvent, Event] = {}
        self.accountDict: Dict[OpenSeaAccount, Account] = {}
        self.collectionDict: Dict[OpenSeaCollection, Collection] = {}
        self.assetSet: Dict[OpenSeaAsset, Asset] = {}



