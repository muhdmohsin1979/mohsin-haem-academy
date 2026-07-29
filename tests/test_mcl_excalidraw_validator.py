from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MCLExcalidrawValidatorTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("MCL_EXCAL_NODE_ROOT"), "isolated Excalidraw renderer not configured")
    def test_official_renderer_accepts_exact_editable_preview(self) -> None:
        env = os.environ.copy()
        node_root = Path(env["MCL_EXCAL_NODE_ROOT"])
        env["NODE_PATH"] = str(node_root / "node_modules")
        result = subprocess.run(
            ["node", "scripts/validate_mcl_excalidraw.cjs"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("official MCL Excalidraw render audit: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
