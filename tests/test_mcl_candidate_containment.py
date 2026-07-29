from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import patch

from scripts import validate_mcl_candidate_containment as candidate


class MCLCandidateContainmentNegativeTests(unittest.TestCase):
    def valid_worker(self) -> str:
        entries = "\n".join(f'  "{path}",' for path in sorted(candidate.CANDIDATE_PATHS))
        return f"const BLOCKED_FILES = new Set([\n{entries}\n]);\n"

    def valid_routes(self) -> dict[str, object]:
        return {"version": 1, "include": sorted(candidate.CANDIDATE_PATHS), "exclude": []}

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
        worker = self.valid_worker().replace(
            '  "/guidelines/mcl/guideline-v2.0.pdf",\n', "", 1
        )
        routes = self.valid_routes()
        with self.assertRaisesRegex(AssertionError, "not blocked"):
            self.validate_with(worker, routes)

    def test_missing_cloudflare_route_fails_closed(self) -> None:
        worker = self.valid_worker()
        routes = self.valid_routes()
        include = cast(list[str], routes["include"])
        include.remove("/guidelines/mcl/quickref-v2.0.pdf")
        with self.assertRaisesRegex(AssertionError, "bypass the worker"):
            self.validate_with(worker, routes)


if __name__ == "__main__":
    unittest.main()
