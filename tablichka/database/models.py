from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, Float, Date

from database.asyn import metadata, Base



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
    m9 = Column(TIMESTAMP(timezone=False), nullable=True)
    case = Column(TIMESTAMP(timezone=False), nullable=True)

class Capsule_quantites(Base):
    __tablename__ = 'capsule_quantites'
    date = Column(Date, primary_key=True)

    paris_2023_challengers_autograph_capsule = Column(Integer, nullable=True)
    paris_2023_contenders_autograph_capsule = Column(Integer, nullable=True)
    paris_2023_legends_autograph_capsule = Column(Integer, nullable=True)
    paris_2023_champions_autograph_capsule = Column(Integer, nullable=True)
    paris_2023_challengers_sticker_capsule = Column(Integer, nullable=True)
    paris_2023_legends_sticker_capsule = Column(Integer, nullable=True)
    paris_2023_contenders_sticker_capsule = Column(Integer, nullable=True)
    antwerp_2022_contenders_sticker_capsule = Column(Integer, nullable=True)
    antwerp_2022_champions_autograph_capsule = Column(Integer, nullable=True)
    antwerp_2022_legends_autograph_capsule = Column(Integer, nullable=True)
    antwerp_2022_contenders_autograph_capsule = Column(Integer, nullable=True)
    antwerp_2022_challengers_autograph_capsule = Column(Integer, nullable=True)
    antwerp_2022_legends_sticker_capsule = Column(Integer, nullable=True)
    antwerp_2022_challengers_sticker_capsule = Column(Integer, nullable=True)
    
    rmr_2020_legends = Column(Integer, nullable=True)
    rmr_2020_challengers = Column(Integer, nullable=True)
    rmr_2020_contenders = Column(Integer, nullable=True)
    
    sticker__9ine__paris_2023 = Column(Integer, nullable=True)