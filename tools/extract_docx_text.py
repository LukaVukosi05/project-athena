"""Print terminal-readable paragraphs and tables from a DOCX for source audit."""
from pathlib import Path
from sys import argv
from xml.etree import ElementTree as ET
from zipfile import ZipFile

NS={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
source=Path(argv[1])
with ZipFile(source) as archive:
    body=ET.fromstring(archive.read("word/document.xml")).find("w:body",NS)
table_number=0
for child in body:
    kind=child.tag.rsplit("}",1)[-1]
    if kind=="p":
        value="".join(node.text or "" for node in child.findall(".//w:t",NS)).strip()
        style=child.find("./w:pPr/w:pStyle",NS)
        style=style.get(f"{{{NS['w']}}}val") if style is not None else "Paragraph"
        if value: print(f"[{style}] {value}")
    elif kind=="tbl":
        table_number+=1; print(f"\n[TABLE {table_number}]")
        for row in child.findall("./w:tr",NS):
            print(" | ".join(" ".join("".join(t.text or "" for t in cell.findall(".//w:t",NS)).split()) for cell in row.findall("./w:tc",NS)))
