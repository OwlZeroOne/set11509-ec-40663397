import bfaker
from sqlalchemy import create_engine, Column, String, Integer, Float, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Broker(Base):
    __tablename__ = "brokers"

    bid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True, default=None)
    domain = Column(String(50), nullable=False)
    trading_record = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "bid": self.bid,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "domain": self.domain,
            "trading_record": self.trading_record,
            "rating": self.rating,
            "price": self.price
        }

class Repository:
    session: Session
    engine: Engine

    def __init__(self):
        self.engine = create_engine('sqlite:///brokers.db')
        Base.metadata.create_all(bind=self.engine)
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)()

        # Populate database with random, fake, brokers if empty.
        if self.session.query(Broker).count() <= 0:
            self.generate_brokers()

    def add_broker(self, **kwargs):
        broker = Broker(**{k: v for k, v in kwargs.items() if v is not None})
        self.session.add(broker)
        self.session.commit()

    def get_all(self):
        return [broker.to_dict() for broker in self.session.query(Broker).all()]

    def get_all_except(self, domains):
        return [broker.to_dict() for broker in self.session.query(Broker).filter(Broker.domain.notin_(domains)).all()]

    def get_by_domains(self, domains):
        return [broker.to_dict() for broker in self.session.query(Broker).filter(Broker.domain.in_(domains)).all()]

    def generate_brokers(self):
        broker_list: list[dict] = bfaker.generate_brokers(
            locales=['en_GB', 'pl_PL', 'de_DE'],
            count=100
        )
        for broker in broker_list:
            self.add_broker(**broker)


if __name__ == '__main__':
    Repository()