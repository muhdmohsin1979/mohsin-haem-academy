from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MCLReleaseStateGateTests(unittest.TestCase):
    def test_ci_invokes_the_state_aware_gate(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "preflight.yml").read_text(encoding="utf-8")
        active_lines = [line.split("#", 1)[0].strip() for line in workflow.splitlines()]
        self.assertIn("run: python scripts/validate_mcl_release_state.py", active_lines)

    def test_production_candidate_requires_exact_release_and_candidate_containment(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_mcl_release_state.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("MCL production-candidate containment: PASS", result.stdout)
        self.assertIn("MCL v2.0 production-candidate validation: PASS", result.stdout)
        self.assertIn("MCL controlled publication state gate: PASS state=PRODUCTION_CANDIDATE", result.stdout)


if __name__ == "__main__":
    unittest.main()
