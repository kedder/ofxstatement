~~~~~~~~~~~~~
OFX Statement
~~~~~~~~~~~~~

.. image:: https://travis-ci.org/kedder/ofxstatement.png?branch=master
    :target: https://travis-ci.org/kedder/ofxstatement
.. image:: https://coveralls.io/repos/kedder/ofxstatement/badge.png?branch=master
    :target: https://coveralls.io/r/kedder/ofxstatement?branch=master

Ofxstatement is a tool to convert proprietary bank statement to OFX format,
suitable for importing to GnuCash. Package provides single command line tool to
run: ``ofxstatement``. Run ``ofxstatement -h`` to see basic usage description.
``ofxstatement`` works under Python 3 and is not compatible with Python 2.


Rationale
=========

Most internet banking systems are capable of exporting account transactions to
some sort of computer readable formats, but few supports standard data formats,
like `OFX`_.  On the other hand, personal accounting tools, such as `GnuCash`_
support standard formats only, and will probably never support proprietary
statement formats of online banking systems.

To bridge the gap between them, ofxstatement tool was created.

.. _GnuCash: http://gnucash.org/
.. _OFX: http://en.wikipedia.org/wiki/Open_Financial_Exchange

Mode of Operation
=================

The ``ofxstatement`` tool is intended to be used in the following workflow:

1. At the end of each month, use your online banking service to export
   statements from all of your bank accounts to files in formats, known to
   ofxstatement.

2. Run ``ofxstatement`` on each exported file to convert it to standard OFX
   format.  Shell scripts or Makefile may help to automate this routine.

3. Import generated OFX files to GnuCash or other accounting system.

Installation and Usage
======================

Before using ``ofxstatement``, you have to install plugin for your bank (or
write your own!). Plugins are installed as regular python eggs, with
easy_install or pip, for example::

  $ pip3 install ofxstatement-lithuanian

Note, that ofxstatement itself will be installed automatically this way. After
installation, ``ofxstatement`` utility should be available.

Users of *Ubuntu* and *Debian* operating systems can install ofxstatement from 
official package repositories::

  $ apt install ofxstatement ofxstatement-plugins 

You can check ofxstatement is working by running::

  $ ofxstatement list-plugins

You should get a list of your installed plugins printed.

After installation, usage is simple::

  $ ofxstatement convert -t <plugin> bank_statement.csv statement.ofx

Resulting ``statement.ofx`` is then ready to be imported to GnuCash or other
financial program you use.


Known Plugins
=============

There are several user-developed plugins available:

================================= ============================================
Plugin                            Description
================================= ============================================
`ofxstatement-lithuanian`_        Plugins for several banks, operating in
                                  Lithuania: Swedbank, Danske and common Lithuanian exchange format - LITAS-ESIS.

`ofxstatement-czech`_             Plugin for Poštovní spořitelna
                                  (``maxibps``) and banks using GPC
                                  format (e.g., FIO banka, module
                                  ``gpc``).

`ofxstatement-airbankcz`_         Plugin for Air Bank a.s. (Czech Republic)
`ofxstatement-raiffeisencz`_      Plugin for Raiffeisenbank a.s. (Czech Republic)
`ofxstatement-unicreditcz`_       Plugin for UniCredit Bank Czech Republic and Slovakia
`ofxstatement-otp`_               Plugin for OTP Bank, operating in Hungary
`ofxstatement-bubbas`_            Set of plugins, developed by @bubbas:
                                  ``dkb_cc`` and ``lbbamazon``.

`banking.statements.osuuspankki`_ Finnish Osuuspankki bank
`banking.statements.nordea`_      Nordea bank (at least Finnish branch of it)
`ofxstatement-germany`_           Plugin for several german banks (1822direkt and Postbank at the moment)
`ofxstatement-austrian`_          Plugins for several banks, operating in Austria:
                                  Easybank, ING-Diba, Livebank, Raiffeisenbank.
