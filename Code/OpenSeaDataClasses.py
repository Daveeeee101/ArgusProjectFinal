from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from OpenseaRequests import EventTypes


@dataclass(frozen=True)
class OpenSeaAccount:
    address: str
    relayId: str


@dataclass(frozen=True)
class OpenSeaCollection:
    slug: str
    name: str
    relayId: str


@dataclass(frozen=True)
class OpenSeaAsset:
    name: str
    contractAddress: str
    tokenId: int
    collection: OpenSeaCollection
    relayId: str


@total_ordering
@dataclass(frozen=True)
class OpenSeaEvent:
    timestamp: datetime
    fromAccount: OpenSeaAccount
    asset: OpenSeaAsset
    type: EventTypes
    relayId: str
    toAccount: OpenSeaAccount = None
    priceEth: float = None
    priceUSD: float = None

    def __le__(self, other):
        return self.timestamp < other.timestamp

    def getCollectionInfo(self) -> OpenSeaCollection:
        return self.asset.collection
