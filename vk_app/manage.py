import unittest

import click

from tests.test_models import TestModels
from tests.test_utils import TestUtils


@click.group(name='tests', invoke_without_command=False)
def main():
    pass


@main.command(name='models')
def test_models():
    """Tests implemented models"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    unittest.TextTestRunner(verbosity=2).run(suite)


@main.command(name='utils')
def test_models():
    """Tests utility functions"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
