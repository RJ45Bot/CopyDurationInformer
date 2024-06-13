import json
class Device:
    def __init__(self, model, OS, time_duration):
        self.model = model
        self.OS = OS
        self.time_duration = time_duration

class Brand:
    def __init__(self, brand_name):
        self.brand_name = brand_name
        self.devices = []

    def add_device(self, model, OS, time_duration):
        self.devices.append(Device(model, OS, time_duration))

def loadData():
    with open('data.json', 'r') as file:
        data_list = json.load(file)

    brands_list = []
    for data in data_list:
        brand_name = data['Brands']
        model = data['Device']
        OS = data['Os']
        time_duration = data['Time']

        brand_obj = next((b for b in brands_list if b.brand_name == brand_name), None)

        if brand_obj is None:
            brand_obj = Brand(brand_name)
            brands_list.append(brand_obj)

        brand_obj.add_device(model, OS, time_duration)

    brands = [brand.brand_name for brand in brands_list]
    models = {brand.brand_name: [device.model for device in brand.devices] for brand in brands_list}
    os = {device.model: device.OS for brand in brands_list for device in brand.devices}
    durations = {device.model: device.time_duration for brand in brands_list for device in brand.devices}

    return brands, models, os, durations, brands_list, data_list


