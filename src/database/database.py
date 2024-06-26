import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker, class_mapper

from .config import settings

logger = logging.getLogger('Database')

engine = create_engine(url=settings.db_url_psycopg2, echo=False)
session_factory = sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
metadata = MetaData()


def reflect_tables():
    with engine.connect() as conn:
        metadata.reflect(bind=conn, only=['sku'], schema='public')

    class SkuTable(Base):
        __table__ = metadata.tables['public.sku']

    return SkuTable


class SKUOperations:
    SkuTable = reflect_tables()

    @classmethod
    def add_sku_data(cls, data_list):
        try:
            with session_factory() as session:
                with session.begin():
                    mapper = class_mapper(cls.SkuTable)
                    session.bulk_insert_mappings(mapper, data_list)
        except SQLAlchemyError as e:
            logger.error(f"Error adding data: {e}")
