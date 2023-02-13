from dotenv import dotenv_values

config = dotenv_values("../../.env")

BOT_NAME = 'PIMS'
SPIDER_MODULES = ['PIMS.spiders']
NEWSPIDER_MODULE = 'PIMS.spiders'

ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'de',
}

ITEM_PIPELINES = {
    'PIMS.pipelines.ProductPipeline': 1,
    'PIMS.pipelines.DatabasePipeline': 300,
    'PIMS.pipelines.ImagePipeline': 300,
}

IMAGES_STORE = config.get('PATH')

