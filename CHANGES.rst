~~~~~~~
Changes
~~~~~~~

0.6.1 (2017-05-07)

- Fix installation problem on python-3.5 (#55)


0.6.0 (2016-12-02)
==================

- Support for specifying account information for each parsed satatement
  line and translate it to BANKACCTTO aggregate in OFX.

- Command line option to display debugging information (--debug).

- Fix config file location for appdirs >= 1.3.0

0.5.0 (2013-11-03)
==================

- Plugins are now registered via setuptools' entry-points mechanism. This
  allows plugins to live in separate eggs and developed independently of
  ofxstatement itself. Plugins are registered as 'ofxstatement' entry points
  (#11).


- Command line interface changed: ``ofxstatement`` now accepts "action"
  parameter and few actions were added:

  * ``ofxstatement convert``: perform conversion to OFX
  * ``ofxstatement list-plugins``: list available conversion plugins
  * ``ofxstatement edit-config``: launch default editor to edit configuration
    file

- ``ofxstatement convert`` can be run without any configuration. Plugin name
  to use is specified using ``-t TYPE`` parameter in this case (#12).

- ``StatementLine`` supports more attributes, translated to OFX (#13):

  * ``refnum`` - translated to ``<REFNUM>`` in OFX.
  * ``trntype`` - translated to ``<TRNTYPE>`` in OFX.
