from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from typing import Dict

def generate_debate_pdf(filename: str, topic: str, responses: Dict[str, str], verdict: str):
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "ParliAI - Debate Summary Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, " Topic:")
    y -= 20
    for line in topic.split("\n"):
        c.drawString(60, y, line.strip())
        y -= 15

    y -= 10
    for persona, response in responses.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f" {persona}'s Argument:")
        y -= 20
        c.setFont("Helvetica", 11)
        for line in response.split("\n"):
            c.drawString(60, y, line.strip())
            y -= 15
            if y < 100:
                c.showPage()
                y = height - 50

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, " Summary Verdict:")
    y -= 20
    c.setFont("Helvetica", 11)
    for line in verdict.split("\n"):
        c.drawString(60, y, line.strip())
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
