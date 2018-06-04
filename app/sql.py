"""
    This module contains all custom SQL statements. This is just to help
    declutter the code in model classes. Also possible to define different
    statement dictionaries for development vs. production, if the need arises.
"""

from sqlalchemy.sql import text

def get_queries():
    return {
        "SHARE_CLASS" : {},
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
