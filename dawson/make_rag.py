import os
import sys
import xml.etree.ElementTree as ET
import re

docs_dir = os.path.dirname(__file__)

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
    curr_nbr = None
    curr_subject = None
    curr_text = []
    rules = []
    with open("dawson/dawson_rules.txt", "r") as f:
        f.readline()
        f.readline()
        rules = f.readlines()
        for i, line in enumerate(rules):
            if m := re.search(r"\*\*(\d+).\s+(.*)\*\*\s*--\s*(.*)", line):
                # check if we've accumulated text from previous rule
                if len(curr_text) > 0:
                    with open(f"dawson/rag_files/rules/rule-{curr_nbr}.txt", "w") as r:
                        r.write(f"RULE {curr_nbr}: Subject: {curr_subject} Text: {' '.join(curr_text)}")
                curr_nbr = m.group(1)
                curr_subject = m.group(2)
                curr_text = [m.group(3)]
            else: 
                curr_text.append(line)
    if len(curr_text) > 0:
        with open(f"dawson/rag_files/rules/rule-{curr_nbr}.txt", "w") as r:
            r.write(f"RULE {curr_nbr}: Subject: {curr_subject} Text: {' '.join(curr_text)}")
    pass

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
    for fn in [make_faqs, make_maint, make_rules]:
        fn()
