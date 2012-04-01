Package provides single command line tool to run: ``ofxstatement``. Run
``ofxstatement -h`` to see basic usage description.


Rationale
=========

Most internet banking systems are capable of exporting account transaction to
some sort of computer readable formats, but few supports standard data formats,
like `OFX`_.  On the other hand, personal accounting tools, such as `GnuCash`_
support standard formats only, and will probably never support proprietary
statement formats of online banking systems.

To bridge the gap between them, ofxstatement tool was created.

.. _GnuCash: http://gnucash.org/
.. _OFX: http://en.wikipedia.org/wiki/Open_Financial_Exchange

Mode of operation
=================

The ``ofxstatement`` tool is intended to be used in the following workflow:

1. At the end of each month, use your online banking service to export
   statements from all of your bank accounts to files in formats, known to
   ofxstatement.

2. Run ``ofxstatement`` on each exported file to convert it to standard OFX
   format.  Shell scripts or Makefile may help to automate this routine.

3. Import generated OFX files to GnuCash or other accounting system.


Configuration
=============

Before first use, ofxstatement should be configured to know about particular
format of your statement files. Configuration file is stored in
``~/.config/ofxstatement/config.ini`` and must be created before first use.

Configuration file format is a standard .ini format. Configuration is divided
to sections, that corresponds to ``--type`` command line parameter. Each
section must provide ``plugin`` option that points to one of the registered
conversion plugins. Other parameters are plugin specific.

Sample configuration file::

    [swedbank]
    plugin = swedbank

    [dnb]
    plugin = dnb
    charset = cp1257

Such configuration will let ofxstatement to know about two statement file
format, handled by plugins ``swedbank`` and ``dnb``. ``dnb`` plugin will load
statements using ``cp1257`` charset.

To convert proprietary ``dnb.csv`` to OFX ``dnb.ofx``, run::

    $ ofxstatement -t dnb dnb.csv dnb.ofx

Writing your own plugin
=======================

Statement plugins, included in ofxstatement, are very specific to proprietary
bank formats they are dealing with. This means that, most likely, you will not
find support for your bank' specific format in distribution.  However, it is
easy (for anyone with basic knowledge of programming in python) to add support
for converting of almost any proprietary bank statement format to standard OFX
representation.

Creation of new plugin involves the following steps:

1. Create ``StatementParser`` class in
   ``src/ofxstatement/plugins/yourformat.py``, that will be responsible for
   reading statement file and extracting information from it;

2. Create ``Plugin`` class in ``src/ofxstatement/plugins/yourformat.py``, that
   will configure the parser according to user settings;

3. Register new plugin by importing it in
   ``src/ofxstatement/plugins/__init__.py``.

``StatementParser`` is the main object that does all the hard work. It has only
one public method: ``parse()``, that should return
``ofxstatement.statement.Statement`` object, filled with data from given input.
The default implementation, however, splits this work into two parts:
``split_records()`` to split the whole file into logical parts, e.g.
transaction records, and ``parse_record()`` to extract information from
individual record. See ``src/ofxstatement/parser.py`` for details. If your
statement' format looks like CSV file, you might find ``CsvStatementParser``
class useful: it simplifies mapping bettween CSV columns and ``StatementLine``
attributes.

``Plugin`` interface consists of ``name`` attribute, by which plugin is
identified in configuration file, and ``get_parser()`` method, that returns
configured StatementParser object for given input filename.

See ``src/ofxstatement/plugins`` for examples.
