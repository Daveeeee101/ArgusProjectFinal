from OpenSeaDataClasses import OpenSeaAsset
from OpenSeaDataClasses import OpenSeaAccount
from datetime import datetime


class Asset:

    def __init__(self, data: OpenSeaAsset, currentOwner: OpenSeaAccount, isListed: bool, currPriceEth: float,
                 currPriceDollar: float):
        self.data: OpenSeaAsset = data
        self.currentOwner: OpenSeaAccount = currentOwner
        self.isListed: bool = isListed
        self.currPriceEth: float = currPriceEth
        self.currPriceDollar: float = currPriceDollar
        self.lastUpdated: datetime = datetime.now()

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data

    def updateAssetInfo(self, updateTime: datetime,
                        currentOwner: OpenSeaAccount = None,
                        isListed: bool = None,
                        currPriceEth: float = None,
                        currPriceDollar: float = None):
        """updates the asset information - should not be called by anyone other than the OpenSeaManager"""
        self.currentOwner: OpenSeaAccount = currentOwner
        self.isListed = isListed
        self.currPriceEth = currPriceEth
        self.currPriceDollar = currPriceDollar
        self.lastUpdated = updateTime
