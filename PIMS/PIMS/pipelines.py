import os
from re import findall
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from sqlmodel import Session, create_engine, select
from PIMS.models import Product, Base


"""
| Erweitert die ImagesPipeline von Scrapy mit
| benutzerdefinierten Funktionen.
"""
class ImagePipeline(ImagesPipeline):

    """
    | @Param: Request -> Produktseite mit sämtlichen Informationen
    | @Param: Item -> Produkt mit sämtlichen Attributen
    | @Return: Dateipfad für die erstellten Bilder
    | 
    | Die Methode file_path erzeugt einen Dateipfad für alle erhaltenen Bilder.
    """
    def file_path(self, request, response=None, info=None, item=None):
        return item['id'] + '/' + os.path.basename(urlparse(request.url).path) 


"""
| Die Klasse DatabasePipeline ist eine benutzerdefinierte Pipeline, 
| welche zur Verwaltung (hinzufügen, aktualisieren) von Produkte dient.
"""
class DatabasePipeline:

    """
    | Bei der initialiseren der Klasse ProductPipeline wird die
    | Methode __init__ aufgerufen, welche eine Verbindung zur Datenbank
    | aufbaut und alle Entitäten erstellt. 
    """
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pims')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)

    """
    | @Param: Item -> Überprüfendes Produkt
    | @Return: True -> Produkt existiert
    | @Return: False -> Produkt existiert nicht
    | 
    | Diese Methode überprüft ob ein gegebenes Produkt bereits in 
    | Datenbank existiert.
    """
    def check_item(self, item):
        result = self.session.exec(select(Product).where(Product.id == item['id'])).first()
        if result is None: return True
        else: return False

    """
    | @Param: Item -> Aktualisierendes Produkt
    | 
    | Bei einem bereits vorhandenen Produkt werden alle Werte aktualisiert und gespeichert.
    """
    def update_item(self, item):
        pro = self.session.exec(select(Product).where(Product.id == item['id'])).one()
        pro.brand = item['brand']
        pro.title = item['title']
        pro.price = item['price']
        pro.size = item['size']
        pro.unit = item['unit']
        pro.time = item['time']
        pro.short_description = item['short_description']
        pro.description = item['description']
        pro.recommendation = item['recommendation']
        pro.composition = item['composition']    
        pro.usage = item['usage']
        pro.safety = item['safety']
        pro.recommendation_title = item['recommendation_title']
        pro.composition_title = item['composition_title']
        pro.usage_title = item['usage_title']
        pro.safety_title = item['safety_title']
        pro.short_description_html = item['short_description_html']
        pro.description_html = item['description_html']
        pro.recommendation_html = item['recommendation_html']
        pro.composition_html = item['composition_html']
        pro.usage_html = item['usage_html']
        pro.safety_html = item['safety_html']
        self.session.add(pro)
        self.session.commit()
        self.session.refresh(pro)

    """
    | @Param: Item -> Hinzufügendes Produkt
    | 
    | Es wird ein neues Produkt erstellt und in die Datenbank hinzugefügt.
    """
    def insert_item(self, item):
        self.session.add(
            Product(
                brand = item['brand'],
                id = item['id'], 
                title = item['title'],
                price = item['price'],
                size = item['size'],
                unit = item['unit'],
                time = item['time'],
                short_description = item['short_description'],
                description = item['description'],
                recommendation = item['recommendation'],
                composition = item['composition'],
                usage = item['usage'],
                safety = item['safety'],
                recommendation_title = item['recommendation_title'],
                composition_title = item['composition_title'],
                usage_title = item['usage_title'],
                safety_title = item['safety_title'],
                short_description_html = item['short_description_html'],
                description_html = item['description_html'],
                recommendation_html = item['recommendation_html'],
                composition_html = item['composition_html'],
                usage_html = item['usage_html'],
                safety_html = item['safety_html'],
            )
        )
        self.session.commit()

    """
    | @Param: Item -> Erhaltenes Produkt mit sämtlichen Attributen
    | 
    | Die Methode process_item wird aufgerufen, wenn ein Produkt von
    | einem Spider gespeichert wird -> Beispiel (yield Product).
    | Anschließend wird das Produkt auf Duplizität geprüft und darauf
    | folgend hinzugefügt insert_item oder aktualisiert update_item.
    """
    def process_item(self, item, spider):
        if self.check_item(item) is True:
            self.insert_item(item)
        else:
            self.update_item(item)
        return item


class ProductPipeline:

    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pims')
        self.session = Session(self.engine)

    """
    | @Param: Item -> Erhaltenes Produkt mit sämtlichen Attributen
    | 
    | Die Methode set_item_default setzt alle Werte des übergebenen
    | Item aus einen festgelegten Standartwert.
    """
    def set_default(self, item):
        for field in item.fields:
            item.setdefault(field, None)

    """
    | @Param: Text -> Erhaltener Text mit gegebenen Größen
    | @Return: Liste -> Liefert eine Liste mit allen gefundeten Werten
    | 
    | Die Methode value findet alle float/double Werte aus einem Text und
    | liefert diese zurück für weitere Verwendungen.
    """
    def value(self, text):
        return findall(r'[-+]?(?:\d*\.\d+|\d+)', text.replace(',','.'))

    """
    | @Param: Item -> Erhaltenes Produkt mit sämtlichen Attributen
    | 
    | Die Methode size überprüft ob eine Größe/Einheit gegeben
    | ist und setzt diese Werte dann im Produkt ein.
    """
    def size(self, item):
        if len(self.value(item['size'])) == 1 and self.unit(item['size']) != None:
            item['unit'] = self.unit(item['size'])
            item['size'] = self.value(item['size'])[0]
        else: 
            item['unit'] = None
            item['size'] = None

    """
    | @Param: Unit -> Überprüfender Text mit Einheit
    | @Return: Einheit -> Einheit die im Text gefunden wurde
    | @Return None -> Keine Einheit gefunden
    | 
    | Die Methode überprüft ob eine Einheit im Text gegeben
    | ist.
    """
    def unit(self, unit):
        for txt in unit.lower().split():
            if txt == 'l': return 'Liter'
            if txt == 'liter': return 'Liter'
            if txt == 'ml': return 'Milliliter'
            if txt == 'milliliter': return 'Milliliter'
            if txt == 'kg': return 'Kilogramm'
            if txt == 'kilogramm': return 'Kilogramm'
            if txt == 'g': return 'Gramm'
            if txt == 'gramm': return 'Gramm'

    """
    | @Param: Item -> Item mit umzusetzenen Preis 
    | 
    | Die Methode price setzt den Wert auf den gefundenen
    | double/float Wert vom Produkt.
    """
    def price(self, item):
        item['price'] = self.value(item['price'])[0]

    def category(self, item):
        pass

    """
    | @Param: Item -> Erhaltenes Produkt mit sämtlichen Attributen
    | 
    | Die Methode process_item wird aufgerufen, wenn ein Produkt von
    | einem Spider gespeichert wird -> Beispiel (yield Product).
    | Es werden zuerst alle Standartwerte für ein Produkt erstellt mit
    | dem Aufruf set_item_default.
    | Anschließend werden Preis/Größe/Einheit validiert und gespeichert.
    """
    def process_item(self, item, spider):
        self.set_default(item)
        self.price(item)
        self.size(item)
        return item