from sqlalchemy import text
from engine import engine

#Check the details about this table ->>

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT sql
        FROM sqlite_master
        WHERE type='table' AND name='UserNotes'
    """))
    print(result.scalar())


#Drop and make a new table -->
# with engine.begin() as conn:
#     conn.execute(text(
#         "ALTER TABLE UserNotes RENAME TO UserNotes_old"
#     ))

#     conn.execute(text("""
#         CREATE TABLE UserNotes (
#             id INTEGER NOT NULL PRIMARY KEY,
#             title VARCHAR NOT NULL,
#             created_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
#             mail TEXT,
#             content TEXT
#         )
#     """))

#     conn.execute(text("""
#         INSERT INTO UserNotes (id, title, created_date, mail, content)
#         SELECT id, title, created_date, mail, content
#         FROM UserNotes_old
#     """))

#     conn.execute(text(
#         "DROP TABLE UserNotes_old"
#     ))