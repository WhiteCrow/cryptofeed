'''
Copyright (C) 2017-2018  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed.feedhandler import FeedHandler
from cryptofeed import Coinbase, Bitfinex, HitBTC, Bitstamp, Gemini


def nbbo_update(pair, bid, ask, bid_feed, ask_feed):
    print('Pair: {} Bid: {:.2f} Bid Feed: {} Ask: {:.2f} Ask Feed: {}'.format(pair, bid, bid_feed, ask, ask_feed))


def main():
    f = FeedHandler()
    f.add_nbbo([Coinbase, HitBTC, Bitfinex, Bitstamp, Gemini], ['BTC-USD'], nbbo_update)
    f.run()

if __name__ == '__main__':
    main()

