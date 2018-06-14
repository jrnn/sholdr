"""
    This module collects all custom SQL statements into one dictionary, indexed
    by database entity. Statements are accessed with relevant entity name as
    first key, and reference to desired statement as second key, for example
    sql["CERTIFICATE"]["FIND_ALL_FOR_LIST"].

    Statements with variable table and/or column references are defined 'up
    front' as functions and then passed into the statement dictionary, so that
    the table/column names can be passed as parameters depending on context.
"""

from sqlalchemy.sql import text



def get_statements():
    def check_if_unique(table, column):
        return text(
            "SELECT"
            " COUNT(*) AS count"
            " FROM %s"
            " WHERE id != :id"
            " AND %s = :unique_value" % (table, column,)
        )

    def count_all(table):
        return text(
            "SELECT"
            " COUNT(*) AS count"
            " FROM %s" % table
        )

    def count_where(table, column):
        return text(
            "SELECT"
            " COUNT(*) AS count"
            " FROM %s"
            " WHERE %s = :value" % (table, column,)
        )

    def find_max(table, column):
        return text(
            "SELECT"
            " MAX(%s) AS max"
            " FROM %s" % (column, table,)
        )

    def find_max_where(table, column, where):
        return text(
            "SELECT"
            " MAX(%s) AS max"
            " FROM %s"
            " WHERE %s = :value" % (column, table, where,)
        )

    return {
        "_COMMON" : {
            "CHECK_IF_UNIQUE" : check_if_unique,
            "COUNT_ALL" : count_all,
            "COUNT_WHERE" : count_where,
            "FIND_MAX" : find_max,
            "FIND_MAX_WHERE" : find_max_where
        },
        "CERTIFICATE" : {
            "BUNDLE_JOIN" : text(
                "INSERT INTO"
                " certificate_share (share_id, certificate_id)"
                " SELECT s.id, :id"
                " FROM share s"
                " WHERE s.id >= :lower AND s.id <= :upper"
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
            ),
            "FIND_CURRENT_OWNER" : text(
                "SELECT"
                " id, name"
                " FROM juridical_person"
                " UNION SELECT"
                " id, last_name || ', ' || first_name AS name"
                " FROM natural_person"
                " JOIN ( SELECT"
                " shareholder_id as _id, MAX(recorded_on)"
                " FROM _transaction"
                " WHERE certificate_id = :id ) _s"
                " ON id = _s._id"
            ),
            "FIND_EARLIEST_BUNDLE_DATE" : text(
                "SELECT"
                " MAX(_s.date) AS max"
                " FROM ( SELECT"
                " MAX(issued_on) AS date"
                " FROM share"
                " WHERE id = :upper"
                " UNION SELECT"
                " MAX(c.canceled_on)"
                " FROM certificate c"
                " JOIN ( SELECT"
                " DISTINCT(certificate_id) AS id"
                " FROM certificate_share"
                " WHERE share_id >= :lower AND share_id <= :upper ) cs"
                " ON c.id = cs.id ) _s"
            )
        },
        "SHARE" : {
            "BIND_OR_RELEASE_RANGE" : text(
                "UPDATE share"
                " SET is_bound = :is_bound"
                " WHERE id >= :lower AND id <= :upper"
            ),
            "FIND_ALL_BOUND_OR_UNBOUND" : text(
                "SELECT id FROM share"
                " WHERE is_bound = :is_bound"
                " ORDER BY id ASC"
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
            "FIND_ALL_FOR_DROPDOWN" : text(
                "SELECT"
                " id, name"
                " FROM juridical_person"
                " UNION SELECT"
                " id, last_name || ', ' || first_name AS name"
                " FROM natural_person"
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
