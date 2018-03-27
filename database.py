from sqlalchemy import Column, Integer, String, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class Doc(Base):
    __tablename__ = "document"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(5000), server_default="System Title")
    link = Column(String(1024), server_default="No Link")
    create_time = Column(TIMESTAMP, server_default=func.now())
    update_time = Column(TIMESTAMP, server_default=func.now())
    done = Column(String(255), server_default="N")
    spider_source = Column(String(1024), server_default="No Source")


def configure_orm():
    global engine
    global Session
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False))
    try:
        engine = create_engine("mysql://root:a1b2c3d4e@127.0.0.1:1924/indole?charset=utf8", echo=True)
        Session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine))
    except Exception as e:
        print("初始化数据库出现问题： {}".format(e))


def initdb():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print ("自动生成数据库表出现问题: {}".format(e))


def single(v):
    cnt = engine.execute('select count(*) from document where link=\'' + str(v) + '\'').fetchone()
    if cnt[0] == 0:
        return True
    else:
        return False


configure_orm()

if __name__ == "__main__":
    initdb()
