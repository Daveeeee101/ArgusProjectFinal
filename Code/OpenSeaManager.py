from typing import Set
from Event import Event
from Account import Account
from Collection import Collection
from Asset import Asset


class OpenSeaManager:

    def __init__(self):
        self.eventSet: Set[Event] = set()
        self.accountSet: Set[Account] = set()
        self.collectionSet: Set[Collection] = set()
        self.assetSet: Set[Asset] = set()

