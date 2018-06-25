Requirements
------------
The format for "capturing" requirements is the **user story**. Most important
user stories are listed here. The list is not exhaustive, omitting at least some
trivial/must-have stuff (such as login etc.) For some user stories, the relevant
SQL query is given too. (Note that all "manual" SQL statements used in the app
are collected in [one place](https://github.com/jrnn/sholdr/blob/master/app/sql.py)).
Moreover, known issues and development needs are listed here, to some extent.

### User stories (implemented)
As admin, I ...
- can add shareholders (either natural or juridical persons) to the system
- can view and update basic information of a shareholder
- can grant or revoke shareholders access to the system
- can issue shares that are numbered sequentially
- can declare share classes, which determine e.g. the number of votes that a
  share grants to its owner
- can associate shares with a share class
- can bundle an uninterrupted sequence of shares into a share certificate
  ```sql
  INSERT INTO
      certificate_share
      ( share_id, certificate_id )
      SELECT s.id, :id
          FROM share s
          WHERE s.id >= :lower AND s.id <= :upper
  ;
  UPDATE share
      SET is_bound = true
      WHERE id >= :lower AND id <= :upper
  ;
  ```
- can further bundle two or more share certificates into one, provided that the
  resultant certificate also forms an uninterrupted sequence
  - Note : currently can only be done "indirectly" by first canceling the
    certificates and then bundling their shares into a new certificate
- can split up one share certificate into several
  - Note : currently can only be done "indirectly" by first canceling the
    certificate and then bundling its shares into several new certificates
- record transactions where a share certificate moves from the ownership of one
  shareholder to another for some price
- can see the composition of a certificate's shares broken down by class
  ```sql
  SELECT name,
         COUNT(*) AS count,
         SUM(votes) AS votes
      FROM ( SELECT sc.name, sc.votes
             FROM certificate_share cs
             JOIN share s ON s.id = cs.share_id
             JOIN share_class sc ON sc.id = s.share_class_id
             WHERE cs.certificate_id = :id
            ) _s
      GROUP BY name
  ;
  ```
- can view lists of all (1) shareholders, (2) shares, (3) share certificates,
  (4) transactions, and (5) share classes, with sorting and filtering controls
- can see the full ownership and transaction history of any individual share
  certificate or shareholder
  ```sql
  SELECT t.price, t.price_per_share, t.recorded_on,
         _s.name AS seller, _b.name AS buyer
      FROM _transaction t
      JOIN ( SELECT id, name
             FROM juridical_person
             UNION SELECT id, last_name || ', ' || first_name
             FROM natural_person
            ) _s
      ON _s.id = t.seller_id
      JOIN ( SELECT id, name
             FROM juridical_person
             UNION SELECT id, last_name || ', ' || first_name
             FROM natural_person
            ) _b
      ON _b.id = t.buyer_id
      WHERE t.certificate_id = :id
      ORDER BY t.recorded_on ASC
  ;
  ```
- can track down only the transactions to which the issuing entity is a party,
  and the per-share value of those transactions
- can be sure that no certificate is bundled on a such a date as would conflict
  with the original issue date or any prior certificate bindings of any of the
  constituent shares
  ```sql
  SELECT MAX(_s.date) AS max
      FROM ( SELECT MAX(issued_on) AS date
             FROM share
             WHERE id = :upper
             UNION SELECT MAX(c.canceled_on)
             FROM certificate c
             JOIN ( SELECT DISTINCT(certificate_id) AS id
                    FROM certificate_share
                    WHERE share_id >= :lower AND share_id <= :upper
                  ) cs
             ON c.id = cs.id
            ) _s
  ;
  ```

As basic user, I ...
- can view and update my basic information
- can view the share certificates currently under my ownership
- can view the full history of transactions where I either sold or purchased
  share certificates
  ```sql
  SELECT t.price, t.price_per_share, t.recorded_on,
         c.first_share, c.last_share,
         _s.name AS seller, _b.name AS buyer
      FROM _transaction t
      JOIN ( SELECT id, name
             FROM juridical_person
             UNION SELECT id, last_name || ', ' || first_name
             FROM natural_person
            ) _s
      ON _s.id = t.seller_id
      JOIN ( SELECT id, name
             FROM juridical_person
             UNION SELECT id, last_name || ', ' || first_name
             FROM natural_person
            ) _b
      ON _b.id = t.buyer_id
      JOIN certificate c ON c.id = t.certificate_id
      WHERE t.seller_id = :id OR t.buyer_id = :id
      ORDER BY t.recorded_on ASC
  ;
  ```

### User stories (not yet implemented)
As admin, I ...
- can cancel shares, on the condition that they are under ownership of the
  issuing entity
- can produce a report that (1) lists all shareholders (including their basic
  information) in possession of shares, and (2) beneath each shareholder lists
  the share certificates under their ownership, and (3) shows how many votes
  each certificate translates to based on the classification of its shares
- can see a list of only those shareholders who own at least one share of a
  certain share class
- can override the share class of all shares when bundling them into a
  certificate
- can track login and logout events

As basic user, I ...
- can track all changes to my information over time (when and by whom)

### Known development needs
- Functionality is not complete. Remaining user stories should be implemented.
- Data model handles 'Shares' in the most naïve and wasteful way possible — each
  share is a database row(!), causing massive unnecessary data when shares start
  numbering in 10,000s or above. Data model should be adjusted so that the
  trivial 'Share' entity is replaced with something clever — perhaps issue and
  cancel 'Events', or similar, which handle shares not as individuals, but as
  ranges. (This should not be too tricky.)
- Automatic unit and integration tests are missing altogether. If sholdr is to
  be developed further, at least some basic testing is needed, otherwise
  debugging and scaling are a nightmare.
- Verifying new users with a unique token via email; possibility to change one's
  password; etc. rudimentary security stuff.
- Something else still...?
