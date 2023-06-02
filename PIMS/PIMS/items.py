from itemloaders.processors import MapCompose as Map
from itemloaders.processors import TakeFirst as First
from itemloaders.processors import Join
from w3lib.html import remove_tags
from scrapy import Item, Field
from re import sub


def check_html(text):
    return sub(r'<(?!p|/p|h[1-6]|/h[1-6]|ul|/ul|ol|/ol|li|/li|u|/u|strong|/strong).*?>','', text)

def check_text(text):
    values = ['  ', '\n', '\r', '\t', ';', '®', '&amp', '!', '%', '–', '{', '}', '[', ']']
    for x in values: text = text.replace(x, '')
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
    date = Field()
    unit = Field()

    selector = Field(input_processor=Map(remove_tags, check_text), output_processor=Join())

    title_1 = Field()
    title_2 = Field()
    title_3 = Field()
    title_4 = Field()
    title_5 = Field()
    title_6 = Field()

    content_1 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))
    content_2 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))
    content_3 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))
    content_4 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))
    content_5 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))
    content_6 = Field(input_processor=Map(remove_tags, check_text), output_processor=Join('\n'))

    content_1_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())
    content_2_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())
    content_3_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())
    content_4_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())
    content_5_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())
    content_6_html = Field(input_processor=Map(check_text, check_html), output_processor=Join())

    image_urls = Field()
    images = Field()