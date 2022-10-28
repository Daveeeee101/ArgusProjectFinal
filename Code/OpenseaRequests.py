from typing import Dict
from typing import List
import ujson
from datetime import datetime
from typing import Union


class RequestTooLargeException(Exception):

    def __init__(self, requestedNumber, maxNumber):
        super().__init__()
        self.requestedNumber = requestedNumber
        self.maxNumber = maxNumber


class EventTypes:
    SUCCESSFUL = 'AUCTION_SUCCESSFUL'
    CREATED = 'AUCTION_CREATED'
    CANCELLED = 'AUCTION_CANCELLED'
    APPROVED = 'ASSET_APPROVE'
    TRANSFER = 'ASSET_TRANSFER'
    BULK_CANCEL = 'BULK_CANCEL'
    OFFER = 'OFFER_ENTERED'

    @staticmethod
    def values():
        return ['AUCTION_SUCCESSFUL', 'AUCTION_CREATED', 'AUCTION_CANCELLED', 'ASSET_APPROVE', 'ASSET_TRANSFER'
            , 'BULK_CANCEL', 'OFFER_ENTERED']


class InferredEventTypes:
    SOLD = 'SOLD'
    LISTED = 'LISTED'
    DELISTED = 'DELISTED'
    RELISTED = 'RELISTED'
    LISTING_CANCELLED = 'LISTING_CANCELLED'

    @staticmethod
    def values():
        return ['SOLD, LISTED', 'DELISTED', 'RELISTED', 'LISTING_CANCELLED']


class Chains:
    ETHEREUM = 'ETHEREUM'
    SOLANA = 'SOLANA'

    @staticmethod
    def values():
        return ['ETHEREUM', 'SOLANA']


class OpenSeaRequest:
    """Base class for creating requests that can be sent to opensea. Usually don't instantiate directly but use
    subclass instances """
    URL = "https://api.opensea.io/graphql/"

    def __init__(self):
        self.name: str = ""
        self.body: str = ""
        self.header: Dict[str, str] = {}
        self.variables = {}

    def __repr__(self):
        return self.name + "\n~~~~~~~~~~~~~~~~~~~~\n" + "headers\n---------------\n" + str(self.header) + \
               "\nbody\n---------------\n" + self.body + "\nvariables\n---------------\n" + str(self.variables)

    def setBody(self):
        queryBodies = open("./Files/QueryBodies.json")
        self.body = ujson.loads(queryBodies.read())[self.name]

    def setHeader(self):
        apiFiles = open("./Files/APICalls.json")
        key = ujson.loads(apiFiles.read())[self.name]
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://opensea.io",
            "Referer": "https://opensea.io/",
            "Authority": "api.opensea.io",
            "sec-fetch-mode": "cors",
            "x-signed-query": key
        }
        apiFiles.close()

    def getBody(self):
        return ujson.dumps({
            "id": self.name,
            "query": self.body,
            "variables": self.variables
        })


class OpenSeaEventHistoryPollQuery(OpenSeaRequest):
    """Request class for requesting events that have occurred on opensea. Can be polled so that only events after a
    certain time are returned """

    def __init__(self):
        super().__init__()
        self.name = "EventHistoryPollQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'count': 32, 'showAll': True}

    def collections(self, collSlugs: List[str]):
        """Sets the collections that the events should come from. (use collection slugs)"""
        self.variables['collections'] = collSlugs
        return self

    def eventTypes(self, eventTypes: List[EventTypes]):
        """Sets the type of events that should be registered - see EventTypes class"""
        self.variables['eventTypes'] = eventTypes
        return self

    def count(self, numberOfResponses: int):
        """Sets the number of events that should be obtained - max 32"""
        if numberOfResponses > 32:
            raise RequestTooLargeException(numberOfResponses, 32)
        self.variables['count'] = numberOfResponses
        return self

    def chains(self, chains: List[Chains]):
        """Sets the chains (e.g ethereum or solana - see Chains class) that should be queried for events"""
        self.variables['chains'] = chains
        return self

    def nft(self, tokenId: int, contractAddress: str):
        """sets the specific asset that should be queried for events using the contract address and tokenId"""
        self.variables['archetype'] = {'assetContractAddress': contractAddress, 'tokenId': tokenId}
        return self

    def fromTime(self, date: datetime):
        """sets the time from which events should be returned (the minimum timestamp that an event in the response
        can have) """
        self.variables['eventTimestamp_Gt'] = date.isoformat()
        return self


