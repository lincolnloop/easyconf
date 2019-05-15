import typing
from decimal import Decimal

REQUIRED = object()

CASTS = [int, str, float, list, bool, Decimal]
CastTypes = typing.TypeVar("CastTypes", *CASTS)
