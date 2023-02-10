from itemloaders.processors import MapCompose as Map
from itemloaders.processors import TakeFirst as First
from itemloaders.processors import Join
from w3lib.html import remove_tags
from scrapy import Item, Field


"""
| @Param: Text -> Überprüfender Text vom erhaltenes Produkt
| @Return: Text -> Überarbeiterte Text
| 
| Die Methode check_text entfernt alle unpassenden Daten aus
| den erhaltenen Inhalte.
"""
def check_text(text):
    val = ['  ', '\n', '\r', '\t', '®', '&amp']
    for x in val:
        text = text.replace(x, '')
    return text

"""
| @Param: Item -> Item-Instance von Scrapy
| 
| @Var: Field -> Initialisiert die Variable als Attribut des Items
| @Var: Input_Processor -> Validiert die eingehenden Inhalte
| @Var: Output_Processor -> Definiert wie die Inhalte gespeichert werden
| @Var: MapCompose -> Spezifiziert die Validierung der Inhalte
| @Var: Remove_Tags -> Entfernt alle HTML-Komponenten aus den Inhalten
| @Var: First -> Speichert das erste Element, welches übergeben wird
| @Var: Join -> Speichert alle Elemente, die übergeben werden
| 
| Die Klasse Product erweitert die Item-Instance von Scrapy und wird
| mit dem ItemLoader von Scrapy verwendet. 
"""
class Product(Item):
    brand = Field()
    id = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    title = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    price = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    time = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    size = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    unit = Field()
    selector = Field()

    short_description = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())
    description = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())
    recommendation = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())
    composition = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())
    usage = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())
    safety = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())

    recommendation_title = Field()
    composition_title = Field()
    usage_title = Field()
    safety_title = Field()

    short_description_html = Field(input_processor=Map(check_text), output_processor=Join())
    description_html = Field(input_processor=Map(check_text), output_processor=Join())
    recommendation_html = Field(input_processor=Map(check_text), output_processor=Join())
    composition_html = Field(input_processor=Map(check_text), output_processor=Join())
    usage_html = Field(input_processor=Map(check_text), output_processor=Join())
    safety_html = Field(input_processor=Map(check_text), output_processor=Join())

    image_urls = Field()
    images = Field()