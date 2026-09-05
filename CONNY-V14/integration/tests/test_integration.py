import unittest

from integration.contracts.platform_contract import (
    ClientContext,
    ClientPlatform,
)
from integration.service import IntegrationService


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.service = IntegrationService()

    def test_windows(self):
        result = self.service.connect(
            ClientContext(
                ClientPlatform.WINDOWS,
                "14.14.0",
                "windows-test",
            )
        )
        self.assertTrue(result.success)

    def test_linux(self):
        result = self.service.connect(
            ClientContext(
                ClientPlatform.LINUX,
                "14.14.0",
                "linux-test",
            )
        )
        self.assertTrue(result.success)

    def test_android(self):
        result = self.service.connect(
            ClientContext(
                ClientPlatform.ANDROID,
                "14.14.0",
                "android-test",
            )
        )
        self.assertTrue(result.success)

    def test_web(self):
        result = self.service.connect(
            ClientContext(
                ClientPlatform.WEB,
                "14.14.0",
                "web-test",
            )
        )
        self.assertTrue(result.success)

    def test_missing_device_rejected(self):
        with self.assertRaises(ValueError):
            self.service.connect(
                ClientContext(
                    ClientPlatform.WINDOWS,
                    "14.14.0",
                    "",
                )
            )


if __name__ == "__main__":
    unittest.main()
