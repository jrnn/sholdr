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

Documentation
-------------
- [User stories](https://github.com/jrnn/sholdr/blob/master/docs/user_stories.md)
- [Database diagram](https://github.com/jrnn/sholdr/blob/master/docs/db_model.pdf)
- [Sorry excuse of a spec](https://github.com/jrnn/sholdr/blob/master/docs/specification.md)

It runs on Heroku
-----------------
Click [here](https://sholdr.herokuapp.com/) to see sholdr in action.
You can log in with:
```
email : celery@man.io
password : Qwerty_123
```
