import requests
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('22MK5796598D01V6000072.xml')  # Replace 'note.xml' with your file path
root = tree.getroot()
# Define the namespace
namespace = {'ns': 'cdeps:import:messages'}

# Find all <naim> elements inside <body>
gdi_nodes = root.findall('ns:GOOITEGDS', namespace)



result = []
for gdi in gdi_nodes:
    gdi_num = gdi.find('ns:IteNumGDS7', namespace).text if gdi.find('ns:IteNumGDS7', namespace) is not None else ''
    gross_mass = gdi.find('ns:GooDesGDS23', namespace).text if gdi.find('ns:GooDesGDS23', namespace) is not None else ''
    result.append(f"{gdi_num}-{gross_mass}")
break


print("Loop exited after processing the first GOOITEGDS node.")




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

