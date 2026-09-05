import unittest

from v14_platform.models import PlatformContext, PlatformType


class PlatformModelTests(unittest.TestCase):

    def test_windows_context(self):
        context = PlatformContext(
            PlatformType.WINDOWS,
            "14.7.0",
            "windows-test",
        )
        self.assertTrue(context.is_supported)

    def test_linux_context(self):
        context = PlatformContext(
            PlatformType.LINUX,
            "14.7.0",
            "linux-test",
        )
        self.assertTrue(context.is_supported)

    def test_android_context(self):
        context = PlatformContext(
            PlatformType.ANDROID,
            "14.7.0",
            "android-test",
        )
        self.assertTrue(context.is_supported)

    def test_unknown_context(self):
        context = PlatformContext(
            PlatformType.UNKNOWN,
            "14.7.0",
            "unknown-test",
        )
        self.assertFalse(context.is_supported)


if __name__ == "__main__":
    unittest.main()
