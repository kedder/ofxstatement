import doctest

from ofxstatement import plugin

def doctest_autoregistration():
    """Test plugin registry operation

    To get started, make sure plugin registry is clean:
        >>> plugin.registry.clear()

    Create new plugin and see if it self-registers:
        >>> class SamplePlugin(plugin.Plugin):
        ...     name = "sample"
        >>> plugin.registry.get("sample")
        <class 'ofxstatement.tests.test_plugin.SamplePlugin'>
        >>> len(plugin.registry.enumerate())
        1
    """


def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
