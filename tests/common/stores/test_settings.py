"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

import os
from unittest import TestCase

from common.stores.settings import SettingsStore
from common.utils.singleton import Singleton


TEST_DEFAULTS_CONFIG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'config.ini',
    ),
)


class TestSettingsStore(TestCase):
    """
    Tests for common.stores.settings.SettingsStore
    """

    def tearDown(self):
        Singleton.destroy(SettingsStore)

    def test_class_is_singleton(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_config = 'testDefaults'
        self.assertEqual(
            expected_config,
            settings_store._config['config.meta']['name'],
        )

        # Next call shouldn't change the config
        new_settings_store = SettingsStore(config='foo.bar.txt')
        self.assertEqual(
            expected_config,
            settings_store._config['config.meta']['name'],
        )

    def test_init_with_default_config(self):
        settings_store = SettingsStore()
        expected_config = 'defaults'

        self.assertEqual(
            expected_config,
            settings_store._config['config.meta']['name'],
        )

    def test_init_with_test_config(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_config = 'testDefaults'

        self.assertEqual(
            expected_config,
            settings_store._config['config.meta']['name'],
        )

    def test_get_section_only(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_section = ['foo', 'baz', 'buz']

        self.assertEqual(
            expected_section,
            settings_store.get('test.data'),
        )

    def test_get_invalid_section(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        self.assertIsNone(settings_store.get('foo'))

    def test_get_section_and_key(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_value = 'bar'

        self.assertEqual(
            expected_value,
            settings_store.get('test.data', 'foo'),
        )

    def test_get_invalid_key(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        self.assertIsNone(
            settings_store.get('test.data', 'boz'),
        )

    def test_get_typed_key_int(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_value = 1

        self.assertEqual(
            expected_value,
            settings_store.get('test.data', 'baz', int),
        )

    def test_get_typed_key_bool(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        expected_value = True

        for value in ['yes', 'Yes', 'y', 'Y', '1', 'true', 'True']:
            self.assertEqual(
                expected_value,
                settings_store._convert_to_type(value, bool),
            )

        expected_value = False
        for value in ['no', 'No', 'n', 'N', '0', 'false', 'False']:
            self.assertEqual(
                expected_value,
                settings_store._convert_to_type(value, bool),
            )

        for value in ['3', 'foo.bar', 'None']:
            self.assertIsNone(
                settings_store._convert_to_type(value, bool),
            )

    def test_get_invalidly_typed_key(self):
        settings_store = SettingsStore(config=TEST_DEFAULTS_CONFIG)
        self.assertIsNone(
            settings_store.get('test.data', 'foo', int),
        )
