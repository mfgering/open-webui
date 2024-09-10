import os
import sys
import xml.etree.ElementTree as ET
import re

docs_dir = os.path.dirname(__file__)

def make_covenants():
    pass

def make_maint():
    with open("dawson/dawson_maintenance.txt", "r") as f:
        # skip the first 2 lines
        f.readline()
        f.readline()
        i = 0
        while (line := f.readline().strip()):
            i += 1
            parts = line.split("|")
            if len(parts) == 5:
                _, item, party, comment, _, = parts
                with open(f"dawson/rag_files/maintenance/maint-{i}.txt", "w") as r:
                    if comment == '':
                        r.write(f"Item: {item}, Responsibility: {party}")
                    else:
                        r.write(f"Item: {item}, Responsibility: {party}, Comment: {comment}")
    pass

def make_rules():
    tree = ET.parse("dawson/dawson_rules.xml")
    root = tree.getroot()
    # Iterate through each <rule> element in the XML
    for rule in root.findall('rule'):
        # Find the <title> and <description> elements
        nbr = rule.find('number').text
        subject = rule.find('subject').text
        text = rule.find('text').text
        with open(f"dawson/rag_files/rules/rule-{nbr}.txt", "w") as r:
            r.write(f"Rule {nbr}: {subject}: {text}")

def make_faqs():
    with open("dawson/dawson_faqs.txt", "r") as f:
        faqs = f.readlines()
        for i,faq in enumerate(faqs):
            fn = f"faq-{i}.txt"
            with open(f"dawson/rag_files/faqs/{fn}", "w") as r:
                r.write(faq)
            print(f"{i}. {faq}")
    pass

if __name__ == "__main__":
    for fn in [make_covenants, make_faqs, make_maint, make_rules]:
        fn()
