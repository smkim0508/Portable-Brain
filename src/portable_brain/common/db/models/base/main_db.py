from sqlalchemy.orm import DeclarativeBase

# A dedicated Base for all models that map to tables in the main database.
class MainDB_Base(DeclarativeBase):
    pass
