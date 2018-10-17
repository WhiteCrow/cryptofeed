'''
Copyright (C) 2017-2018  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio
import json
import logging
from decimal import Decimal
from collections import defaultdict
from datetime import datetime as dt

import requests
from sortedcontainers import SortedDict as sd

from cryptofeed.feed import Feed
from cryptofeed.exchanges import GATEIO, COINBASE
from cryptofeed.defines import L2_BOOK, L3_BOOK, BID, ASK, TRADES, TICKER, DEL, UPD


LOG = logging.getLogger('feedhandler')

class Gateio(Feed):
    id = GATEIO
    api = 'wss://ws.gateio.io/v3/'

    def __init__(self, pairs=None, channels=None, callbacks=None, **kwargs):
        super().__init__('api', pairs=pairs, channels=channels, callbacks=callbacks, **kwargs)
        self.pairs = pairs
        self.__reset()

    def __reset(self):
        self.l3_book = {}
        self.l2_book = {}

    async def subscribe(self, websocket):
        for channel in self.channels:
            await websocket.send(json.dumps({"id": 'subscribe_gateio_' + str(dt.datetime.now()),
                                             "method": channel}))

    # TODO
    async def _ticker(self, msg):
        ''' example:
        {
            "error": null,
            "result": {
                "period": 86400,
                "open": "5.9606",
                "close": "5.9606",
                "high": "5.9606",
                "low": "5.9606",
                "last": "5.9606",
                "change": "0",
                "quoteVolume": "4",
                "baseVolume": "23.8424"
            },
            "id": 12312
        }
        '''
        await self.callbacks[TICKER](feed=self.id,
                                     pair="to do",
                                     bid=Decimal(msg['best_bid']),
                                     ask=Decimal(msg['best_ask']))

    async def _l2_book(self, msg):
        """ example:
        {
            "method": "depth.update",
            "params": [
                true,
                {
                "asks": [
                    [
                        "8000.00",
                        "9.6250"
                    ]
                ],
                "bids": [
                    [
                        "8000.00",
                        "9.6250"
                    ]
                ]},
                "EOS_USDT"
            ],
            "id": null
        }
        """
        timestamp = dt.utcnow()
        timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        pair = msg['params'][-1]
        self.l2_book[pair] = {
            BID: sd({
                Decimal(price): Decimal(amount)
                for price, amount in msg['bids']
            }),
            ASK: sd({
                Decimal(price): Decimal(amount)
                for price, amount in msg['asks']
            })
        }
        await self.callbacks[L2_BOOK](feed=self.id, pair=pair, book=self.l2_book[pair], timestamp=timestamp)
