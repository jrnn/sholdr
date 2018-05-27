User stories
------------

As admin, I ...
 - can add shareholders (either natural or juridical persons) to the system
 - can view and update basic information of a shareholder
 - can grant or revoke shareholders access to the system
 - can issue shares that are numbered sequentially
 - can cancel shares, on the condition that they are under ownership of the
   issuing entity
 - can declare share classes, which determine e.g. the number of votes that a
   share grants to its owner
 - can associate shares with a share class
 - can bundle an uninterrupted sequence of shares into a share certificate
 - can further bundle two or more share certificates into one, provided that the
   resultant certificate also forms and uninterrupted sequence
 - can split up one share certificate into several
 - record transactions where a share certificate moves from the ownership of one
   shareholder to another for some price
 - can view lists of all (1) shareholders, (2) shares, (3) share certificates,
   (4) transactions, and (5) share classes, with sorting and filtering controls
 - can see the full ownership and transaction history of any individual share,
   share certificate, and shareholder
 - can track down only the transactions to which the issuing entity is a party,
   and the per-share value of those transactions
 - can produce a report that (1) lists all shareholders (including their basic
   information) in possession of shares, and (2) beneath each shareholder lists
   the share certificates under their ownership, and (3) shows how many votes
   each certificate translates to based on the classification of its shares
 - (can track login and logout events...?)

 As basic user, I ...
  - can view and update my basic information
  - can track all changes to my information over time (when and by whom)
  - can view the share certificates currently under my ownership
  - can view the full history of transactions where I either sold or purchased
    share certificates
