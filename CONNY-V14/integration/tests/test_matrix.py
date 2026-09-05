import unittest

from integration.contracts.platform_contract import (
    ClientContext,
    ClientPlatform,
)
from integration.service import IntegrationService


class CrossPlatformMatrixTests(unittest.TestCase):

    def test_all_platforms(self):
        service = IntegrationService()

        for platform in ClientPlatform:
            with self.subTest(platform=platform):
                result = service.connect(
                    ClientContext(
                        platform,
                        "14.14.0",
                        f"{platform.value}-matrix",
                    )
                )
                self.assertTrue(result.success)

    def test_platforms_are_distinct(self):
        values = {platform.value for platform in ClientPlatform}
        self.assertEqual(
            values,
            {"windows", "linux", "android", "web"},
        )


if __name__ == "__main__":
    unittest.main()