`ofxstatement-postfinance`_       Swiss PostFinance (E-Finance Java text based bank/credit statements).
`ofxstatement-mbank-sk`_          MBank.sk
`ofxstatement-be-keytrade`_       KeytradeBank (Belgium)
`ofxstatement-be-ing`_            ING (Belgium)
`ofxstatement-be-kbc`_            KBC (Belgium)
`ofxstatement-be-argenta`_        Argenta (Belgium)
`ofxstatement-betterment`_        Betterment (https://www.betterment.com/)
`ofxstatement-simple`_            Simple (the bank, https://www.simple.com/) JSON financial statement format
`ofxstatement-latvian`_           Latvian banks
`ofxstatement-iso20022`_          Support for generic ISO-20022 format
`ofxstatement-seb`_               SEB (Sweden), it parses Export.xlsx for private accounts
`ofxstatement-alfabank`_          AlfaBank (Russia), it parses movementList.csv for private accounts
`ofxstatement-paypal`_            PayPal, it parses *.csv for private accounts
`ofxstatement-polish`_            Support for some Polish banks and financial institutions
`ofxstatement-russian`_           Support for several Russian banks: Avangard, Tinkoff, Sberbank (debit).
`ofxstatement-dab`_               DAB Bank (Germany)
`ofxstatement-consors`_           Consorsbank (Germany)
`ofxstatement-is-arionbanki`_     Arion bank in Iceland
`ofxstatement-be-triodos`_        Belgian Triodos Bank CSV statements
`ofxstatement-de-triodos`_        German Triodos Bank CSV statements (also works for GLS Bank)
`ofxstatement-lansforsakringar`_  Länsförsäkringar (Sweden), it parses Kontoutdrag.xls for private accounts
`ofxstatement-revolut`_           Revolut Mastercard
`ofxstatement-sp-freiburg`_       Sparkasse Freiburg-Nördlicher Breisgau (Germany)
`ofxstatement-al_bank`_           Arbejdernes Landsbank (Denmark)
`ofxstatement-fineco`_            FinecoBank (Italy)
`ofxstatement-intesasp`_          Intesa San Paolo (xlsx balance file)
`ofxstatement-de-ing`_            Ing Diba Bank (Germany)
`ofxstatement-us-first-republic`_ First Republic Bank (USA)
`ofxstatement-cz-komercni`_       Komerční banka (Czech Republic)
================================= ============================================


.. _ofxstatement-lithuanian: https://github.com/kedder/ofxstatement-lithuanian
.. _ofxstatement-czech: https://gitlab.com/mcepl/ofxstatement-czech
.. _ofxstatement-airbankcz: https://github.com/milankni/ofxstatement-airbankcz
.. _ofxstatement-raiffeisencz: https://github.com/milankni/ofxstatement-raiffeisencz
.. _ofxstatement-unicreditcz: https://github.com/milankni/ofxstatement-unicreditcz
.. _ofxstatement-otp: https://github.com/abesto/ofxstatement-otp
.. _ofxstatement-bubbas: https://github.com/bubbas/ofxstatement-bubbas
.. _banking.statements.osuuspankki: https://github.com/koodaamo/banking.statements.osuuspankki
.. _banking.statements.nordea: https://github.com/koodaamo/banking.statements.nordea
.. _ofxstatement-germany: https://github.com/MirkoDziadzka/ofxstatement-germany
.. _ofxstatement-austrian: https://github.com/nblock/ofxstatement-austrian
.. _ofxstatement-postfinance: https://pypi.python.org/pypi/ofxstatement-postfinance
.. _ofxstatement-mbank-sk: https://github.com/epitheton/ofxstatement-mbank-sk
.. _ofxstatement-be-keytrade: https://github.com/Scotchy49/ofxstatement-be-keytrade
.. _ofxstatement-be-ing: https://github.com/jbbandos/ofxstatement-be-ing
.. _ofxstatement-be-kbc: https://github.com/plenaerts/ofxstatement-be-kbc
.. _ofxstatement-be-argenta: https://github.com/woutbr/ofxstatement-be-argenta
.. _ofxstatement-betterment: https://github.com/cmayes/ofxstatement-betterment
.. _ofxstatement-simple: https://github.com/cmayes/ofxstatement-simple
.. _ofxstatement-latvian: https://github.com/gintsmurans/ofxstatement-latvian
.. _ofxstatement-iso20022: https://github.com/kedder/ofxstatement-iso20022
.. _ofxstatement-seb: https://github.com/themalkolm/ofxstatement-seb
.. _ofxstatement-alfabank: https://github.com/themalkolm/ofxstatement-alfabank
.. _ofxstatement-paypal: https://github.com/themalkolm/ofxstatement-paypal
.. _ofxstatement-polish: https://github.com/yay6/ofxstatement-polish
.. _ofxstatement-russian: https://github.com/gerasiov/ofxstatement-russian
.. _ofxstatement-dab: https://github.com/JohannesKlug/ofxstatement-dab
.. _ofxstatement-consors: https://github.com/JohannesKlug/ofxstatement-consors
.. _ofxstatement-is-arionbanki: https://github.com/Dagur/ofxstatement-is-arionbanki
.. _ofxstatement-be-triodos: https://github.com/renardeau/ofxstatement-be-triodos
.. _ofxstatement-de-triodos: https://github.com/pianoslum/ofxstatement-de-triodos
.. _ofxstatement-lansforsakringar: https://github.com/lbschenkel/ofxstatement-lansforsakringar
.. _ofxstatement-revolut: https://github.com/mlaitinen/ofxstatement-revolut
.. _ofxstatement-sp-freiburg: https://github.com/omarkohl/ofxstatement-sparkasse-freiburg
.. _ofxstatement-al_bank: https://github.com/lbschenkel/ofxstatement-al_bank
.. _ofxstatement-fineco: https://github.com/frankIT/ofxstatement-fineco
.. _ofxstatement-intesasp: https://github.com/Jacotsu/ofxstatement-intesasp
.. _ofxstatement-de-ing: https://github.com/fabolhak/ofxstatement-de-ing
.. _ofxstatement-germany: https://github.com/MirkoDziadzka/ofxstatement-germany
.. _ofxstatement-us-first-republic: https://github.com/medovina/ofxstatement-us-first-republic
.. _ofxstatement-cz-komercni: https://github.com/medovina/ofxstatement-cz-komercni

Advanced Configuration
======================

While ofxstatement can be used without any configuration, some plugins may
accept additional configuration parameters. These parameters can be specified
in configuration file. Configuration file can be edited using ``edit-config``
command, that brings your favored editor with configuration file open::

  $ ofxstatement edit-config

Configuration file format is a standard .ini format. Configuration is divided
to sections, that corresponds to ``--type`` command line parameter. Each
section must provide ``plugin`` option that points to one of the registered
conversion plugins. Other parameters are plugin specific.

Sample configuration file::

    [swedbank]
    plugin = swedbank

    [danske:usd]
    plugin = litas-esis
    charset = cp1257
    currency = USD
    account = LT123456789012345678


Such configuration will let ofxstatement to know about two statement file
format, handled by plugins ``swedbank`` and ``litas-esis``. ``litas-esis``
plugin will load statements using ``cp1257`` charset and set custom currency
and custom account number. This way, GnuCash will automatically associate
imported .ofx statement with particular GnuCash account.

To convert proprietary ``danske.csv`` to OFX ``danske.ofx``, run::

    $ ofxstatement -t danske:usd danske.csv danske.ofx

Note, that configuration parameters are plugin specific. See particular plugin
documentation for more info.

Writing your own Plugin
=======================

If plugin for your bank is not yet developed (see `Known plugins`_ section
above), you can easily write your own, provided some knowledge about python
programming language. There is an `ofxstatement-sample`_ plugin project
available, that provides sample boilerplate and describes plugin development
process in detail.

.. _ofxstatement-sample: https://github.com/kedder/ofxstatement-sample
