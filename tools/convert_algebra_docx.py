"""Convert the approved Topic 5 DOCX to reviewable Markdown and runtime JSON."""
from __future__ import annotations
import json, re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"Project_Athena_Grade12_Topic5_Algebra_Equations_and_Inequalities_Approved_Lesson_Pack.docx"
OUTPUT=ROOT/"docs/curriculum/grade12/content/05-algebra-equations-inequalities"
RUNTIME=ROOT/"backend/app/curriculum/grade12/lessons/algebra_pack_data.json"
NS={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
RUNTIME_CORRECTIONS={
    "G12-ALG-L14-P11": "x=(-1+sqrt(33))/2 or x=(-1-sqrt(33))/2; x!=-2.",
}

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

def next_table(items,index):
    return next(value for kind,_,value in items[index+1:] if kind=="table")

def main():
    items=blocks(); starts=[(i,int(m.group(1))) for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and (m:=re.match(r"Lesson (\d+)\s+[—–-]",item[2]))]
    assert [number for _,number in starts]==list(range(1,19))
    tail=next(i for i,item in enumerate(items) if item[0]=="p" and item[1]=="Heading1" and item[2].startswith("5. Topic mastery"))
    OUTPUT.mkdir(parents=True,exist_ok=True); runtime=[]
    for pos,(start,number) in enumerate(starts):
        end=starts[pos+1][0] if pos+1<len(starts) else tail; section=items[start:end]
        title=re.split(r"\s+[—–-]\s+",section[0][2],maxsplit=1)[-1]
        field=next(value for kind,_,value in section if kind=="table" and value and value[0][:2]==["Field","Requirement"])
        meta={row[0]:row[1] for row in field[1:]}
        teaching_index=next(i for i,item in enumerate(section) if item[0]=="p" and item[2]=="Teach the idea before the procedure")
        teaching=next(item[2] for item in section[teaching_index+1:] if item[0]=="p")
        wb_index=next(i for i,item in enumerate(section) if item[0]=="p" and item[2]=="Ten whiteboard examples")
        practice_index=next(i for i,item in enumerate(section) if item[0]=="p" and item[2]=="Twelve self-guided questions")
        wb=next_table(section,wb_index); practice=next_table(section,practice_index)
        assert len(wb)==11 and len(practice)==13
        runtime.append({"number":number,"id":f"g12-algebra-{number:02}","title":title,
          "objective":meta["Mastery objective"],"misconception":meta["Primary misconception"],
          "teaching":teaching,"anchor":next(value[0][0].split("STRUCTURE ANCHOR",1)[-1].strip() for kind,_,value in section if kind=="table" and value and value[0] and value[0][0].startswith("STRUCTURE ANCHOR")),
          "whiteboards":[{"id":row[0],"level":row[1],"prompt":row[2],"answer":row[3]} for row in wb[1:]],
          "practice":[{"id":row[0],"level":row[1],"prompt":row[2],"answer":RUNTIME_CORRECTIONS.get(row[0],row[3])} for row in practice[1:]]})
        front=f'''---\nid: g12-algebra-{number:02}\ngrade: 12\nsubject: mathematics\ntopic: algebra-equations-inequalities\nlesson_number: {number}\ntitle: "{title}"\npaper: 1\nterm: 2\nduration_minutes: 65\nmastery_threshold: 80\nprerequisites: {[] if number==1 else [f'g12-algebra-{number-1:02}']}\nstatus: teacher_review_required\nsource_document: {SOURCE.name}\n---\n\n'''
        (OUTPUT/f"lesson-{number:02}.md").write_text(front+markdown(section[1:]),encoding="utf-8")
    RUNTIME.write_text(json.dumps({"source":SOURCE.name,"lessons":runtime},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest="\n".join(f'  - {{order: {x["number"]}, id: {x["id"]}, title: "{x["title"]}", status: teacher_review_required}}' for x in runtime)
    (OUTPUT/"topic.yaml").write_text(f'''id: algebra-equations-inequalities\ntitle: Algebra, Equations and Inequalities\ngrade: 12\npaper: 1\nproduct_order: 5\nmastery_threshold: 80\nsource_document: {SOURCE.name}\nlessons:\n{manifest}\n''',encoding="utf-8")
    (OUTPUT/"assessment.md").write_text("# Topic mastery and engineering acceptance\n\n"+markdown(items[tail:]),encoding="utf-8")
    (OUTPUT/"content-corrections.md").write_text("""# Content corrections

## G12-ALG-L14-P11

- Source prompt: `Solve 6/(x+2)=x-1.`
- Source answer: `x=2 or x=-3; x!=-2.`
- Corrected runtime answer: `x=(-1+sqrt(33))/2 or x=(-1-sqrt(33))/2; x!=-2.`
- Verification: multiplying by the non-zero denominator gives `6=(x-1)(x+2)`, hence `x^2+x-8=0`. The quadratic formula gives `x=(-1+-sqrt(33))/2`; neither root is the excluded value `-2`.

The review Markdown preserves the source wording. The validated runtime data applies this correction explicitly.
""",encoding="utf-8")

if __name__=="__main__": main()
