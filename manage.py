import unittest

import click

from tests.test_app import TestApp
from tests.test_models import TestModels
from tests.test_utils import TestUtils


@click.group(name='tests', invoke_without_command=False)
def test():
    pass


@test.command(name='test_models')
def test_models():
    """Tests implemented models"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    unittest.TextTestRunner(verbosity=2).run(suite)


@test.command(name='test_utils')
def test_utils():
    """Tests utility functions"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)


@test.command(name='test_app')
def test_app():
    """Tests utility functions"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    test()
