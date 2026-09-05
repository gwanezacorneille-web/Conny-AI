from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FinalV14Tests(unittest.TestCase):

    def test_version(self):
        version = (
            ROOT / "VERSION"
        ).read_text().strip()

        self.assertEqual(
            version,
            "14.16.0",
        )

    def test_web_client_exists(self):
        self.assertTrue(
            (ROOT / "clients/web/index.html").is_file()
        )

        self.assertTrue(
            (ROOT / "clients/web/app.js").is_file()
        )

    def test_android_client_exists(self):
        self.assertTrue(
            (ROOT / "clients/android/AuthClient.java").is_file()
        )

    def test_windows_client_exists(self):
        self.assertTrue(
            (
                ROOT
                / "clients/desktop/windows/conny_v14_windows.py"
            ).is_file()
        )

    def test_linux_client_exists(self):
        self.assertTrue(
            (
                ROOT
                / "clients/desktop/linux/conny_v14_linux.py"
            ).is_file()
        )

    def test_deployment_files_exist(self):
        self.assertTrue(
            (ROOT / "requirements.txt").is_file()
        )

        self.assertTrue(
            (ROOT / "render.yaml").is_file()
        )

        self.assertTrue(
            (ROOT / "Procfile").is_file()
        )

    def test_shared_auth_contract_exists(self):
        self.assertTrue(
            (
                ROOT
                / "integration/clients/auth_contract.py"
            ).is_file()
        )

    def test_sync_api_exists(self):
        text = (
            ROOT / "api/main.py"
        ).read_text()

        self.assertIn(
            "/sync/push",
            text,
        )

        self.assertIn(
            "/sync/pull",
            text,
        )


if __name__ == "__main__":
    unittest.main()
