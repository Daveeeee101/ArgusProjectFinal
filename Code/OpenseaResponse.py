import ujson
from typing import List
from datetime import datetime
import datetime
from OpenseaRequests import EventTypes
from OpenSeaDataClasses import *


class OpenseaResponse:

    def __init__(self, textResponse):
        self.jsonFormat = ujson.loads(textResponse)

    def strip(self) -> List:
        pass

    def __iter__(self):
        for event in self.strip():
            yield event['node']

    def __repr__(self):
        out = ""
        for ev in self:
            out += "========================================\n"
            for (key, val) in ev.items():
                out += f"{key} = {val}\n"
            out += "========================================\n"
        return out


class NodeConversionException(Exception):

    def __init__(self, reason, nodeCode):
        super().__init__()
        self.reason: str = reason
        self.code = nodeCode


class OpenseaEventHistoryPollResponse(OpenseaResponse):

    def __init__(self, textResponse):
        super().__init__(textResponse)

    def strip(self):
        return self.jsonFormat['data']['assetEvents']['edges']

    @staticmethod
    def nodeToEvent(node) -> OpenSeaEvent:
        try:
            collInfo = node['collection']
            slug = collInfo['slug']
            collName = collInfo['name']
            collRelayId = collInfo['id']
        except (TypeError, ValueError):
            raise NodeConversionException(reason="could not get collection info", nodeCode=node)
        try:
            timestamp = datetime.fromisoformat(node['eventTimestamp'])
        except (TypeError, ValueError):
            raise NodeConversionException(reason=f"cannot convert timestamp", nodeCode=node)
        eventType = node['eventType']
        if eventType == 'CREATED' or eventType == 'CANCELLED':
            toAccount = None
            if eventType == 'CREATED':
                eventTypeOut = EventTypes.CREATED
                try:
                    priceDetails = node['perUnitPrice']
                    priceEth = priceDetails['eth']
                    priceUSD = priceDetails['usd']
                except (TypeError, ValueError):
                    raise NodeConversionException(reason=f"could not get user details", nodeCode=node)
            else:
                eventTypeOut = EventTypes.CANCELLED
                priceEth = None
                priceUSD = None
            try:
                sellerInfo = node['seller']
                sellerAddressLink = sellerInfo['address']
                sellerRelayId = sellerInfo['id']
            except (TypeError, ValueError):
                """THIS HAPPENS WHEN THERE IS AN OFFER BEING CANCELLED"""
                return None
        elif eventType == 'SUCCESSFUL':
            eventTypeOut = EventTypes.SUCCESSFUL
            try:
                priceDetails = node['perUnitPrice']
                priceEth = priceDetails['eth']
                priceUSD = priceDetails['usd']
            except (TypeError, ValueError):
                raise NodeConversionException(reason=f"could not get user details", nodeCode=node)
            try:
                sellerInfo = node['seller']
                sellerAddressLink = sellerInfo['address']
                sellerRelayId = sellerInfo['id']
            except (TypeError, ValueError):
                raise NodeConversionException(reason=f"could not get user seller details", nodeCode=node)
            try:
                buyerInfo = node['winnerAccount']
                buyerAddressLink = buyerInfo['address']
                buyerRelayId = buyerInfo['id']
                toAccount = OpenSeaAccount(address=buyerAddressLink, relayId=buyerRelayId)
            except (TypeError, ValueError):
                raise NodeConversionException(reason=f"could not get user buyer details", nodeCode=node)

        else:
            raise NodeConversionException(reason=f"Unsupported event type", nodeCode=node)
        try:
            assetInfo = node['item']
            assetName = assetInfo['name']
            tokenId = int(assetInfo['tokenId'])
            address = assetInfo['assetContract']['address']
            assetRelay = assetInfo['id']
        except (TypeError, ValueError):
            raise NodeConversionException(reason=f"could not get asset details", nodeCode=node)
        try:
            eventRelay = node['id']
        except (TypeError, ValueError):
            raise NodeConversionException(reason=f"could not get relayId details", nodeCode=node)

        return OpenSeaEvent(timestamp=timestamp,
                            fromAccount=OpenSeaAccount(sellerAddressLink, sellerRelayId),
                            asset=OpenSeaAsset(name=assetName,
                                               contractAddress=address,
                                               collection=OpenSeaCollection(slug, collName, collRelayId),
                                               tokenId=tokenId,
                                               relayId=assetRelay),
                            type=eventTypeOut,
                            relayId=eventRelay,
                            toAccount=toAccount,
                            priceEth=priceEth,
                            priceUSD=priceUSD,
                            )

    def toOpenSeaEventList(self) -> List[OpenSeaEvent]:
        return [self.nodeToEvent(node) for node in self if self.nodeToEvent(node) is not None]


class OpenSeaOrderResponse(OpenseaResponse):

    def __init__(self, textResponse):
        super().__init__(textResponse)

    def strip(self):
        return self.jsonFormat['data']['orders']['edges']


class OpenSeaOrderActivityResponse(OpenseaResponse):

    def __init__(self, textResponse):
        super().__init__(textResponse)

    def strip(self):
        return self.jsonFormat['data']['collectionItems']['edges']
