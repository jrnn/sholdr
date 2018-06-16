Some kind of specification or guidelines or whatever ...
--------------------------------------------------------

### Architecture
- sholdr is a simple webapp built on Python Flask framework, following the
  traditional approach (as opposed to SPA) where the server does all the work,
  and returns a full HTML page on each request.

### Code organization
- It should be obvious from looking at the repository subfolders, that the code
  follows a functional structure where modules are organized by what they do.
- Models are grouped in one directory, view blueprints in another, HTML
  templates in yet another, etc.
- On the subfolder level, code is mostly (but not always) arranged according to
  which database entity it deals with.
- The only reason for this kind of layout is personal preference ...

### Configuration
- There is little difference between production vs. development configurations.
- Production is set up to run on [Heroku](https://sholdr.herokuapp.com/), but
  hardly qualifies as "production grade", and the app is not intended for real
  use.
- The only thing that sets some ramifications is that production connects to a
  PostgreSQL database, while locally in dev mode SQLite is used.

### Data access / ORM
- Control of the data tier is graciously delegated to [flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy).
- Simple CRUD involving just one table is done with SQLAlchemy's Query API, but
  for anything beyond that (aggregate and/or join queries) manual SQL statements
  are preferred — with the obvious trade-off of limiting use to SQL only.
- Aim is to confine all DB queries to Model classes, exposed to other parts of
  the application via static methods.

### DTO / validation
- Data transfer and validation between the model layer and users' greasy fingers
  is handled exclusively with [flask-WTF](https://github.com/lepture/flask-wtf).
- Though WTForms ships with a nice set of validators, almost all forms make use
  of one or more custom/tweaked validator classes. (Such a special snowflake!)

### Optimization
- Most DB queries can be quite heavyweight, especially when shares start
  numbering in hundreds of thousands or millions.
- Hence, enter [flask-Caching](https://github.com/sh4nks/flask-caching).
- Caching is not tied to controller endpoints, because this can cause awkward
  side effects such as inadvertently caching flashed messages; instead, caching
  is for most part applied to methods that handle DB queries.
- Entire cache is flushed whenever there's an INSERT, UPDATE, or DELETE query.

### Security
- User session management is handled with [flask-login](https://github.com/maxcountryman/flask-login),
  almost "to-the-letter" as instructed in their documentation.
- Passwords are salted and hashed with [flask-bcrypt](https://github.com/maxcountryman/flask-bcrypt).
- CSRF tokens off-the-shelf with [flask-WTF](https://github.com/lepture/flask-wtf).

### Testing
- There is none...
- sholdr was never intended for "real use", just for getting acquainted with
  Flask. So, no point in investing time and effort here.

### UI and sugarcoating
- [Bootstrap](https://github.com/twbs/bootstrap) out-of-the-box!
- [DataTables](https://github.com/DataTables/DataTables) as well
