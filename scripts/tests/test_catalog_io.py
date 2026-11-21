import json
import tempfile
import unittest
from pathlib import Path

from catalog_io import load_catalog, migrate_to_shards, save_catalog


class CatalogShardTests(unittest.TestCase):
    def test_round_trip_and_update(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "sources.json"
            original = {"schema_version": 1, "resources": [{"id": str(i), "title": "x" * 80} for i in range(30)]}
            path.write_text(json.dumps(original), encoding="utf-8")
            count, shards = migrate_to_shards(path, 500)
            self.assertEqual(count, 30)
            self.assertGreater(shards, 1)
            self.assertEqual(load_catalog(path), original)
            updated = load_catalog(path)
            updated["resources"].append({"id": "new", "title": "added"})
            save_catalog(path, updated)
            self.assertEqual(load_catalog(path), updated)
            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["record_count"], 31)

    def test_legacy_list_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sources.json"
            original = [{"id": "one"}, {"id": "two"}]
            path.write_text(json.dumps(original), encoding="utf-8")
            migrate_to_shards(path, 500)
            self.assertEqual(load_catalog(path), original)


if __name__ == "__main__":
    unittest.main()
