import argparse
import xml.etree.ElementTree as ET

def parse_input_file(input_file):
    with open(input_file, 'r') as f:
        rows = []
        for line in f:
            if line.strip():  # ignore empty lines
                values = line.strip().split('|')[1:]  # Skip the first empty column
                rows.append(values)
        return rows

def replace_placeholders(template_str, row_data, tag_to_repeat):
    root = ET.fromstring(template_str)
    # Find the repeating block based on the tag_to_repeat
    repeating_block = root.find(f".//{tag_to_repeat}")
    parent = repeating_block.getparent()

    # Remove original repeating block (it's the placeholder)
    parent.remove(repeating_block)

    for row in row_data:
        # Make a deep copy of the repeating block and fill it with row data
        new_block = ET.fromstring(ET.tostring(repeating_block))
        for idx, value in enumerate(row, start=1):
            placeholder = f"CL{idx}"
            for element in new_block.iter():
                if placeholder in element.attrib.get('value', ''):
                    element.set('value', value)
                if element.text and placeholder in element.text:
                    element.text = value
        parent.append(new_block)
    
    return ET.tostring(root, encoding='unicode')

def main(input_file, template_file, output_file, tag_to_repeat):
    # Parse input data
    rows = parse_input_file(input_file)
    
    # Load template XML file
    with open(template_file, 'r') as f:
        template_str = f.read()
    
    # Replace placeholders and create output XML
    output_xml = replace_placeholders(template_str, rows, tag_to_repeat)
    
    # Write the output XML to a file
    with open(output_file, 'w') as f:
        f.write(output_xml)
    
    print(f"XML successfully written to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate XML from template and input file.")
    parser.add_argument('--input', required=True, help="Path to the input .txt file")
    parser.add_argument('--template', required=True, help="Path to the template XML file")
    parser.add_argument('--output', required=True, help="Path to save the generated XML")
    parser.add_argument('--tag', required=True, help="Name of the tag that starts the repeating block")

    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.input, args.template, args.output, args.tag)
