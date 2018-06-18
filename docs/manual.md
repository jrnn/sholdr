How to use sholdr?
------------------

### Logging in, landing
- This should be self-evident. Assumption is that you are operating as admin.
  For the demo version, admin credentials are given at bottom of README.md.
- Once logged in, whether as admin or basic user, you will land on a page that
  shows your own 'Shareholder details'.
- This is a read-only view showing the most important aggregate results of one
  shareholder's current share ownership and past transactions. There is a button
  that opens form view for editing the shareholder's basic information.
- This view is the only thing a basic user is allowed to see. Everything else is
  for admins only.

### Managing shareholders
- The leftmost link in the nav bar says 'Shareholders'. This opens a list view
  of all shareholders.
- In this view, you can either
  - add new shareholders (buttons below list), or
  - go to one shareholder's details (click on list row).
- Adding new shareholders couples as a kind of registration. A password must be
  set, and then the shareholder can access the system using their email and that
  password.
  - (In real life this would be handled e.g. with user verification through
    email, and password reset with a unique token -- but bear with me please)
- The 'details page' of a shareholder is the same as the landing page. Through
  this page, basic information can be edited.
- Each shareholder's basic vs. admin role, and access rights to the application,
  can be adjusted also. The controls are visible only to admin.
- Admin can also delete a shareholder, but only if they have never held shares.

### Managing share classes
- We don't get to shares quite yet. A precondition for issuing shares is that at
  least one share class has been declared.
- Each share belongs to a share class, which is a kind of measure of 'voting
  power': i.e. how many votes does the share grant its owner.
- From the nav bar, pick "Share classes".
- Feel free to add or edit share classes. How this is done should be self-
  explanatory.

### Managing shares
- Now, shares. From nav bar, "Shares". (-Cpt. Obvious)
- There are two key sections on this page: (1) shares, and (2) certificates.
- Let's first look at shares:
  - There's a statement of how many shares have been issued. All further shares
    are issued continuing from that number.
  - In case there are 'unbound' shares, there's an alert in red color listing
    the ranges of such shares. All shares should at all times be 'bundled' into
    share certificates.
  - Then, there's a button for issuing more shares.
- Then for the other section, certificates:
  - There's a list of all currently valid share certificates, with information
    on their share count, owner, and sum voting power.
  - Clicking on a row opens a page with that certificate's details.
  - Below the list is a button for bundling 'unbound' (see above) shares into a
    certificate.
 - Hopefully you can see how the two things on this page relate to one another?

### Issuing shares
- Shares are issued with a simple form.
- On the form, you need to provide:
  - The new 'upper bound'. Shares for all numbers from current upper bound up to
    the new one are issued, in sequence. Obviously the new upper bound must be
    greater than the current number.
  - Date of issue. This obviously cannot be earlier than previous issue date.
  - Share class. All shares in the to-issue range are marked into the selected
    class. If you want to issue several classes, each class requires a separate
    issue.

### Issuing certificates
- Shares are bundled into certificates with a simple form. Precondition is that
  there must be unbound shares (that is, something to bind).
- On the form, you need to provide:
  - Lower and upper bounds of the range to bind. The shares in one certificate
    must form a full, consistent sequence. If there is even one bound share
    within the given range, bundling fails.
  - Date of issue. This cannot conflict with the issue dates and possible prior
    bindings of the constituent shares. It's a somewhat complex check, but don't
    worry about it -- sholdr checks it for you.
  - Initial owner. (This is stupid, because all shares by default initially are
    under the issuing company's control... but whatever...)

### Managing certificate transactions
- Navigate to the page that shows an individual certificate's details.
- Here you can see some key data points, breakdown of shares by class, and full
  transaction history of that one certificate.
- Also, bottom of the page, you have controls for (1) transferring and (2)
  canceling the certificate. Let's look at transfer first.
- Again, a simple form. You need to provide:
  - New owner. Cannot be the same as current owner ('duh).
  - Transaction date. Cannot precede date of the last transaction ('duh').
  - Price. How much did the new owner pay to the current one?
  - Remarks are optional.
- After the transfer is recorded, ownership of the certificate is updated, and
  the relevant transaction appears in the 'details' views of (1) the certificate
  itself, and (2) both shareholders who were part of the transaction.

### Canceling certificates
- Finally, a certificate can be canceled to 'release' its component shares. The
  motivation for doing so typically is either combining two or more certificates
  together, or splitting one certificate further. (Another reason would be
  cancellation of the shares themselves, but sholdr does not yet support this).
- In the cancellation form, you only need to provide the date of cancellation.
- Once a certificate is canceled, you'll notice that the corresponding shares
  appear on the 'Shares' page as an unbound range. You can then bundle them
  again however you like.

### That's it...?
- Yep, that's about it.
