from datetime import datetime
from enum import Enum
from typing import Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, Session
)
from sqlalchemy.sql import func


def db_action(_func) -> callable:
    def action(*args, **kwargs):
        if (_ := kwargs.get("db_session")) is None:
            if kwargs.get("server_config") is None:
                raise RuntimeError(
                    f"Calls to database actions must provide a valid ServerConfig. ({_func.__name__})"
                )
            else:
                sc = kwargs.pop("server_config")

            engine = sc.db_engine
            with Session(engine, expire_on_commit=False) as session:
                kwargs["db_session"] = session
                r = _func(*args, **kwargs)
                session.commit()
        else:
            r = _func(*args, **kwargs)
        return r
    return action


class TableNames(Enum):
    F: str = "fs"
    Pin: str = "pins"
    User: str = "users"
    Vote: str = "votes"


class FbotBase(DeclarativeBase):
    pass


class Users(FbotBase):
    __tablename__ = TableNames.User

    uid: Mapped[int] = mapped_column("user_id", primary_key=True, nullable=False)
    created: Mapped[datetime] = mapped_column("created", nullable=False, default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        "last_updated", nullable=False, default=func.now(), onupdate=func.now()
    )

    is_muted: Mapped[bool] = mapped_column("is_muted", nullable=False, default=False)

    fs: Mapped[list["F"]] = relationship()
    pins: Mapped[list["Pins"]] = relationship(foreign_keys="Pins.author_id")
    pinned_messages: Mapped[list["Pins"]] = relationship(foreign_keys="Pins.pinned_by_id")
    votes: Mapped[list["Votes"]] = relationship()

    @staticmethod
    @db_action
    def create_user(user_id: int, db_session: Session = None) -> "Users":
        new_user = Users(uid=user_id)
        db_session.add(new_user)
        return new_user

    @classmethod
    @db_action
    def get_user(cls, user_id: int, db_session: Session = None) -> Self:
        user = db_session.query(cls).filter(Users.uid == user_id).first()
        if not user:
            user = cls.create_user(user_id, db_session=db_session)
        return user

    @db_action
    def get_user_f(self, db_session: Session = None) -> int:
        user_f: int = len(
            db_session.query(F).filter(F.user == self).all()
        )
        return user_f

    @db_action
    def create_f(self, db_session: Session = None) -> Self:
        new_f = F(user_id=self.uid)
        db_session.add(new_f)
        return new_f

    @db_action
    def create_pin(
            self,
            message_id: int,
            message_text: str,
            author_id: int,
            db_session: Session = None
    ) -> Self:
        new_pin = Pins(
            uid=message_id, message_text=message_text, author_id=author_id, pinned_by_id=self.uid
        )
        db_session.add(new_pin)
        return new_pin

    @db_action
    def create_vote(
            self,
            is_up: bool,
            pinned_message_id: int,
            db_session: Session = None
    ) -> Self:
        new_pin = Pins(is_up=is_up, pinned_message_id=pinned_message_id, voter_id=self.uid)
        db_session.add(new_pin)
        return new_pin


class F(FbotBase):
    __tablename__ = TableNames.F

    uid: Mapped[int] = mapped_column("uid", primary_key=True, autoincrement=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column("timestamp", nullable=False, default=datetime.now())

    user_id: Mapped[int] = mapped_column("user_id", ForeignKey(Users.uid), nullable=False)
    user: Mapped[Users] = relationship(foreign_keys=[user_id], back_populates="fs")

    @classmethod
    @db_action
    def get_total_f(cls, db_session: Session = None) -> int:
        total_f: int = len(
            db_session.query(cls).all()
        )
        return total_f


class Pins(FbotBase):
    __tablename__ = "pins"

    uid: Mapped[int] = mapped_column("message_id", primary_key=True, nullable=False)

    timestamp: Mapped[datetime] = mapped_column("timestamp", default=datetime.now())
    message_text: Mapped[str] = mapped_column("text", nullable=False)

    author_id: Mapped[int] = mapped_column("author_id", ForeignKey(Users.uid), nullable=False)
    author: Mapped[Users] = relationship(
        foreign_keys=[author_id], back_populates="pinned_messages", overlaps="pins"
    )

    pinned_by_id: Mapped[int] = mapped_column("pinned_by_id", ForeignKey(Users.uid), nullable=False)
    pinned_by: Mapped[Users] = relationship(
        foreign_keys=[pinned_by_id], back_populates="pins", overlaps="pinned_messages"
    )

    votes: Mapped[list["Votes"]] = relationship()


class Votes(FbotBase):
    __tablename__ = TableNames.Vote

    uid: Mapped[int] = mapped_column("vid", primary_key=True, autoincrement=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column("timestamp", nullable=False, default=datetime.now())

    is_up: Mapped[bool] = mapped_column("is_up", nullable=False)

    pinned_message_id: Mapped[int] = mapped_column("pinned_message_id", ForeignKey(Pins.uid), nullable=False)
    pinned_message: Mapped[Pins] = relationship(foreign_keys=[pinned_message_id], back_populates="votes")

    voter_id: Mapped[int] = mapped_column("voter_id", ForeignKey(Users.uid), nullable=False)
    voter: Mapped[Users] = relationship(foreign_keys=[voter_id], back_populates="votes")
