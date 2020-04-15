

def put_break_even(strike, cost):
    """
    :param strike: strike price of the put option
    :param cost: cost of the put option
    :return: price of stock where this put option will break even
    """
    return strike - cost