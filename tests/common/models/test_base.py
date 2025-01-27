"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from typing import Optional
from unittest import TestCase

from pydantic import BaseModel

from common.models.base import HashableMixin


class Foo(HashableMixin, BaseModel):
    id: str
    attr: Optional[str] = None


class Bar(HashableMixin, BaseModel):
    id: str


class FooOptionalId(HashableMixin, BaseModel):
    id: Optional[str] = None
    attr: str

    @property
    def unique_fields(self):
        return ['attr']


class FooMissingUniqueFields(HashableMixin, BaseModel):
    attr: str


class TestHashableMixin(TestCase):
    """
    Tests for common.models.base.HashableMixin
    """

    def test_eq_true(self):
        foo1 = Foo(id='foo')
        foo2 = Foo(id='foo')
        self.assertEqual(foo1, foo2)

    def test_eq_true_different_attributes(self):
        # It should only look at the attributes.
        # One represents an unsaved version;
        # one represents a saved version of the same object.
        foo1 = FooOptionalId(attr='bar')
        foo2 = FooOptionalId(id='foo', attr='bar')
        self.assertEqual(foo1, foo2)

    def test_eq_false_different_classes(self):
        foo = Foo(id='foo')
        bar = Bar(id='foo')
        self.assertNotEqual(foo, bar)

    def test_eq_false_different_ids_same_attributes(self):
        # It should only look at the IDs,
        # because we might be in the process of updating a model.
        foo1 = Foo(id='foo')
        foo2 = Foo(id='foo', attr='bar')
        self.assertEqual(foo1, foo2)

    def test_eq_false_different_attributes(self):
        foo1 = FooOptionalId(id='foo', attr='bar')
        foo2 = FooOptionalId(id='foo', attr='foo')
        self.assertNotEqual(foo1, foo2)

    def test_hash(self):
        foo = Foo(id='foo', attr='bar')

        attrs_dict = {'id': foo.id}
        expected = hash(f'{foo.__class__.__qualname__}-{attrs_dict}')
        returned = hash(foo)

        self.assertEqual(expected, returned)

    def test_hash_no_unique_id(self):
        foo = FooOptionalId(id='foo', attr='bar')

        attrs_dict = {'attr': foo.attr}
        expected = hash(f'{foo.__class__.__qualname__}-{attrs_dict}')
        returned = hash(foo)

        self.assertEqual(expected, returned)

    def test_unique_fields_id_exists(self):
        foo = Foo(id='foo', attr='bar')
        expected = ['id']
        returned = foo.unique_fields
        self.assertEqual(expected, returned)

    def test_unique_fields_properly_implemented(self):
        foo = FooOptionalId(id='foo', attr='bar')
        expected = ['attr']
        returned = foo.unique_fields
        self.assertEqual(expected, returned)

    def test_unique_fields_not_implementented(self):
        foo = FooMissingUniqueFields(attr='bar')
        with self.assertRaises(NotImplementedError):
            foo.unique_fields
