Changes
-------

0.7.1 (2020-09-14)
==================

- Include PEP-561 marker into source code distribution


0.7.0 (2020-09-13)
==================

- Drop support for Python 3.4, 3.5, add support for Python 3.8
- Fixed naive end balance validation (#106)
- Modernize development environment (use pipenv, mypy, black)

0.6.5 (2020-06-09)
==================

- Added balance checks and improved generation of unique ids (#100, #104)


0.6.4 (2020-03-04)
==================

- Fix regression introduced in 0.6.3 - `edit-config` command stopped working.


0.6.3 (2020-02-13)
==================

- Fix config editing on Windows

0.6.2 (2020-01-20)
==================

- Better `EDITOR` environment variable handling for `edit-config` command
- Support Python-3.7
- API: type of StatementLine.date_user (date when user initiated transaction)
  will not be a string by default.
- API: More unique generated transaction ids (when one is not available from
  the statement file)

0.6.1 (2017-05-07)
==================

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
