from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Define your PostgreSQL database URL
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdatabase"
#Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# engine = create_engine(
#     'postgresql://username:password@localhost:5432/mydatabase', echo=True, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800,
#     pool_pre_ping=True,
#     connect_args={'options': '-csearch_path=myschema'},
#     isolation_level='AUTOCOMMIT'
# )

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for your models to inherit from
Base = declarative_base()
