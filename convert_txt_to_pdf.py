from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# Use a font that supports Unicode
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", size=12)

with open("file.txt", "r", encoding="utf-8") as f:
    for line in f:
        pdf.cell(200, 10, txt=line.strip(), ln=True)

pdf.output("file.pdf")

