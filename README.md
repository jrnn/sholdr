sholdr
======

Description
-----------
- **sholdr** is a pocket-size shareholder register, reduced to bare minimum
  features needed for keeping tabs on a small private company’s shares.
- The main purpose is to track ownership structure over time: who owns which
  shares, how much voting power do those shares grant them, who has been selling
  theirs and to whom, and how much money is involved in those transactions.
- To achieve this, roughly, the following features are needed:
  - Adding **shareholders** to the system. Shareholders are also users of the
    app, with different access rights and privileges.
  - Issuing **shares** in large quantities. Shares are a unit of capital that
    quantify ownership between the issuing company and its shareholders.
  - Declaring various **share classes**, which differentiate shares in terms of
    e.g. voting power and other privileges.
  - Bundling subsets of sequentially numbered shares into **share certificates**,
    an instrument of trade and proof of ownership that simplifies bookkeeping.
  - Recording **transactions** where share certificates change hands (for a
    price).
  - ...and finally, being able to handle and track the various changes these
    entities go through over time: shares can be canceled, certificates can be
    split up or merged, share classification can be changed e.g. in conjunction
    with transactions, and so on.

Disclaimer
----------
- sholdr is an exercise project. It is **NOT** intended for "real use", for
  numerous reasons: non-GDPR compliance, naively wasteful data model, zero
  automatic testing... just to name a few.
- If you are looking for a shareholder registry application, turn around right
  now and move on to real, production-grade options.
- If you for whatever inexplicable reason decide to use sholdr for anything, you
  do so at your own personal risk, expense, liability, and headache.

Documentation
-------------
- [Requirements](https://github.com/jrnn/sholdr/blob/master/docs/user_stories.md)
- [Database diagram](https://github.com/jrnn/sholdr/blob/master/docs/db_model.pdf)
- [How to install](https://github.com/jrnn/sholdr/blob/master/docs/installation.md)
- [How to use](https://github.com/jrnn/sholdr/blob/master/docs/manual.md)
- [Few words on technology etc.](https://github.com/jrnn/sholdr/blob/master/docs/specification.md)

It runs on Heroku
-----------------
Click [here](https://sholdr.herokuapp.com/) to see sholdr (demo) in action.
Log in as admin:
        ```
        email : celery@man.io
        password : Qwerty_123
        ```
Log in as basic user:
        ```
        email : chuck@norr.is
        password : Qwerty_123
        ```
