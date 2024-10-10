from sqlalchemy import BigInteger, Integer, create_engine, String, DateTime
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
import datetime
from config import config

DATABASE_URL = f"postgresql://{config['DATA_BASE']['USER']}:{config['DATA_BASE']['PASSWORD']}@{config['DATA_BASE']['IP']}:{config['DATA_BASE']['PORT']}/{config['DATA_BASE']['NAME']}"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class UserCommandLog(Base):
    __tablename__ = "user_command_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(BigInteger)
    command: Mapped[str] = mapped_column(String)
    bot_response: Mapped[str] = mapped_column(String)
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow())

    def add(self):
        with Session(engine) as ses:
            ses.add(self)
            ses.commit()


def manualAdd(userid: int, command: str, bot_response: str):
    UserCommandLog(userid=userid, command=command, bot_response=bot_response).add()


Base.metadata.create_all(engine)
