from arcgis.geocoding import geocode
from arcgis.gis import GIS
import csv

gis = GIS(api_key="AAPK6dbc98774eea4b54a0e5053458c853a7_JJsyqzpWMnLI2pLC4QhHijixbvTGX0rLjHcDPa8XCGBT9oDIPgrXL-anVMgh9gF")

csv_file = "C:/Users/dgdia/OneDrive/Documentos/GisDay/prueba.csv"  

output_csv_file = "C:/Users/dgdia/OneDrive/Documentos/GisDay/prueba_con_coordenadas.csv" 

geocoded_addresses = []
with open(csv_file, 'r', encoding='latin-1') as file:
    csv_reader = csv.reader(file, delimiter=';')
    original_header = next(csv_reader)
    
    original_header.append("Longitud")
    original_header.append("Latitud")

    original_data = [original_header]
    
    for row in csv_reader:
        original_data.append(row)
for row in original_data[1:]:
    data = row[0]
    
    headers = data.split(';')
    
    departamento = headers[6].strip()  
    municipio = headers[7].strip() 
    address = headers[-1].strip()
    
    result = geocode(address + ", " + municipio + ", " + departamento + ", Colombia")
    if result:
        geocoded_addresses.append(result[0])
for location, row in zip(geocoded_addresses, original_data[1:]):
    if location:
        lat = location['location']['y']
        lon = location['location']['x']
        row[0] += f"; {lon}; {lat}"
    else:
        row[0] += "; NO GEOREFERENCIADO"
with open(output_csv_file, 'w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(original_header)
    csv_writer.writerows(original_data[1:])

map = gis.map("Colombia")
map.center = [4.5709, -74.2973] 

symbol = {
    "type": "esriSMS",
    "style": "esriSMSCircle",
    "color": [0, 0, 255, 128],  # Color azul con transparencia
    "size": 1
}

for location in geocoded_addresses:
    popup = {
        "title": "Dirección Geocodificada",
        "content": location['address']
    }
    map.draw(location['location'], popup)

map