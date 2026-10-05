"""Every frozen file has a search behind it and a place in the hash chain."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import engine.dagapeyeff_cache as cache
from engine.dagapeyeff_provenance import provenance_report

# The parity check is hashed inside the checks entry, not on its own.
_COVERED_ELSEWHERE = {"parity"}


class DagapeyeffCacheTest(unittest.TestCase):
    def test_every_file_has_a_search_and_every_search_has_a_file(self) -> None:
        registry = cache.frozen_registry()
        stored = cache.stored_names()
        self.assertEqual(sorted(registry), stored)
        for name, (module, function) in registry.items():
            self.assertTrue(module.startswith("engine."), name)
            self.assertTrue(function, name)

    def test_every_frozen_file_is_in_the_provenance_chain(self) -> None:
        chained = {entry["name"] for entry in provenance_report()["entries"]}
        missing = sorted(set(cache.stored_names()) - chained - _COVERED_ELSEWHERE)
        self.assertEqual(missing, [], "add these frozen names to engine/dagapeyeff_provenance.py")

    def test_the_first_call_returns_what_later_calls_read(self) -> None:
        with tempfile.TemporaryDirectory() as folder, mock.patch.object(cache, "_DIR", Path(folder)):
            first = cache.remember("probe", lambda: {"pair": (1, 2), "rows": {3: 4.5}})
            again = cache.remember("probe", lambda: self.fail("the file should be read"))
        self.assertEqual(first, {"pair": [1, 2], "rows": {"3": 4.5}})
        self.assertEqual(first, again)

    def test_one_name_cannot_belong_to_two_searches(self) -> None:
        with mock.patch.dict(cache._REGISTRY, clear=False):

            @cache.frozen("duplicate-probe")
            def one() -> dict:
                return {}

            with self.assertRaises(ValueError):

                @cache.frozen("duplicate-probe")
                def two() -> dict:
                    return {}

        self.assertNotIn("duplicate-probe", cache._REGISTRY)
        self.assertEqual(one.cache_name, "duplicate-probe")


if __name__ == "__main__":
    unittest.main()
