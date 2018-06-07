"""
    This module contains all custom SQL statements. The returned 'query
    dictionary' accounts for the minor differences between SQLite in development
    vs. PostgreSQL in production.
"""

from sqlalchemy.sql import text

def get_queries(dialect = None):
    if dialect == "postgresql":
        FALSE = "false"
        TRUE = "true"
    else:
        FALSE = 0
        TRUE = 1

    return {
        "SHARE" : {
            "FIND_ALL_UNBOUND" : text(
                "SELECT"
                " id AS id"
                " FROM share"
                " WHERE is_bound = %s"
                " ORDER BY id ASC" % FALSE
            ),
            "LAST_SHARE_NUMBER" : text(
                "SELECT"
                " MAX(id) AS max"
                " FROM share"
            )
        },
        "SHARE_CLASS" : {
            "FIND_ALL_FOR_DROPDOWN" : text(
                "SELECT"
                " id, name, votes"
                " FROM share_class"
                " ORDER BY name ASC"
            ),
            "FIND_ALL_FOR_LIST" : text(
                "SELECT"
                " share_class.id AS id,"
                " share_class.name AS name,"
                " share_class.votes AS votes,"
                " COUNT(share.id) AS count"
                " FROM share_class"
                " LEFT JOIN share"
                " ON share_class.id = share.share_class_id"
                " GROUP BY name"
            )
        },
        "SHAREHOLDER" : {
            "COUNT_ALL" : text(
                "SELECT"
                " COUNT(*) AS count"
                " FROM shareholder"
            ),
            "FIND_ALL_FOR_LIST" : text(
                "SELECT"
                " juridical_person.business_id,"
                " juridical_person.name,"
                " natural_person.first_name,"
                " natural_person.last_name,"
                " natural_person.nin,"
                " shareholder.country,"
                " shareholder.id,"
                " shareholder.type"
                " FROM shareholder"
                " LEFT JOIN natural_person"
                " ON shareholder.id = natural_person.id"
                " LEFT JOIN juridical_person"
                " ON shareholder.id = juridical_person.id"
            )
        }
    }
