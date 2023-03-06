from PIMS.models import Product, Selector, ProductCategory, Image, Base
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

    def get_image(self, images, index):
        if len(images) > index:
            return images[index]
        else: 
            return None

    def file_path(self, request, response=None, info=None, item=None):
        return 'Export/' + item['id'] + '_' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        images = [x['path'] for ok, x in results if ok]
        
        for i in range(len(images)):
            images[i] = images[i].replace('Export/', '')

        session = Session(create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pims'))
        result = session.exec(select(Image).where(Image.product == item['id'])).first()        

        if result is None:
            session.add(
                Image(
                    product=item['id'],
                    image_1=self.get_image(images, 0),
                    image_2=self.get_image(images, 1),
                    image_3=self.get_image(images, 2),
                    image_4=self.get_image(images, 3),
                    image_5=self.get_image(images, 4),
                    image_6=self.get_image(images, 5),
                    image_7=self.get_image(images, 6),
                    image_8=self.get_image(images, 7),
                    image_9=self.get_image(images, 8),
                    image_10=self.get_image(images, 9),
                    image_11=self.get_image(images, 10),
                    image_12=self.get_image(images, 11)
                )
            )
            session.commit()
        else:
            result.image_1=self.get_image(images, 0)
            result.image_2=self.get_image(images, 1)
            result.image_3=self.get_image(images, 2)
            result.image_4=self.get_image(images, 3)
            result.image_5=self.get_image(images, 4)
            result.image_6=self.get_image(images, 5)
            result.image_7=self.get_image(images, 6)
            result.image_8=self.get_image(images, 7)
            result.image_9=self.get_image(images, 8)
            result.image_10=self.get_image(images, 9)
            result.image_11=self.get_image(images, 10)
            result.image_12=self.get_image(images, 11)

            session.add(result)
            session.commit()
            session.refresh(result)

        return item


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
        result = self.session.exec(select(Product).where(Product.id == item['id'])).one()
        
        result.brand = item['brand']
        result.address = item['address']
        result.title = item['title']
        result.price = item['price']
        result.size = item['size']
        result.unit = item['unit']
        result.time = item['time']
        result.short_description = item['short_description']
        result.description = item['description']
        result.recommendation = item['recommendation']
        result.composition = item['composition']    
        result.usage = item['usage']
        result.safety = item['safety']
        result.recommendation_title = item['recommendation_title']
        result.composition_title = item['composition_title']
        result.usage_title = item['usage_title']
        result.safety_title = item['safety_title']
        result.short_description_html = item['short_description_html']
        result.description_html = item['description_html']
        result.recommendation_html = item['recommendation_html']
        result.composition_html = item['composition_html']
        result.usage_html = item['usage_html']
        result.safety_html = item['safety_html']

        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)

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