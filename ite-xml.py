import json
import requests
import xml.etree.ElementTree as ET
from lxml import etree
import html
import re
import argparse
import sys
from datetime import date


today = date.today()

parser = argparse.ArgumentParser(description="This script accepts command-line arguments.")

parser.add_argument('filename', type=str, help="Xml Name")
parser.add_argument('--date', type=str, help="Date of Registration in YYYY-MM-DD format. If left empty it will use today's daye",
                     default= today.strftime("%Y-%m-%d"), required=False)
parser.add_argument('--data', type=str, help="JSON-encoded object for supplementary unit type eg. '[{\"key\":\"54\",\"sup\":\"MTK\"}]'",
                      required=False)
args = parser.parse_args()
sup_data = None
if args.data: 
    try:
        jsondata= json.loads(args.data)
        sup_data = {item["key"]: item for item in jsondata}
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

if not args.date or not args.filename:
    print("Error: Both 'date' and 'filename' are mandatory arguments.")
    sys.exit(1)  # Stop the script with a non-zero exit code (error)


date_sub = args.date #'2023-11-23'
xml_name = args.filename # '22MK5796598D01V6000072'
# Parse the XML file
tree = ET.parse('files\\imd\\' + xml_name + '.xml')  # Replace 'note.xml' with your file path
root = tree.getroot()
# Define the namespace
namespace = {'ns': 'cdeps:import:messages'}

# Find all <naim> elements inside <body>
gdi_nodes = root.findall('ns:GOOITEGDS', namespace)

def createResult(date, currency, items):
   return f"""<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:calc="http://bull.com.pl/calc">
   <soapenv:Header/>
   <soapenv:Body>
      <calc:calculate soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <TARIC_query xsi:type="xsd:string"><![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
			<TARIC_query xmlns="http://bull.com.pl/calc/calcxml" xmlns:xsp="http://apache.org/xsp" xmlns:input="http://apache.org/cocoon/xsp/input/1.0" xmlns:util="http://apache.org/xsp/util/2.0" xmlns:cinclude="http://apache.org/cocoon/include/1.0" xmlns:xsp-request="http://apache.org/xsp/request/2.0" id="SADSCREEN">
				<QINF>
					<transaction Id="T1">T1</transaction>
					<language Id="EN">EN</language>
					<currency Id="MKD">MKD</currency>
				</QINF>
				<SAD>
					<DTE>
						<dat_quest>{date}</dat_quest>
					</DTE>
					<CUR>
						<currency>{currency}</currency>
					</CUR>
					{items}
				</SAD>
				<OPTIONS>
					<forWeb>true</forWeb>
				</OPTIONS>
			</TARIC_query>
			]]></TARIC_query>
      </calc:calculate>
   </soapenv:Body>
</soapenv:Envelope>"""
    

def createGdi(gdi):
    gdi_str = f"""\n\t\t<ITM id="{gdi["num"]}">
            <GDS nbr="{gdi["comm"]}">
                {f"<add_cod>{gdi["add_code"]}</add_cod>" if len(gdi["add_code"]) == 4 else "" }
            </GDS>
            <GEO>
                <geo_area_id>{gdi["area"]}</geo_area_id>
            </GEO>
            <CPC>
                <eu_proc_code>{gdi["proc"]}</eu_proc_code>
                <nat_proc_code>{gdi["nat_proc"]}</nat_proc_code>
            </CPC>
            <PRF>
                <pref_code>{gdi["pref"]}</pref_code>
            </PRF>
            <WGT>
                <net_weight>{gdi["net_mass"]}</net_weight>
                <gr_weight>{gdi["gross_mass"]}</gr_weight>
            </WGT>
            <VAL>
                <customs_value>{gdi["cval"]}</customs_value>
            </VAL>
            <ADD>
                <additional_expenses>{gdi["add_exp"]}</additional_expenses>
            </ADD>"""
    if(gdi["sup"]):
        supl_unit ="NAR"
        if sup_data is not None:
            supl_unit = sup_data.get(gdi["num"])["sup"] if sup_data.get(gdi["num"]) else "NAR"

        gdi_str+= f"""\n\t\t\t<SUP>
                <sup_element>
                    <suppl_unit_code>{supl_unit}</suppl_unit_code> 
                    <suppl_unit_quant>{gdi["sup"]}</suppl_unit_quant> 
                </sup_element>
            </SUP>"""
    gdi_str +=f"""\n\t\t\t{gdi["docs"]}
        </ITM>"""
    return gdi_str

def findNext(gdi, prop, namespace):
    return gdi.find(prop, namespace).text if gdi.find(prop, namespace) is not None else ''

def getRefDocs(gdi):
    proddoc_nodes = gdi.findall('ns:PRODOCDC2', namespace)
    docstring = '<DOC>\n'
    for prododc in proddoc_nodes:
        doctype = prododc.find('ns:DocTypDC21',namespace).text if prododc.find('ns:DocTypDC21',namespace) is not None else ''
        if(len(doctype)!=4):
            continue
        docstring += f'\t\t\t\t<doc_id>{doctype}</doc_id>\n'

    docstring += '\t\t\t</DOC>'
    return docstring

goodsItems = '<ITEMS>'
for gdi in gdi_nodes:
    gdiDict = {
        "num" : findNext(gdi,'ns:IteNumGDS7', namespace),
        "area" : findNext(gdi,'ns:CouOfOriGDI1', namespace),
        "comm" : findNext(gdi,'ns:COMCODGODITM/ns:ComNomCMD1', namespace) + findNext(gdi,'ns:COMCODGODITM/ns:TARCodCMD1', namespace),
        "proc" : findNext(gdi,'ns:ProReqGDI1', namespace) + findNext(gdi,'ns:PreProGDI1', namespace) ,
        "nat_proc" : findNext(gdi,'ns:ComNatProGIM1', namespace),
        "pref" : findNext(gdi,'ns:Pre4046', namespace),
        "net_mass" : findNext(gdi,'ns:NetMasGDS48', namespace),
        "gross_mass" : findNext(gdi,'ns:GroMasGDS46', namespace),
        "cval" : findNext(gdi,'ns:StaValAmoGDI1', namespace),
        "add_exp" : 0,
        "docs" : getRefDocs(gdi),
        "sup": findNext(gdi,'ns:SupUniGDI1', namespace),
        "add_code" : findNext(gdi,'ns:COMCODGODITM/ns:TARFirAddCodCMD1', namespace),
    }
    goodsItems += createGdi(gdiDict)


goodsItems += '\n\t</ITEMS>'

req = createResult(date_sub,'EUR',goodsItems)
with open('files\\req\\req-' + xml_name + '.xml','w') as file:
    file.write(req)


url="http://ite-prod.customs.local:9080/calcxml/services/CalcXml"
headers = {'SOAPAction': 'http://bull.com.pl/calc/calcxml/calcPort/calculateRequest'}

response = requests.post(url,data=req,headers=headers)
res_text = html.unescape(response.text)
pattern = r"(<SAD>.*?</SAD>)"
match =  re.search(pattern, res_text)
if match:
    content = match.group(1)  # Extract the captured content
    root = etree.fromstring(content)
    pretty_xml = etree.tostring(root, pretty_print=True, encoding="unicode")
    with open(f'files\\res\\res-{xml_name}-{date_sub}.xml','w') as file:
        file.write(pretty_xml)
        print(f"Sucess")
else:
    print("No match found.")
