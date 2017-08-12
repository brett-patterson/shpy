import os
import sys
from unittest import TestCase

LIB_PATH = os.path.dirname(os.path.dirname(__file__))

class BaseTest(TestCase):
    """ A testing base class that sets up the import path to use the source
    code next to the testing directory.
    """
    def setUp(self):
        sys.path.insert(0, LIB_PATH)

    def tearDown(self):
        sys.path.remove(LIB_PATH)
