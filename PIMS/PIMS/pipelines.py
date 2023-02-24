from PIMS.models import Product, Selector, ProductCategory, Base
from sqlmodel import Session, create_engine, select
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from re import findall
import os


class StoragePipeline(ImagesPipeline):

    """
    | Die Methode file_path erzeugt einen Dateipfad für erhaltende Bilder.
    """
    def file_path(self, request, response=None, info=None, item=None):
        return 'Storage/' + item['id'] + '/' + os.path.basename(urlparse(request.url).path) 


class ExportPipeline(ImagesPipeline):

    """
    | Die Methode file_path erzeugt einen Dateipfad für erhaltende Bilder.
    """
    def file_path(self, request, response=None, info=None, item=None):
        return 'Export/' + item['id'] + '_' + os.path.basename(urlparse(request.url).path) 


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
    | Diese Methode überprüft ob ein gegebenes Produkt bereits in 
    | Datenbank existiert.
    """
    def check_item(self, item):
        result = self.session.exec(select(Product).where(Product.id == item['id'])).first()
        if result is None: 
            return True
        else: 
            return False

    """
    | Bei einem bereits vorhandenen Produkt werden alle Werte aktualisiert und gespeichert.
    """
    def update_item(self, item):
        pro = self.session.exec(select(Product).where(Product.id == item['id'])).one()
        pro.brand = item['brand']
        pro.address = item['address']
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
    | Es wird ein neues Produkt erstellt und in die Datenbank-Tabelle hinzugefügt.
    """
    def insert_item(self, item):
        self.session.add(
            Product(
                brand = item['brand'],
                address = item['address'],
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
    | Die Methode process_item wird aufgerufen, wenn ein Produkt von
    | einem Spider gespeichert wird.
    | Anschließend wird das Produkt auf Duplizität geprüft und gespeichert.
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
    | Diese Methode überprüft ob ein gegebenes Produkt bereits in 
    | Datenbank existiert.
    """
    def check_item(self, item):
        result = self.session.exec(select(Selector).where(Selector.selector == item['selector'])).first()
        if result is None: 
            return True
        else: 
            return False

    """
    | Die Methode set_item_default setzt alle Werte des übergebenen
    | Item aus einen festgelegten Standartwert.
    """
    def set_default(self, item):
        for field in item.fields:
            item.setdefault(field, None)

    """
    | Die Methode value findet alle float/double Werte aus einem Text und
    | liefert diese zurück für weitere Verwendungen.
    """
    def value(self, text):
        return findall(r'[-+]?(?:\d*\.\d+|\d+)', text.replace(',','.'))

    """
    | Die Methode size überprüft ob eine Größe/Einheit gegeben
    | ist und setzt diese Werte dann im Produkt ein.
    """
    def size(self, item):
        if item['size'] == None:
            return

        if len(self.value(item['size'])) == 1 and self.unit(item['size']) != None:
            item['unit'] = self.unit(item['size'])
            item['size'] = self.value(item['size'])[0]
        else: 
            item['unit'] = None
            item['size'] = None

    """
    | Die Methode überprüft ob eine Einheit im Text gegeben
    | ist und gibt diese zurück.
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
    | Die Methode price setzt den Wert auf den gefundenen
    | double/float Wert vom Produkt.
    """
    def price(self, item):
        if item['price'] == None:
            return
        
        item['price'] = self.value(item['price'])[0]

    """
    """
    def selector(self, item):
        if item['selector'] == None:
            return

        if self.check_item(item):
            self.session.add(Selector(brand=item['brand'], selector=item['selector']))
            self.session.commit()

    """
    """
    def category(self, item):
        if item['selector'] == None:
            return
        
        result = self.session.query(Selector).where(
            Selector.selector == item['selector']
        ).where(
            Selector.brand == item['brand']
        ).where(
            Selector.category != None
        ).first()

        if result is not None:
            category = ProductCategory(product=item['id'], category=result.category)
            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)

    """
    | Die Methode process_item wird aufgerufen, wenn ein Produkt von
    | einem Spider gespeichert wird.
    | Danach werden die jeweiligen Methoden zur Validierung der Daten aufgerufen.
    """
    def process_item(self, item, spider):
        self.set_default(item)
        self.price(item)
        self.size(item)
        self.selector(item)
        self.category(item)
        return item