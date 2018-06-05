"""
    Cache creation and configuration. Cache timeout is quite long (15 minutes),
    but this should not be a problem because the entire cache is flushed at
    every non-read DB operation.
"""

from flask_caching import Cache

def create_cache(app):
    cache = Cache(config = {
        "CACHE_DEFAULT_TIMEOUT" : 900,
        "CACHE_TYPE" : "simple"
    })
    cache.init_app(app)

    with app.app_context():
        cache.clear()

    return cache
