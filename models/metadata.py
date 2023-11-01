from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
metadata = MetaData()

Base: DeclarativeMeta = declarative_base()


