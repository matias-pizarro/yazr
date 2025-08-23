from __future__ import annotations

import pathlib
from typing import Any, Optional

import bigtree
from diskcache import Cache

from .base import BaseNode


class Node(BaseNode):
    """Class to represent a node."""

    def __init__(
        self, name: str, cache_dir_path: Optional[str] = None, **kwargs: Any
    ) -> None:
        super().__init__(name=name, **kwargs)
        if not self.node_name:
            raise bigtree.exceptions.TreeError(
                "Node must have a str as `name` attribute"
            )
        if self.parent is None:
            if cache_dir_path is None:
                cache_dir_path = f"/tmp/yazr_{self.name}.cache"
            self.cache_dir = pathlib.Path(cache_dir_path)
            self._cache = Cache(self.cache_dir)
