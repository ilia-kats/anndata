from collections.abc import MutableMapping
from warnings import warn

from .._core.access import ElementRef


class DeprecatedDict(MutableMapping):
    def __init__(self, data, *, deprecated_items: "Mapping[str, ElementRef]"):
        self.data = dict(data)
        self.deprecated_items = deprecated_items

    def _access_warn(self, key, cur_loc):
        warn(
            f"This location for '{key}' is deprecated. It is instead stored in {cur_loc}",
            FutureWarning,
            stacklevel=2,
        )

    def __getitem__(self, key):
        if key in self.deprecated_items:
            cur_loc = self.deprecated_items[key]
            self._access_warn(key, cur_loc)
            return cur_loc.get()
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        if key in self.deprecated_items:
            cur_loc = self.deprecated_items[key]
            self._access_warn(key, cur_loc)
            cur_loc.set(value)
        else:
            self.data[key] = value

    def __delitem__(self, key):
        if key in self.deprecated_items:
            cur_loc = self.deprecated_items[key]
            self._access_warn(key, cur_loc)
            cur_loc.delete()
            del self.deprecated_items[key]
        else:
            del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def copy(self) -> dict:
        return self.data.copy()