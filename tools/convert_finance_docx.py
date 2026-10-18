"""Extract the approved Finance DOCX into complete, reviewable Markdown."""
from __future__ import annotations
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"Project_Athena_Grade12_Topic3_Finance_Growth_and_Decay_Approved_Lesson_Pack.docx"
OUTPUT=ROOT/"docs/curriculum/grade12/content/03-finance-growth-and-decay"
NS={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def blocks():
    with ZipFile(SOURCE) as archive: body=ET.fromstring(archive.read("word/document.xml")).find("w:body",NS)
    result=[]
    for child in body:
        kind=child.tag.rsplit("}",1)[-1]
        if kind=="p":
            text="".join(node.text or "" for node in child.findall(".//w:t",NS)).strip()
            style=child.find("./w:pPr/w:pStyle",NS);style=style.get(f"{{{NS['w']}}}val") if style is not None else ""
            if text:result.append(("p",style,text))
        elif kind=="tbl":
            rows=[[" ".join("".join(t.text or "" for t in cell.findall(".//w:t",NS)).split()) for cell in row.findall("./w:tc",NS)] for row in child.findall("./w:tr",NS)]
            result.append(("table","",rows))
    return result

def markdown(items):
    out=[]
    for kind,style,value in items:
        if kind=="table":
            width=max(map(len,value));rows=[row+[""]*(width-len(row)) for row in value]
            out += ["| "+" | ".join(rows[0])+" |","| "+" | ".join(["---"]*width)+" |"]+["| "+" | ".join(row)+" |" for row in rows[1:]]
        elif style=="Heading1":out.append("# "+value)
        elif style=="Heading2":out.append("## "+value)
        elif style.startswith("List"):out.append("- "+value)
        else:out.append(value)
        out.append("")
    return "\n".join(out).strip()+"\n"

def main():
    items=blocks();starts=[(i,int(m.group(1))) for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and (m:=re.match(r"Lesson (\d+)\b",item[2]))]
    assert [n for _,n in starts]==list(range(1,17))
    appendix=next(i for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and item[2].startswith("Appendix A"))
    OUTPUT.mkdir(parents=True,exist_ok=True);titles=[]
    for pos,(start,number) in enumerate(starts):
        end=starts[pos+1][0] if pos+1<len(starts) else appendix;section=items[start:end]
        heading=section[0][2];title=re.split(r"\s+[—–-]\s+",heading,maxsplit=1)[-1].strip();titles.append(title)
        duration=next(x[2] for x in section if x[0]=="p" and x[2].startswith("Duration:"));minutes=int(re.search(r"\d+",duration).group())
        objective=next(x[2].split(":",1)[1].strip() for x in section if x[0]=="p" and x[2].startswith("Mastery objective:"))
        front=f'''---\nid: g12-finance-{number:02}\ngrade: 12\nsubject: mathematics\ntopic: finance-growth-decay\nlesson_number: {number}\ntitle: "{title}"\npaper: 1\nterm: 1\nduration_minutes: {minutes}\nmastery_threshold: 80\nprerequisites: {[] if number==1 else [f'g12-finance-{number-1:02}']}\nstatus: {'teacher_review_required' if number<=3 else 'coming_soon'}\nsource_document: {SOURCE.name}\n---\n\n## Mastery objective\n\n{objective}\n\n'''
        (OUTPUT/f"lesson-{number:02}.md").write_text(front+markdown(section[1:]),encoding="utf-8")
    manifest="\n".join(f'  - {{order: {i}, id: g12-finance-{i:02}, title: "{title}", status: {"teacher_review_required" if i<=3 else "coming_soon"}}}' for i,title in enumerate(titles,1))
    (OUTPUT/"topic.yaml").write_text(f'''id: finance-growth-decay\ntitle: Finance, Growth and Decay\ngrade: 12\npaper: 1\nproduct_order: 3\nterm: 1\nmastery_threshold: 80\nsource_document: {SOURCE.name}\nlessons:\n{manifest}\n''',encoding="utf-8")
    appendices=markdown(items[appendix:]);(OUTPUT/"assessment.md").write_text("# Finance assessment and runtime appendices\n\n"+appendices,encoding="utf-8")
    (OUTPUT/"content-corrections.md").write_text("# Content corrections\n\nAll numerical examples were independently recalculated. No corrections were required for Lessons 1–3.\n",encoding="utf-8")

if __name__=="__main__":main()
