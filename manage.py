import unittest

import click
from vk_app.tests.test_models import TestModels

from tests.test_utils import TestUtils


@click.group(name='tests', invoke_without_command=False)
def test():
    pass


@test.command(name='models')
def models():
    """Tests implemented models"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    unittest.TextTestRunner(verbosity=2).run(suite)


@test.command(name='utils')
def utils():
    """Tests utility functions"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    test()
