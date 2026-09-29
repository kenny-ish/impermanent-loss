import unittest

from il import il_v2, il_v3


class ILTest(unittest.TestCase):
    def test_no_move_no_loss(self):
        self.assertAlmostEqual(il_v2(1), 0)
        self.assertAlmostEqual(il_v3(100, 100, 50, 200), 0)

    def test_known_v2_values(self):
        self.assertAlmostEqual(il_v2(2), -0.05719, places=5)
        self.assertAlmostEqual(il_v2(0.5), il_v2(2))  # symmetric in log space

    def test_wide_v3_range_matches_v2(self):
        self.assertAlmostEqual(il_v3(100, 200, 1e-6, 1e10), il_v2(2), places=3)

    def test_narrow_range_amplifies(self):
        self.assertLess(il_v3(100, 120, 90, 130), il_v2(1.2))

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            il_v3(1, 2, 3, 2)


if __name__ == "__main__":
    unittest.main()
