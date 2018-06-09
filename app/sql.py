"""
    This module collects all custom SQL statements into one dictionary, indexed
    by model. Statements are accessed with relevant model name as 1st key, and
    reference to desired statement as 2nd key, e.g. sql["SHARE"]["BIND_RANGE"].
    Minor differences between SQLite in development vs. PostgreSQL in production
    are accounted for.
"""

from sqlalchemy.sql import text



def get_statements(heroku = None):
    FALSE = 0
    TRUE = 1
    if heroku:
        FALSE = "false"
        TRUE = "true"

    return {
        "CERTIFICATE" : {
            "BUNDLE_JOIN" : text(
                "INSERT INTO"
                " certificate_share (share_id, certificate_id)"
                " SELECT s.id, :id"
                " FROM share s"
                " WHERE s.id >= :l AND s.id <= :u"
            )
        },
        "SHARE" : {
            "BIND_RANGE" : text(
                "UPDATE share"
                " SET is_bound = %s"
                " WHERE id >= :l AND id <= :u" % TRUE
            ),
            "FIND_ALL_UNBOUND" : text(
                "SELECT id FROM share"
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
            "COUNT_SHARES_FOR" : text(
                "SELECT"
                " COUNT(*) AS count"
                " FROM share"
                " WHERE share_class_id = :id"
            ),
            "FIND_ALL" : text(
                "SELECT"
                " id, name, votes"
                " FROM share_class"
                " ORDER BY name ASC"
            ),
            "FIND_ALL_FOR_LIST" : text(
                "SELECT"
                " sc.id, sc.name, sc.votes, s.count"
                " FROM share_class sc"
                " JOIN ( SELECT"
                " sc.id, COUNT(s.id) AS count"
                " FROM share_class sc"
                " LEFT JOIN share s"
                " ON sc.id = s.share_class_id"
                " GROUP BY sc.id ) s"
                " ON sc.id = s.id"
                " ORDER BY sc.name ASC"
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
                " j.business_id, j.name,"
                " n.first_name, n.last_name, n.nin,"
                " s.country, s.id, s.type"
                " FROM shareholder s"
                " LEFT JOIN natural_person n"
                " ON s.id = n.id"
                " LEFT JOIN juridical_person j"
                " ON s.id = j.id"
            )
        }
    }
