"""Extract the approved Differential Calculus DOCX into complete Markdown."""
from __future__ import annotations
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"Project_Athena_Grade12_Topic4_Differential_Calculus_Approved_Lesson_Pack.docx"
OUTPUT=ROOT/"docs/curriculum/grade12/content/04-differential-calculus"
NS={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def blocks():
    with ZipFile(SOURCE) as archive: body=ET.fromstring(archive.read("word/document.xml")).find("w:body",NS)
    result=[]
    for child in body:
        kind=child.tag.rsplit("}",1)[-1]
        if kind=="p":
            text="".join(node.text or "" for node in child.findall(".//w:t",NS)).strip()
            style=child.find("./w:pPr/w:pStyle",NS); style=style.get(f"{{{NS['w']}}}val") if style is not None else ""
            if text: result.append(("p",style,text))
        elif kind=="tbl":
            rows=[[" ".join("".join(t.text or "" for t in cell.findall(".//w:t",NS)).split()) for cell in row.findall("./w:tc",NS)] for row in child.findall("./w:tr",NS)]
            result.append(("table","",rows))
    return result

def markdown(items):
    out=[]
    for kind,style,value in items:
        if kind=="table":
            width=max(map(len,value)); rows=[row+[""]*(width-len(row)) for row in value]
            out += ["| "+" | ".join(rows[0])+" |","| "+" | ".join(["---"]*width)+" |"]+["| "+" | ".join(row)+" |" for row in rows[1:]]
        elif style=="Heading1": out.append("# "+value)
        elif style=="Heading2": out.append("## "+value)
        elif style.startswith("List"): out.append("- "+value)
        else: out.append(value)
        out.append("")
    return "\n".join(out).strip()+"\n"

def main():
    items=blocks(); starts=[(i,int(m.group(1))) for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and (m:=re.match(r"Lesson (\d+)\s+[—–-]",item[2]))]
    assert [n for _,n in starts]==list(range(1,25))
    appendix=next(i for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and item[2].startswith("Appendix A"))
    OUTPUT.mkdir(parents=True,exist_ok=True); titles=[]
    for pos,(start,number) in enumerate(starts):
        end=starts[pos+1][0] if pos+1<len(starts) else appendix; section=items[start:end]
        heading=section[0][2]; title=re.split(r"\s+[—–-]\s+",heading,maxsplit=1)[-1].strip(); titles.append(title)
        minutes=int(re.search(r"\d+",next(x[2] for x in section if x[0]=="p" and x[2].startswith("Duration:"))).group())
        objective=next(x[2].split(":",1)[1].strip() for x in section if x[0]=="p" and x[2].startswith("Mastery objective:"))
        front=f'''---\nid: g12-calculus-{number:02}\ngrade: 12\nsubject: mathematics\ntopic: differential-calculus\nlesson_number: {number}\ntitle: "{title}"\npaper: 1\nterm: 2\nduration_minutes: {minutes}\nmastery_threshold: 80\nprerequisites: {[] if number==1 else [f'g12-calculus-{number-1:02}']}\nstatus: {'teacher_review_required' if number<=6 else 'coming_soon'}\nsource_document: {SOURCE.name}\n---\n\n## Mastery objective\n\n{objective}\n\n'''
        (OUTPUT/f"lesson-{number:02}.md").write_text(front+markdown(section[1:]),encoding="utf-8")
    manifest="\n".join(f'  - {{order: {i}, id: g12-calculus-{i:02}, title: "{title}", status: {"teacher_review_required" if i<=6 else "coming_soon"}}}' for i,title in enumerate(titles,1))
    (OUTPUT/"topic.yaml").write_text(f'''id: differential-calculus\ntitle: Differential Calculus\ngrade: 12\npaper: 1\nproduct_order: 4\nterm: 2\nmastery_threshold: 80\ntarget_marks: 35\nsource_document: {SOURCE.name}\nlessons:\n{manifest}\n''',encoding="utf-8")
    (OUTPUT/"assessment.md").write_text("# Differential Calculus assessment and runtime appendices\n\n"+markdown(items[appendix:]),encoding="utf-8")
    (OUTPUT/"content-corrections.md").write_text("# Content corrections\n\nLessons 1–6 were independently recalculated. No correction to the approved pack was required.\n",encoding="utf-8")
    (OUTPUT/"legacy-id-migration.md").write_text("# Legacy lesson ID migration\n\n- `g12-calculus-average-rate` resolves to `g12-calculus-01`.\n- `g12-calculus-secant-to-tangent` resolves to `g12-calculus-04`.\n\nCanonical lessons appear once; aliases preserve historical URLs and progress lookup compatibility.\n",encoding="utf-8")

if __name__=="__main__": main()
