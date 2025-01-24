"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from unittest import TestCase

from common.utils.singleton import Singleton


class Foo(metaclass=Singleton):
    def __init__(self, num: int):
        self.num = num


class TestSingleton(TestCase):
    """
    Tests for common.utils.singleton.Singleton
    """

    def tearDown(self):
        Singleton.destroy(Foo)

    def test_class_is_singleton(self):
        expected_num = 3
        foo = Foo(expected_num)
        self.assertEqual(
            expected_num,
            foo.num,
        )

        # This shouldn't update the num
        foo2 = Foo(12345)
        self.assertEqual(
            expected_num,
            foo.num,
        )

    def test_destroy(self):
        expected_foo = Foo(3)
        self.assertTrue(Foo in Singleton._instances)
        self.assertEqual(
            expected_foo,
            Singleton._instances[Foo],
        )

        Singleton.destroy(Foo)
        self.assertFalse(Foo in Singleton._instances)

        # Creating a new one updates the settings
        expected_num = 12345
        foo = Foo(expected_num)
        self.assertTrue(Foo in Singleton._instances)
        self.assertEqual(
            expected_num,
            foo.num,
        )

    def test_destroy_class_does_not_exist(self):
        self.assertFalse(TestCase in Singleton._instances)
        # We shouldn't get any errors
        Singleton.destroy(TestCase)
