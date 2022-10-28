from OpenSeaDataClasses import OpenSeaCollection
from OpenSeaDataClasses import OpenSeaAsset
from OpenSeaDataClasses import OpenSeaEvent
from typing import Set
from typing import List


class Collection:

    def __init__(self, data: OpenSeaCollection, assetsListed: Set[OpenSeaAsset]):
        self.data: OpenSeaCollection = data
        self.assetsListed: Set[OpenSeaAsset] = assetsListed
        self.eventsHistory: List[OpenSeaEvent] = []

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data
