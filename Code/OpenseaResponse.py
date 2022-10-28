import ujson
from typing import List
from datetime import datetime
import datetime
from OpenseaRequests import EventTypes


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
    def nodeToEvent(node):
        try:
            collInfo = node['collection']
            slug = collInfo['slug']
        except (TypeError, ValueError):
            raise NodeConversionException(reason="could not get collection info", nodeCode=node)
        try:
            timestamp = datetime.fromisoformat(node['eventTimestamp'])
        except (TypeError, ValueError):
            raise NodeConversionException(reason=f"cannot convert timestamp", nodeCode=node)
        eventType = node['eventType']
        if eventType not in EventTypes.values():
            raise NodeConversionException(reason=f"event type not expected = {eventType}", nodeCode=node)
        try:
            sellerInfo = node['fromAccount']
            addressLink = sellerInfo['address']
        except (TypeError, ValueError):
            raise NodeConversionException(reason=f"could not get user details", nodeCode=node)

    def toEventList(self):
        return [self.nodeToEvent(node) for node in self]


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


