import os
import doctest

from ofxstatement import configuration
from ofxstatement.ui import UI

def doctest_configuration():
    """Test configuration routines

        >>> ui = UI()
        >>> cfname = os.path.join(os.path.dirname(__file__),
        ...                       'samples', 'config.ini')
        >>> config = configuration.read(ui, cfname)
        >>> config['swedbank']['plugin']
        'swedbank'

    """

def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
