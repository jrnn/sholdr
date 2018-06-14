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

    GET_SHAREHOLDER_NAMES = "SELECT" \
        " id, name FROM juridical_person" \
        " UNION SELECT id, last_name || ', ' || first_name" \
        " FROM natural_person"

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
            "CALCULATE_SHARE_COMPOSITION" : text(
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
                " c.id, c.first_share, c.last_share, c.share_count,"
                " _s.votes, _sh.name AS owner"
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
                " JOIN ( %s ) _sh"
                " ON _sh.id = c.owner_id"
                " WHERE c.canceled_on IS NULL"
                " ORDER BY c.first_share ASC" % GET_SHAREHOLDER_NAMES
            ),
            "FIND_CURRENT_OWNER" : text(
                "SELECT"
                " c.owner_id AS id, _s.name"
                " FROM certificate c"
                " JOIN ( %s ) _s"
                " ON _s.id = c.owner_id"
                " WHERE c.id = :id" % GET_SHAREHOLDER_NAMES
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
            ),
            "FIND_TRANSACTIONS" : text(
                "SELECT"
                " t.price, t.recorded_on, _s.name AS owner"
                " FROM _transaction t"
                " JOIN ( %s ) _s"
                " ON _s.id = t.shareholder_id"
                " WHERE t.certificate_id = :id"
                " ORDER BY t.recorded_on ASC" % GET_SHAREHOLDER_NAMES
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
            "COUNT_TRANSACTIONS" : text(
                "SELECT"
                " COUNT(*) AS count"
                " FROM ( SELECT id"
                " FROM certificate"
                " WHERE owner_id = :id"
                " UNION SELECT id"
                " FROM _transaction"
                " WHERE shareholder_id = :id ) _s"
            ),
            "FIND_ALL_FOR_DROPDOWN" : text(
                "%s ORDER BY name ASC" % GET_SHAREHOLDER_NAMES
            ),
            "FIND_ALL_FOR_LIST" : text(
                "SELECT"
                " s.id, s.country, _s.name, _s.type_id,"
                " COALESCE(_c.shares, 0) AS share_count"
                " FROM shareholder s"
                " JOIN ( SELECT"
                " id, name, business_id AS type_id"
                " FROM juridical_person"
                " UNION SELECT"
                " id, last_name || ', ' || first_name, nin"
                " FROM natural_person ) _s"
                " ON s.id = _s.id"
                " LEFT JOIN ( SELECT"
                " owner_id AS id, SUM(share_count) AS shares"
                " FROM certificate"
                " WHERE canceled_on IS NULL"
                " GROUP BY owner_id ) _c"
                " ON s.id = _c.id"
                " ORDER BY _s.name ASC"
            )
        }
    }
