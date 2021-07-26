#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   async-redis-cache, 2021
#   LiveViewTech
# <<

from hashlib import sha1

from toolz.functoolz import is_arity, has_keywords


__all__ = [
    'MAX_KEYLEN',
    'default_key_builder',
    'trim_key',
]

MAX_KEYLEN = 80


def default_key_builder(func, args, kwargs) -> str:
    """Converts keys passed to a single function into a SHA1 checksum for caching."""
    try:
        has_kwargs = has_keywords(func) is not False
        is_unary = is_arity(1, func)
    except TypeError:  # pragma: no cover
        has_kwargs = True
        is_unary = False

    if is_unary:
        k = str(args[0])
    elif has_kwargs:
        k = (args or None, frozenset(kwargs.items() if kwargs else None))
    else:
        k = args
    key = sha1(str(k).encode('utf-8')).hexdigest()[:MAX_KEYLEN]
    return trim_key(key)


def trim_key(key: str) -> str:
    """Fixes a string to a fixed length defined as a constant ``MAX_KEYLEN``.

    >>> trim_key('')
    ''
    >>> trim_key('abc')
    'abc'
    """
    return str(key)[:MAX_KEYLEN]