class OpenSeaOrdersQuery(OpenSeaRequest):
    """Request class for requesting orders that have occurred on opensea"""

    def __init__(self):
        super().__init__()
        self.name = "OrdersQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'count': 32, 'expandedMode': True}

    def collections(self, collSlugs: List[str]):
        """sets the collections that orders should be chosen from (use collection slugs)"""
        self.variables['takerAssetCollections'] = collSlugs
        return self


class OpenSeaAssetQuery(OpenSeaRequest):
    """Request class for requesting asset details (i.e NFTs) from opensea"""

    def __init__(self):
        super().__init__()
        self.name = "AssetSearchCollectionQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'count': 32}

    def collections(self, collections: List[str]):
        """sets the collections that asset details should be retrieved from. (use collection slug)"""
        self.variables['collections'] = collections
        return self


class OpenSeaOrderActivityQuery(OpenSeaRequest):
    """Request class for requesting orders from opensea. Difference between this and OpenSeaOrdersQuery is unclear."""

    def __init__(self):
        super().__init__()
        self.name = "OrderActivityListQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'pageSize': 32}

    def collection(self, collSlug: str):
        """choose the collection that orders are requested from"""
        self.variables['collectionSlug'] = collSlug
        return self


class OpenSeaSelectAssetQuery(OpenSeaRequest):
    """Request class for requesting asset details from opensea. Used for when you have an asset relay id but
    no information about the asset"""

    def __init__(self):
        super().__init__()
        self.name = "AssetSelectionQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'assets': []}

    def assets(self, relayIds: List[str]):
        """set a list of relayIds that the request will get assets for"""
        self.variables['assets'] = relayIds
        return self

    def addAsset(self, relayId: str):
        """Add a relayId to the list of assets that the request will get"""
        self.variables['assets'].append(relayId)
        return self


class OpenSeaCollectionActivityQuery(OpenSeaRequest):
    """Request class for getting the activities from a collection - not 100% sure what this does yet"""

    def __init__(self):
        super().__init__()
        self.name = "CollectionActivityPageQuery"
        self.setBody()
        self.setHeader()
        self.variables = {'collections': []}

    def collections(self, collections: List[str]):
        self.variables['collections'] = collections
        return self

    def addCollection(self, collection: str):
        self.variables['collections'].append(collection)
        return self

    def collection(self, collection: str):
        self.variables['collection'] = collection
        return self


class OpenSeaPriceHistoryQuery(OpenSeaRequest):
    """Class for getting the price history for a collection"""

    def __init__(self):
        super().__init__()
        self.name = "PriceHistoryGraphV2Query"
        self.setBody()
        self.setHeader()
        self.variables = {'collections': []}

    def collection(self, slug: str):
        """Set the collection to get the price history from"""
        self.variables['collectionSlug'] = slug
        return self

    def startDate(self, date: datetime):
        self.variables['startDate'] = date.isoformat()
        return self


class OpenSeaPriceHistoryQuery(OpenSeaRequest):
    """Class for getting the price history for a collection"""

    def __init__(self):
        super().__init__()
        self.name = "PriceHistoryGraphV2Query"
        self.setBody()
        self.setHeader()
        self.variables = {'collections': []}

    def collection(self, slug: str):
        """Set the collection to get the price history from"""
        self.variables['collectionSlug'] = slug
        return self

    def startDate(self, date: Union[datetime, str]):
        if type(date) == datetime:
            self.variables['startDate'] = date.isoformat()
        else:
            self.variables['startDate'] = date
        return self
