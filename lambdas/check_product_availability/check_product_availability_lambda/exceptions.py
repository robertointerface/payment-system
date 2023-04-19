class OrderNotFoundException(Exception):
    """Order is not found on database"""
    pass


class ProductNotFoundException(Exception):
    """Product no found on database"""
    pass


class ProductsNotAvailableException(Exception):
    """One or multiple of the products are not available on database."""
    pass
