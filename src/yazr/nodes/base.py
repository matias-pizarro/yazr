from __future__ import annotations

import bigtree
from diskcache import Cache


class BaseNode(bigtree.Node):  # type: ignore[misc]
    """Base class to represent a node."""

    @property
    def cache(self) -> Cache:
        try:
            return self._cache
        except AttributeError:
            return self.parent.cache

    def __repr__(self) -> str:
        """Print format of Node.

        Returns:
            Print format of Node
        """
        class_name = self.__class__.__name__
        return f"{class_name}({self.path_name})"
