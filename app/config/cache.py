"""
    Create and configure cache. Timeout is quite long (15 minutes), but this
    should not be a problem because the entire cache is flushed at every
    non-read DB operation: this is done by defining a 'cache clear + DB commit'
    function, which is then monkey patched to DB instance ( ... :D )
"""

from flask_caching import Cache



def create_cache(app, db):
    cache = Cache(config = {
        "CACHE_DEFAULT_TIMEOUT" : 900,
        "CACHE_TYPE" : "simple"
    })
    cache.init_app(app)

    with app.app_context():
        cache.clear()

    def commit_and_flush_cache():
        cache.clear()
        db.session.commit()

    db.commit_and_flush_cache = commit_and_flush_cache
    return cache
