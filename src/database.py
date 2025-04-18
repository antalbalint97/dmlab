from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Float, Date, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define base class for SQLAlchemy models
Base: DeclarativeMeta = declarative_base()
metadata = Base.metadata


# Abstract base class for DB models
class DataBase:
    @staticmethod
    def create_table(engine, table_name: str, columns: dict):
        """
        Dynamically create a table given a name and dictionary of column definitions.
        :param engine: SQLAlchemy engine
        :param table_name: Name of the table to create
        :param columns: Dictionary of {column_name: SQLAlchemy Column instance}
        """
        table = Table(
            table_name,
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            *[Column(col_name, *col_args, **col_kwargs) for col_name, (col_args, col_kwargs) in columns.items()],
            extend_existing=True
        )
        print(f"Creating dynamic table: {table_name}")
        metadata.create_all(engine, tables=[table])


def get_engine(echo: bool = False):
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5440")
    db = os.getenv("POSTGRES_DB")

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url, echo=echo)


def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def create_all_tables(engine=None):
    if engine is None:
        engine = get_engine()
    print("Creating all tables defined in Base metadata...")
    Base.metadata.create_all(engine)
