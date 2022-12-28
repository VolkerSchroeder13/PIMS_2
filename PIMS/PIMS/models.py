from sqlalchemy import Column, String, Float, Text, Numeric, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


"""
| @Param: Base -> Deklariert die Klasse Produkt als Entität
| 
| Die Klasse repräsentiert die Entität Produkt in der
| gegebenen Datenbank. Die Variablen in der Klasse entsprechen
| den zugehörigen Attributen und deren initialisierten Datentypen.
"""
class Product(Base):
    __tablename__ = "product"
    """
    | @Var: Brand -> Hersteller  [String: Aniforte]
    | @Var: Id -> Produktnummer/SKU  [String: A1000120]
    | @Var: Title -> Produktbezeichnung  [String: Hundefutter]
    | @Var: Price -> Preis  [Float: 15.99]
    | @Var: Time -> Lieferzeit [String: 2-4 Werktage]
    """
    brand = Column(String(255))
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    price = Column(Float)
    size = Column(Numeric(10, 2))
    unit = Column(String(255))
    time = Column(String(255))
    category = Column(Integer)
    """
    | @Var: Shortdescription -> Kurzbeschreibung
    | @Var: Description -> Umfangreiche Beschreibung
    | @Var: Recommendation -> Empfehlungen
    | @Var: Composition -> Zusammensetzung
    | @Var: Usage -> Anwendung
    | @Var: Safety -> Sicherheitshinweise
    """
    short_description = Column(Text)
    description = Column(Text)
    recommendation = Column(Text)
    composition = Column(Text)
    usage = Column(Text)
    safety = Column(Text)
    """
    | @Var: Recommendation Title -> Bezeichnung des Datenfeldes Empfehlungen
    | @Var: Composition Title -> Bezeichnung des Datenfeldes Zusammensetzung
    | @Var: Usage Title -> Bezeichnung des Datenfeldes Anwendung
    | @Var: Safety Title -> Bezeichnung des Datenfeldes Sicherheitshinweise
    """
    recommendation_title = Column(String(255))
    composition_title = Column(String(255))
    usage_title = Column(String(255))
    safety_title = Column(String(255))
    """
    | @Var: Shortdescription HTML -> Kurzbeschreibung in HTML
    | @Var: Description HTML -> Umfangreiche Beschreibung in HTML
    | @Var: Recommendation HTML -> Empfehlungen in HTML
    | @Var: Composition HTML -> Zusammensetzung in HTML
    | @Var: Usage HTML -> Anwendung in HTML
    | @Var: Safety HTML -> Sicherheitshinweise in HTML
    """
    short_description_html = Column(Text)
    description_html = Column(Text)
    recommendation_html = Column(Text)
    composition_html = Column(Text)
    usage_html = Column(Text)
    safety_html = Column(Text)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))

    aniforte = Column(Text)
    agrobs = Column(Text)
    ardapcare = Column(Text)
    ballistol = Column(Text)
    voss = Column(Text)
    waldkraft = Column(Text)