"""
The Poloniex API package.

Contains clients for the Public and Trading API.
Public/Trading are segregated since they have different
concerns and security/limiting requirements.

For more see https://poloniex.com/support/api/
"""
from .public import Public
from .trading import Trading
