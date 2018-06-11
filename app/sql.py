"""
    This module collects all custom SQL statements into one dictionary, indexed
    by database entity. Statements are accessed with relevant entity name as
    first key, and reference to desired statement as second key, for example
    sql["CERTIFICATE"]["FIND_ALL_FOR_LIST"]. Minor differences between SQLite in
    development vs. PostgreSQL in production are accounted for.
"""

import os
from sqlalchemy.sql import text



def get_statements():
    FALSE = 0
    TRUE = 1
    if os.environ.get("HEROKU"):
        FALSE = "false"
        TRUE = "true"

    """
    Define statements with variable table and/or column references up front as
    functions, so that parameters can be passed to them depending on context.
    """
    def check_if_unique(table_name, column_name):
        return text(
            "SELECT"
            " COUNT(*) AS count"
            " FROM %s"
            " WHERE id != :id"
            " AND %s = :unique_value" % (table_name, column_name,)
        )

    return {
        "_COMMON" : {
            "CHECK_IF_UNIQUE" : check_if_unique
        },
        "CERTIFICATE" : {
            "BUNDLE_JOIN" : text(
                "INSERT INTO"
                " certificate_share (share_id, certificate_id)"
                " SELECT s.id, :id"
                " FROM share s"
                " WHERE s.id >= :l AND s.id <= :u"
            ),
            "CALCULATE_SHARE_COMPOSITION_FOR" : text(
                "SELECT"
                " name, COUNT(*) AS count, SUM(votes) AS votes"
                " FROM ( SELECT"
                " sc.name, sc.votes"
                " FROM certificate_share cs"
                " JOIN share s"
                " ON s.id = cs.share_id"
                " JOIN share_class sc"
                " ON sc.id = s.share_class_id"
                " WHERE cs.certificate_id = :id ) _s"
                " GROUP BY name"
            ),
            "FIND_ALL_FOR_LIST" : text(
                "SELECT"
                " c.id, c.first_share, c.last_share, c.share_count, _s.votes"
                " FROM certificate c"
                " JOIN ( SELECT"
                " cs.certificate_id AS _id, SUM(sc.votes) AS votes"
                " FROM certificate_share cs"
                " JOIN share s"
                " ON s.id = cs.share_id"
                " JOIN share_class sc"
                " ON sc.id = s.share_class_id"
                " GROUP BY _id ) _s"
                " ON c.id = _s._id"
                " WHERE c.canceled_on IS NULL"
                " ORDER BY c.first_share ASC"
            )
        },
        "SHARE" : {
            "BIND_OR_RELEASE_RANGE" : text(
                "UPDATE share"
                " SET is_bound = :is_bound"
                " WHERE id >= :l AND id <= :u"
            ),
#            "BIND_RANGE" : text(
#                "UPDATE share"
#                " SET is_bound = %s"
#                " WHERE id >= :l AND id <= :u" % TRUE
#            ),
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
                " sc.id, sc.name, sc.votes, _s.count"
                " FROM share_class sc"
                " JOIN ( SELECT"
                " sc.id, COUNT(s.id) AS count"
                " FROM share_class sc"
                " LEFT JOIN share s"
                " ON sc.id = s.share_class_id"
                " GROUP BY sc.id ) _s"
                " ON sc.id = _s.id"
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
