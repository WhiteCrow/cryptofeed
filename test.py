import cryptofeed
from cryptofeed import FeedHandler, Gateio
from cryptofeed.defines import L2_BOOK

def cb_book(book):
    print(book)

cb = {L2_BOOK: cb_book}

fh = FeedHandler()
fh.add_feed(Gateio(pairs=['ETH_USDT'], channels=[L2_BOOK], callbacks=cb))
fh.run()

