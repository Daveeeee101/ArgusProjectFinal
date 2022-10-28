from OpenSeaDataClasses import OpenSeaAccount


class Account:

    def __init__(self, data: OpenSeaAccount):
        self.data: OpenSeaAccount = data

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data

