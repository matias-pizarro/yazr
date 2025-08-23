import functools
from collections.abc import Callable, Iterable
from typing import Any, Optional, ParamSpec, Tuple, TypeVar

from diskcache import ENOVAL
from diskcache.core import args_to_key, full_name

Param = ParamSpec("Param")
RetType = TypeVar("RetType")


# def memoize[**Param, RetType](
#     name: Optional[str] = None,
#     typed: Optional[bool] = False,
#     expire: Optional[str] = None,
#     tag: Optional[float] = None,
#     ignore: Optional[Iterable[str]] = (),
# ) -> Callable[P, R]:


def memoize(
    name: Optional[str] = None,
    typed: Optional[bool] = False,
    expire: Optional[float] = None,
    tag: Optional[str] = None,
    ignore: Optional[Iterable[str]] = (),
) -> Callable[Param, RetType]:
    """Memoizing cache decorator.

    Decorator to wrap callable with memoizing function using cache.
    Repeated calls with the same arguments will lookup result in cache and
    avoid function evaluation.

    This version has been adapted

    If name is set to None (default), the callable name will be determined
    automatically.

    When expire is set to zero, function results will not be set in the
    cache. Cache lookups still occur, however. Read
    :doc:`case-study-landing-page-caching` for example usage.

    If typed is set to True, function arguments of different types will be
    cached separately. For example, f(3) and f(3.0) will be treated as
    distinct calls with distinct results.

    The original underlying function is accessible through the __wrapped__
    attribute. This is useful for introspection, for bypassing the cache,
    or for rewrapping the function with a different cache.

    >>> from diskcache import Cache
    >>> cache = Cache()
    >>> @memoize(expire=1, tag='fib')
    ... def fibonacci(number):
    ...     if number == 0:
    ...         return 0
    ...     elif number == 1:
    ...         return 1
    ...     else:
    ...         return fibonacci(number - 1) + fibonacci(number - 2)
    >>> print(fibonacci(100))
    354224848179261915075

    An additional `__cache_key__` attribute can be used to generate the
    cache key used for the given arguments.

    >>> key = fibonacci.__cache_key__(100)
    >>> print(cache[key])
    354224848179261915075

    Remember to call memoize when decorating a callable. If you forget,
    then a TypeError will occur. Note the lack of parenthenses after
    memoize below:

    >>> @memoize
    ... def test():
    ...     pass
    Traceback (most recent call last):
        ...
    TypeError: name cannot be callable

    :param cache: cache to store callable arguments and return values
    :param str name: name given for callable (default None, automatic)
    :param bool typed: cache different types separately (default False)
    :param float expire: seconds until arguments expire
        (default None, no expiry)
    :param str tag: text to associate with arguments (default None)
    :param set ignore: positional or keyword args to ignore (default ())
    :return: callable decorator

    """
    # Caution: Nearly identical code exists in DjangoCache.memoize
    if callable(name):
        raise TypeError("name cannot be callable")

    def decorator(func):  # type: ignore[no-untyped-def]
        """Decorator created by memoize() for callable `func`."""
        base = (full_name(func),) if name is None else (name,)

        @functools.wraps(func)
        def wrapper(  # type: ignore[no-untyped-def]
            instance,
            *args: Param.args,
            **kwargs: Param.kwargs,
        ) -> Any:
            """Wrapper for callable to cache arguments and return values."""
            key = wrapper.__cache_key__(*args, **kwargs)  # type: ignore[attr-defined]
            result = instance.cache.get(key, default=ENOVAL, retry=True)

            if result is ENOVAL:
                result = func(instance, *args, **kwargs)
                if expire is None or expire > 0:
                    instance.cache.set(key, result, expire, tag=tag, retry=True)

            return result

        def __cache_key__(*args: Param.args, **kwargs: Param.kwargs) -> Tuple[str]:
            """Make key for cache given function arguments."""
            return args_to_key(base, args, kwargs, typed, ignore)  # type: ignore[no-any-return]

        wrapper.__cache_key__ = __cache_key__  # type: ignore[attr-defined]
        return wrapper

    return decorator  # type: ignore[return-value]
