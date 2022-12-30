import os

for file in os.listdir("./PIMS/PIMS/spiders"):
    if file.endswith(".py"):
        os.system("cd PIMS && cd PIMS && scrapy crawl " + file.replace('.py', ''))

