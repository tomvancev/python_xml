import requests
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('note.xml')  # Replace 'note.xml' with your file path
root = tree.getroot()

# Find all <naim> elements inside <body>
naim_nodes = root.find('body').findall('naim')

# Create strings in the format {num}-{tar}
result = []
for naim in naim_nodes:
    num = naim.find('num').text if naim.find('num') is not None else ''
    tar = naim.find('tar').text if naim.find('tar') is not None else ''
    result.append(f"{num}-{tar}")

# Print the results
    print(" ".join(result))
# url="https://www.dataaccess.com/webservicesserver/NumberConversion.wso"
# #headers = {'content-type': 'application/soap+xml'}
# headers = {'content-type': 'text/xml'}
# dollars = 300
# body =f"""<?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <NumberToDollars xmlns="http://www.dataaccess.com/webservicesserver/">
#       <dNum>{dollars}</dNum>
#     </NumberToDollars>
#   </soap:Body>
# </soap:Envelope>"""

# response = requests.post(url,data=body,headers=headers)
# print (response.content)

