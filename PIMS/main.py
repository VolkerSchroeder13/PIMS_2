import os


for file in os.listdir("C:/Users/Maurice/Desktop/Programmieren/PetVitalShop Project/PIMS/PIMS/spiders"):
    if file.endswith(".py"):
        print(os.path.join(file))
        os.system('python ' + 'PIMS/PIMS/spiders/' + os.path.join(file))

