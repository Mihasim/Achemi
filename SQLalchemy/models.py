from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship

from config import settings

engine = create_engine(f"postgresql+psycopg2://{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}@"
                       f"{settings.POSTGRESQL_HOSTNAME}/{settings.POSTGRESQL_DATABASE}",
                       echo=True, pool_size=6, max_overflow=10)
engine.connect()
Base = declarative_base()


class Tasks(Base):
    """Мoдель задачи"""
    __tablename__ = "tasks"
    id = Column(Integer(), primary_key=True)
    contestId = Column(Integer(), nullable=False)
    name = Column(String(255), nullable=False)
    tags = relationship("Tags",
                        backref="task_tags",
                        )
    index_task = Column(String(10), nullable=False)
    type = Column(String(255), nullable=False)
    solved_count = Column(Integer())

    def __repr__(self):
        return f"{self.name}"


class Tags(Base):
    """Теги задачи"""
    __tablename__ = 'tags'
    id = Column(Integer(), primary_key=True)
    tag = Column(String(50), nullable=False)
    task_id = Column(Integer(), ForeignKey('tasks.id'), nullable=False)
    task = relationship("Tasks", overlaps="tags,task_tags")

    def __repr__(self):
        return f"{self.tag}"


def create_tables(): Base.metadata.create_all(engine)
def drop_tables(): Base.metadata.drop_all(engine)


#drop_tables()
create_tables()
