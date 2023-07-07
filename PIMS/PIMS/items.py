from itemloaders.processors import MapCompose as Map
from itemloaders.processors import TakeFirst as First
from itemloaders.processors import Join
from w3lib.html import remove_tags
from scrapy import Item, Field
from bs4 import BeautifulSoup
from re import sub


def check_html(text):

    try:
        soup = BeautifulSoup(text, 'html.parser')
    except: pass

    values = [
        'hr', 'p', 'br', 'strong',
        'ul', 'ol', 'li', 'em',
        'i', 'caption', 'col', 'colgroup',
        'table', 'tbody', 'td', 'tfoot',
        'thead', 'th', 'tr', 'u'
    ]

    for tag in soup.findAll():
        if tag.name not in values:
            tag.unwrap()
        else:
            tag.attrs = {}

    return str(soup)

def check_text(text):
    
    values = [
        '  ', '\n', '\r', '\t', 
        ';', '®', '&amp', '!', 
        '%', '–', '{', '}', 
        '[', ']', '%', '|', 
        '„', '“', '½', '”',
        '—', '‘', '³'
    ]
    
    for x in values: 
        text = text.replace(x, '')
    
    return text

def check_title(text):
    
    values = [
        '  ', '\n', '\r', '\t', 
        ';', '®', '&amp', '!', 
        '%', '–', '{', '}', 
        '[', ']', '%', '|', 
        '„', '“', '½', '”',
        '—', '‘', '³'
    ]
    
    for x in values: 
        text = text.replace(x, '')
    
    return text

def check_id(text):
    values = [' ','\n', '\r', '\t']
    for x in values: text = text.replace(x, '')
    return text

def check_prefix(id, loader_context):
    return loader_context.get('prefix') + id


class Product(Item):
    brand = Field()
    address = Field()
    id = Field(input_processor=Map(remove_tags, check_id, check_prefix), output_processor=First())
    sid = Field(input_processor=Map(remove_tags, check_id), output_processor=First())
    parent = Field(input_processor=Map(remove_tags, check_id, check_prefix), output_processor=First())
    ean = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    title = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    price = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    time = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    size = Field(input_processor=Map(remove_tags, check_text), output_processor=First())
    amount = Field()
    date = Field()
    unit = Field()

    selector = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())

    title_1 = Field()
    title_2 = Field()
    title_3 = Field()
    title_4 = Field()
    title_5 = Field()
    title_6 = Field()

    content_1 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))
    content_2 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))
    content_3 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))
    content_4 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))
    content_5 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))
    content_6 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n\r\t'))

    content_1_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))
    content_2_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))
    content_3_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))
    content_4_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))
    content_5_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))
    content_6_html = Field(input_processor=Map(check_text, check_html), output_processor=Join('\n\r\t'))

    image_urls = Field()
    images = Field()