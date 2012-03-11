Tool to convert proprietary bank statement to OFX format, suitable for
importing to GnuCash.

Package provides single command line tool to run: ofxstatement. Run
"ofxstatement -h" to see basic usage description.


Rationale
=========

Most internet banking systems are capable of exporting account transaction to
some sort of computer readable formats, but few supports standard data formats,
like OFX.  On the other hand, personal accounting tools, such as GnuCash
support standard formats only, and will probably never support proprietary
statement formats of online banking systems.

To bridge the gap between them, "ofxstatement" tool was created.


Mode of operation
=================

The "ofxstatement" tool is intended to be used in the following workflow:

  1. At the end of each month, use your online banking service to export
     statements from all of your bank accounts to files in formats, known to
     ofxstatement.

  2. Run "ofxstatement" on each exported file to convert it to standard OFX
     format.  Shell scripts or Makefile may help to automate this routine.

  3. Import generated OFX files to GnuCash or other accounting system.


Configuration
=============

Before first use, ofxstatement should be configured to know about particular
format of your statement files. Configuration file is stored in
~/.config/ofxstatement/config.ini and must be created before first use.

Configuration file format is a standard .ini format. Configuration is divided
to sections, that corresponds to --type command line parameter. Each section
must provide "plugin" option that points to one of the registered conversion
plugins. Other parameters are plugin specific.

Sample configuration file:

    [swedbank]
    plugin = swedbank

    [dnb]
    plugin = dnb
    charset = cp1257

Such configuration will let ofxstatement to know about two statement file
format, handled by plugins "swedbank" and "dnb". "dnb" plugin will load
statements using cp1257 charset.
