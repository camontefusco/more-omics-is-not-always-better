from pathlib import Path
from docx import Document
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "reviewer_package_anonymized"

def scrub(doc):
    replacements = {
        "Carlos Victor Montefusco-Pereira": "Author information withheld for review",
        "Independent Researcher in Data Science and Artificial Intelligence in Industrial Pharmaceutics": "Affiliation withheld for review",
        "Berlin, Germany": "Location withheld for review",
        "cmontefusco@gmail.com": "email withheld for review",
    }
    for p in list(doc.paragraphs) + [p for t in doc.tables for row in t.rows for c in row.cells for p in c.paragraphs]:
        for run in p.runs:
            for old, new in replacements.items():
                run.text = run.text.replace(old, new)

OUT.mkdir(parents=True, exist_ok=True)
for source, target in [(ROOT/"submission/information_fusion_manuscript_package.docx", OUT/"manuscript_anonymized.docx"), (ROOT/"submission/information_fusion_supplementary.docx", OUT/"supplementary_anonymized.docx")]:
    doc = Document(source); scrub(doc); doc.save(target)
for name in ["highlights.txt", "graphical_abstract.png"]:
    shutil.copy2(ROOT/"submission"/name, OUT/name)
(OUT/"README.txt").write_text("Anonymized reviewer package for Information Fusion. Raw provider data are not included. Derived results, figures, manifests, and code remain available in the private project repository. Author identity, affiliation, location, and email were removed from the Word files.\n")
print(OUT)
