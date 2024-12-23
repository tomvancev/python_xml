import requests
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('22MK5796598D01V6000072.xml')  # Replace 'note.xml' with your file path
root = tree.getroot()
# Define the namespace
namespace = {'ns': 'cdeps:import:messages'}

# Find all <naim> elements inside <body>
gdi_nodes = root.findall('ns:GOOITEGDS', namespace)

def createResult(dict):
    f"""<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:calc="http://bull.com.pl/calc">
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
						<dat_quest>{dict["date"]}</dat_quest>
					</DTE>
					<CUR>
						<currency>{dict["currency"]}</currency>
					</CUR>
					<ITEMS>
						<ITM id="1">
							<GDS nbr="8536909500"/>
							<GEO>
								<geo_area_id>GR</geo_area_id>
							</GEO>
							<CPC>
								<eu_proc_code>4000</eu_proc_code>
								<nat_proc_code>000</nat_proc_code>
							</CPC>
							<PRF>
								<pref_code>300</pref_code>
							</PRF>
							<WGT>
								<net_weight>130.47</net_weight>
								<gr_weight>130.47</gr_weight>
							</WGT>
							<VAL>
								<customs_value>105929.07</customs_value>
							</VAL>
							<ADD>
								<additional_expenses>0</additional_expenses>
							</ADD>
							<DOC>
								<doc_id>6007</doc_id>
							</DOC>
						</ITM>
					</ITEMS>
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
    return f"""<ITM id="{gdi["num"]}">
            <GDS nbr="{gdi["comm"]}"/>
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
            </ADD>
            {gdi["docs"]}
        </ITM>"""

def findNext(gdi, prop, namespace):
    return gdi.find(prop, namespace).text if gdi.find(prop, namespace) is not None else ''

def getRefDocs(gdi):
    return """<DOC>
            <doc_id>6007</doc_id>
        </DOC>"""

goodsItems = '<ITEMS>'
for gdi in gdi_nodes:
    gdiDict = {
        "num" : findNext(gdi,'ns:IteNumGDS7', namespace),
        "area" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "comm" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "proc" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "nat_proc" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "pref" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "net_mass" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "gross_mass" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "cval" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "add_exp" : findNext(gdi,'ns:GooDesGDS23', namespace),
        "docs" : getRefDocs(gdi),
    }
    goodsItems += createGdi(gdiDict)


goodsItems += '</ITEMS>'

print(goodsItems)

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

