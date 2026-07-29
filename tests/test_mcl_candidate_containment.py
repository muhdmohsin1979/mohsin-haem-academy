from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_mcl_candidate_containment as candidate

ROOT = Path(__file__).resolve().parents[1]


class MCLCandidateContainmentNegativeTests(unittest.TestCase):
    def validate_with(self, worker: str, routes: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            worker_path = root / "_worker.js"
            routes_path = root / "_routes.json"
            worker_path.write_text(worker, encoding="utf-8")
            routes_path.write_text(json.dumps(routes), encoding="utf-8")
            with patch.object(candidate, "WORKER", worker_path), patch.object(candidate, "ROUTES", routes_path):
                candidate.validate_candidate_containment()

    def test_missing_worker_block_fails_closed(self) -> None:
        worker = (ROOT / "_worker.js").read_text(encoding="utf-8").replace(
            '  "/guidelines/mcl/guideline-v2.0.pdf",\n', "", 1
        )
        routes = json.loads((ROOT / "_routes.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(AssertionError, "not blocked"):
            self.validate_with(worker, routes)

    def test_missing_cloudflare_route_fails_closed(self) -> None:
        worker = (ROOT / "_worker.js").read_text(encoding="utf-8")
        routes = json.loads((ROOT / "_routes.json").read_text(encoding="utf-8"))
        routes["include"].remove("/guidelines/mcl/quickref-v2.0.pdf")
        with self.assertRaisesRegex(AssertionError, "bypass the worker"):
            self.validate_with(worker, routes)


if __name__ == "__main__":
    unittest.main()
