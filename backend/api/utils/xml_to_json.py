import xml.etree.ElementTree as ET
import json

def xml_string_to_json(xml_string):
    try:
        root = ET.fromstring(xml_string)
        def parse_element(element):
            # Parse XML element into a dictionary
            if len(element) == 0:
                return element.text
            return {child.tag: parse_element(child) for child in element}

        json_data = parse_element(root)
        return json.dumps(json_data, ensure_ascii=False, indent=4)
    except ET.ParseError as e:
        return json.dumps({'error': f'XML Parse Error: {str(e)}'}, ensure_ascii=False)