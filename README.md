sholdr
======

Vague description
-----------------

 - sholdr is (or rather will be) a pocket-size shareholder register, reduced to
   just bare minimum features needed for keeping tabs on the ownership of a
   small private company’s shares over time.
 - The two core concepts are **shares** and **shareholders**. The key point of
   interest is the relationship between the two – the ownership structure at a
   given point in time.
 - Shareholders are also users of the app, with varying rights and authority.
   There will be a distinction at least between admin users and basic users with
   limited rights.
 - Each share may at once be under ownership of no more than one shareholder.
   Changes in the ownership of a share are tracked by recording **transactions**
   where shares change hands.
 - Typically shares are owned and traded in large numbers. To avoid massive and
   unnecessary data, ownership and transactions are not recorded for each share
   individually, but rather for **bundles** of sequentially numbered shares.
 - Clearly, one share can be part of only one bundle at a time. However, since
   the bundles can be split up and/or merged together, _over time_ one share can
   belong to several different bundles, which entails some headache.
 - Finally, each share belongs to a **share class**, which can be used to
   differentiate shares in terms of e.g. ownership rules or privileges. Share
   class can also change throughout a share’s life cycle, typically in conjunction
   with transactions.

Expected features
-----------------

 - User (a.k.a.shareholder) registration, authorization, authentication
 - Listing shares and shareholders, with controls for sorting and filtering
 - "Issuing" (i.e. adding) shares
 - Declaring share classes, associating shares with a class
 - Combining shares into bundles
 - Dividing or combining bundles
 - Recording transactions for share bundles
 - Viewing the transaction history of an individual share or bundle
 - Viewing the ownership history of a shareholder
 - (more to come)
