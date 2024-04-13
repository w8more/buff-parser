from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, Float

from src.database import metadata, Base



class M9(Base):
    __tablename__ = 'm9'
    name = Column(String, primary_key=True)

    buff_fn = Column(Float, nullable=True)
    steam_fn = Column(Float, nullable=True)

    buff_mw = Column(Float, nullable=True)
    steam_mw = Column(Float, nullable=True)

    buff_ww = Column(Float, nullable=True)
    steam_ww = Column(Float, nullable=True)

    buff_ft = Column(Float, nullable=True)
    steam_ft = Column(Float, nullable=True)

    buff_bs = Column(Float, nullable=True)
    steam_bs = Column(Float, nullable=True)

class Case(Base):
    __tablename__ = 'case'
    name = Column(String, primary_key=True)
    buff_buy = Column(Float, nullable=True)
    buff_sell = Column(Float, nullable=True)
    steam_sell = Column(Float, nullable=True)

    def to_dict(self):
        return {
            "name": self.name,
            "buff_buy": float(self.buff_buy),
            "buff_sell": float(self.buff_sell),
            "steam_sell": float(self.steam_sell)
        }

class LastParsed(Base):
    __tablename__ = 'last_parsed'
    id = Column(Integer, primary_key=True)
    m9 = Column(TIMESTAMP, nullable=True)
    case = Column(TIMESTAMP, nullable=True)