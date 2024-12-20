# Read the SOCs from the file
with open('sid_20240919910_soc.txt', 'r') as soc_file:
    socs = soc_file.read().splitlines()

# Open the XML file and read its content
with open('OC_1728570308.xml', 'r') as xml_file:
    xml_content = xml_file.read()

# Iterate over each SOC and search for it in the XML content
for soc in socs:
    if soc in xml_content:
        print(soc)