from OpenSeaDataClasses import OpenSeaEvent
from OpenseaRequests import InferredEventTypes


class Event:

    def __init__(self, data: OpenSeaEvent, inferredType: InferredEventTypes):
        self.data: OpenSeaEvent = data
        self.inferredType: InferredEventTypes = inferredType

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data


