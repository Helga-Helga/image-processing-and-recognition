def get_factors(x):
    """Search of number factors

    Parameters
    ----------
    x : int
        Input number

    Returns
    -------
    list of integers
        Factors of x
    """
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors[1:]
