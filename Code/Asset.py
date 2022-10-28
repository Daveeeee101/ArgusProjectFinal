from OpenSeaDataClasses import OpenSeaAsset
from OpenSeaDataClasses import OpenSeaAccount


class Asset:

    def __init__(self, data: OpenSeaAsset, currentOwner: OpenSeaAccount):
        self.data: OpenSeaAsset = data
        self.currentOwner: OpenSeaAccount = currentOwner

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data

