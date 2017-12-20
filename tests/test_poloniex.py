import poloniex


def test_ticker():
    p = poloniex.Public()
    assert p.ticker() == None
