import reqs

from typing import Any

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    uid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(5), nullable=False, default='user')
    tickers = Column(String, nullable=True)
    sectors = Column(String, nullable=True)
    threshold = Column(Integer, nullable=False, default=100)
    darkmode = Column(Boolean, nullable=False, default=False)

    def __init__(self, name, username, email, password_hash, role):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def to_dict(self) -> dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "tickers": self.tickers,
            "sectors": self.sectors,
            "threshold": self.threshold,
            "role": self.role,
            "darkmode": self.darkmode
        }

    def to_safe_dict(self) -> dict[str, Any]:
        d = self.to_dict()
        d.pop("password_hash")
        return d


class Repository:
    session: Session
    engine: Engine

    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///users.db')
        Base.metadata.create_all(bind=self.engine)
        session_factory = sessionmaker(bind=self.engine) # Context Management
        self.session = scoped_session(session_factory)()

        if not self.get_user_by_username("master"):
            try:
                self.session.add(User(
                    name="Administrator",
                    username="master",
                    email="master@admin.co.uk",
                    password_hash=reqs.secure_password("root"),
                    role="admin"
                ))
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print(f"Admin seed skipped: {e}")

    def add_user(self, **kwargs) -> None:
        if self.integrity_check(kwargs["uid"], kwargs["email"], kwargs["username"]):
            self.session.add(User(
                name=kwargs["name"],
                username=kwargs["username"],
                email=kwargs["email"],
                password_hash=reqs.secure_password(kwargs["password"]),
                role=kwargs["role"]
            ))
            self.session.commit()
        else:
            print(f"Integrity check failed for {kwargs['uid']} or {kwargs['email']} or {kwargs['username']}.")

    def integrity_check(self, uid, email, username) -> bool:
        return all([
            self.get_user_by_username(username),
            self.get_user_by_email(email),
            self.get_user_by_id(uid)
        ])

    def get_user_by_id(self, uid:int) -> type[User] | None:
        return self.session.query(User).filter(User.uid == uid).one_or_none()

    def get_user_by_username(self, username: str) -> type[User] | None:
        return self.session.query(User).filter(User.username == username).one_or_none()

    def get_user_by_email(self, email: str) -> type[User] | None:
        return self.session.query(User).filter(User.email == email).one_or_none()

    # def get_user_by_username_and_password(self, username: str, password) -> type[User] | None:
    #     user = self.session.query(User).filter(User.username == username).one_or_none()
    #     if user is not None:
    #         if reqs.verify_password(password, user.password_hash):
    #             return user
    #     return None

    def get_all_users(self) -> list[dict[str, Any]]:
        return [user.to_safe_dict() for user in self.session.query(User).all()]

    def update_user(self, uid: int, **kwargs) -> None:
        if "password" in kwargs:
            kwargs["password_hash"] = reqs.secure_password(kwargs.pop("password"))
        self.session.query(User).filter(User.uid == uid).update(kwargs)
        self.session.commit()

    def delete_user(self, uid:int) -> None:
        self.session.query(User).filter(User.uid == uid).delete()
        self.session.commit()