import os
import unittest

from ofxstatement import configuration


class ConfigurationTest(unittest.TestCase):

    def test_configuration(self):
        here = os.path.dirname(__file__)
        cfname = os.path.join(here, 'samples', 'config.ini')
        config = configuration.read(cfname)
        self.assertEqual(config['swedbank']['plugin'], 'swedbank')

    def test_missing_configuration(self):
        config = configuration.read("missing.ini")
        self.assertIsNone(config)
