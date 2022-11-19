from unittest import TestCase
from OpenseaResponse import OpenseaEventHistoryPollResponse


class TestOpenseaEventHistoryPollResponse(TestCase):
    def test_collectionSlugCorrect_node_to_event(self):
        data = '{"data":{"assetEvents":{"edges":[{"node":{"collection":{"name":"Otherdeed for Otherside",' \
               '"imageUrl":"https://i.seadn.io/gae/yIm-M5' \
               '-BpSDdTEIJRt5D6xphizhIdozXjqSITgK4phWq7MmAU3qE7Nw7POGCiPGyhtJ3ZFP8iJ29TFl-RLcGBWX5qI4-ZcnCPcsY4zI?w' \
               '=500&auto=format","isVerified":true,"slug":"otherdeed","isCategory":false,' \
               '"id":"Q29sbGVjdGlvblR5cGU6MTQwNzcyNTU="},"traitCriteria":null,"itemQuantity":"1",' \
               '"item":{"__typename":"AssetType","relayId":"QXNzZXRUeXBlOjQxMjM5MDcwMw==",' \
               '"verificationStatus":"VERIFIED","__isItemType":"AssetType","name":null,"assetContract":{' \
               '"address":"0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258","id":"QXNzZXRDb250cmFjdFR5cGU6NjcwMTQ0",' \
               '"blockExplorerLink":"https://etherscan.io/address/0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258"},' \
               '"tokenId":"78472","chain":{"identifier":"ETHEREUM"},"collection":{"name":"Otherdeed for Otherside",' \
               '"id":"Q29sbGVjdGlvblR5cGU6MTQwNzcyNTU=","displayData":{"cardDisplayStyle":"CONTAIN"},' \
               '"slug":"otherdeed","verificationStatus":"VERIFIED","isCategory":false},"animationUrl":null,' \
               '"displayImageUrl":"https://img.seadn.io/files/ee45e8906410550c8476ad4a0796a629.jpg?fit=max&h=1200&w' \
               '=1200&auto=format","imageUrl":"https://img.seadn.io/files/ee45e8906410550c8476ad4a0796a629.jpg?fit' \
               '=max&h=1200&w=1200&auto=format","isDelisted":false,"backgroundColor":null,"decimals":0,' \
               '"__isNode":"AssetType","id":"QXNzZXRUeXBlOjQxMjM5MDcwMw=="},' \
               '"relayId":"QXNzZXRFdmVudFR5cGU6ODQ0MzUxNjUwNA==","eventTimestamp":"2022-11-19T23:09:42.862183",' \
               '"eventType":"CREATED","customEventName":null,"orderExpired":false,"isMint":false,"isAirdrop":false,' \
               '"creatorFee":null,"devFeePaymentEvent":null,"fromAccount":{' \
               '"address":"0xc3fcb88585d4a9243b616d48c0c20d60775e5713","config":null,"isCompromised":false,' \
               '"user":{"publicUsername":"Lower-X2Y2","id":"VXNlclR5cGU6MzEwNDEzNg=="},"displayName":"Lower-X2Y2",' \
               '"imageUrl":"https://storage.googleapis.com/opensea-static/opensea-profile/18.png",' \
               '"id":"QWNjb3VudFR5cGU6ODM5NzE5NTI="},"perUnitPrice":{"unit":"1.6678","eth":"1.6678",' \
               '"usd":"2046.6908040000001067392"},"endingPriceType":{"unit":"1.6678"},"priceType":{"unit":"1.6678"},' \
               '"payment":{"symbol":"ETH","chain":{"identifier":"ETHEREUM"},"asset":{' \
               '"imageUrl":"https://openseauserdata.com/files/6f8e2979d428180222796ff4a33ab929.svg","assetContract":{' \
               '"blockExplorerLink":"https://etherscan.io/address/0x0000000000000000000000000000000000000000",' \
               '"id":"QXNzZXRDb250cmFjdFR5cGU6MjMzMQ=="},"id":"QXNzZXRUeXBlOjEzNjg5MDc3"},' \
               '"id":"UGF5bWVudEFzc2V0VHlwZTo0Mg=="},"seller":{' \
               '"address":"0xc3fcb88585d4a9243b616d48c0c20d60775e5713","config":null,"isCompromised":false,' \
               '"user":{"publicUsername":"Lower-X2Y2","id":"VXNlclR5cGU6MzEwNDEzNg=="},"displayName":"Lower-X2Y2",' \
               '"imageUrl":"https://storage.googleapis.com/opensea-static/opensea-profile/18.png",' \
               '"id":"QWNjb3VudFR5cGU6ODM5NzE5NTI="},"toAccount":null,"winnerAccount":null,"transaction":null,' \
               '"id":"QXNzZXRFdmVudFR5cGU6ODQ0MzUxNjUwNA=="}}]}}}'
        testData = OpenseaEventHistoryPollResponse(data)
        for i in testData:
            data = OpenseaEventHistoryPollResponse.nodeToEvent(i)
            self.assertEqual(data.getCollectionInfo().slug, "otherdeed")


