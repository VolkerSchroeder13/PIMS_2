import datetime
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
                    brand=item['brand'],
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
        result.sid = item['sid']
        result.parent = item['parent']
        result.ean = item['ean']
        result.title = item['title']
        result.price = item['price']
        result.size = item['size']
        result.unit = item['unit']
        result.time = item['time']
        result.date = item['date']
        result.title_1 = item['title_1']
        result.title_2 = item['title_2']
        result.title_3 = item['title_3']
        result.title_4 = item['title_4']
        result.title_5 = item['title_5']
        result.title_6 = item['title_6']
        result.content_1 = item['content_1']
        result.content_2 = item['content_2']
        result.content_3 = item['content_3']
        result.content_4 = item['content_4']
        result.content_5 = item['content_5']
        result.content_6 = item['content_6']
        result.content_1_html = item['content_1_html']
        result.content_2_html = item['content_2_html']
        result.content_3_html = item['content_3_html']
        result.content_4_html = item['content_4_html']
        result.content_5_html = item['content_5_html']
        result.content_6_html = item['content_6_html']

        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)

    """
    | Es wird ein neues Produkt erstellt und in die Datenbank-Tabelle hinzugefügt.
    """
    def insert_item(self, item):
        if item['id'] is None:
            return 
        
        self.session.add(
            Product(
                brand = item['brand'],
                address = item['address'],
                id = item['id'],
                sid = item['sid'],
                parent=item['parent'],
                ean = item['ean'],
                title = item['title'],
                price = item['price'],
                size = item['size'],
                unit = item['unit'],
                time = item['time'],
                date = item['date'],
                title_1 = item['title_1'],
                title_2 = item['title_2'],
                title_3 = item['title_3'],
                title_4 = item['title_4'],
                title_5 = item['title_5'],
                title_6 = item['title_6'],
                content_1 = item['content_1'],
                content_2 = item['content_2'],
                content_3 = item['content_3'],
                content_4 = item['content_4'],
                content_5 = item['content_5'],
                content_6 = item['content_6'],
                content_1_html = item['content_1_html'],
                content_2_html = item['content_2_html'],
                content_3_html = item['content_3_html'],
                content_4_html = item['content_4_html'],
                content_5_html = item['content_5_html'],
                content_6_html = item['content_6_html']
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

    
    def check_product(self, item):
        result = self.session.exec(select(Product).where(Product.id == item['id'])).first()
        if result is None: return True
        else: return False

    def check_selector(self, item):
        result = self.session.exec(select(Selector).where(Selector.selector == item['selector'])).first()
        if result is None: return True
        else: return False

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
        text = text.replace(',', '.')
        return findall(r'[-+]?(?:\d*\.\d+|\d+)', text)[0]

    """
    | Die Methode size überprüft ob eine Größe/Einheit gegeben
    | ist und setzt diese Werte dann im Produkt ein.
    """
    def size(self, item):
        if item['size'] is None:
            return

        size = self.value(item['size'])
        unit = self.unit(item['size'])

        if size != None and unit != None:
            item['unit'] = unit
            item['size'] = size
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
        
        item['price'] = self.value(item['price'])

    """
    """
    def date(self, item):
        if item['time'] == None:
            return
        
        result = findall(r'\d{1,2}-\d{1,2}-\d{4}', item['time'])

        if len(result) == 0:
            item['date'] = None
        else:
            date = datetime.datetime.strptime(result[0], '%d-m%-%Y')
            item['date'] = date.strftime('%d.%m.%Y')

    """
    """
    def selector(self, item):
        if item['selector'] == None:
            return

        if self.check_selector(item):
            self.session.add(Selector(brand=item['brand'], selector=item['selector']))
            self.session.commit()

    """
    """
    def category(self, item):
        if item['selector'] == None:
            return
        
        if self.check_product(item):
            return

        result = self.session.query(Selector).where(
            Selector.selector == item['selector']
        ).where(
            Selector.brand == item['brand']
        ).where(
            Selector.category != None
        ).first()

        if result is not None:
            category = ProductCategory(product=item['id'], brand=item['brand'], category=result.category)
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
        self.date(item)
        self.selector(item)
        self.category(item)
        return item