~~~~~~~
Changes
~~~~~~~

0.5.0 (unreleased)
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