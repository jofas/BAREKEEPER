from fpdf import FPDF

sender="""\
Company 1
Second Ave 2131
54321 Nowhere
Germany

Tel.: +49 1245 678910
E-Mail: test@company1.de
"""

recipient="""\
Company 2
Main Street 12b
12345 Somewhere
Germany
"""

footer_sender="""\
Company 1
Second Ave 2131
54321 Nowhere
"""

footer_contact="""\
E-Mail: test@company1.de
Tel.: +49 1245 678910
St.-Nr.: ABC/DEFG/HIJK
"""

footer_bank="""\
Commerzbank
IBAN: DE1233212333123332
BIC: SOMEBICXXX
"""

back_addr="Company 1 | Second Ave 2131 | 54321 Nowhere"

class PDF(FPDF):
    def footer(self):
        self.line(20, height - 40, width - 20, height - 40)

        pdf.set_font("OpenSans", size=10)
        self.set_xy(20, height - 38)

        self.multi_cell((width - 40) * 0.33, lh, txt=footer_sender, ln=3)
        self.multi_cell((width - 40) * 0.33, lh, txt=footer_contact, ln=3)
        self.multi_cell((width - 40) * 0.33, lh, txt=footer_bank, ln=3)


width = 210
height = 297

lh = 4.6

pdf = PDF()

pdf.add_font("OpenSans", fname="fonts/open_sans/static/OpenSans/OpenSans-Regular.ttf", uni=True)
pdf.add_font("OpenSansBold", fname="fonts/open_sans/static/OpenSans/OpenSans-Bold.ttf", uni=True)

pdf.add_page()

pdf.set_margins(left=20, top=20)

pdf.set_font("OpenSans", size=10)

pdf.multi_cell(0, lh, align="R", txt=sender)

pdf.ln(lh)

pdf.set_font("OpenSans", size=8)

pdf.multi_cell(0, lh, txt=back_addr)

pdf.ln(lh)

pdf.set_font("OpenSans", size=10)

pdf.multi_cell(0, lh, txt=recipient)

pdf.ln(lh)

pdf.multi_cell(0, lh, align="R", txt="12. März 2021")

pdf.ln(lh)

pdf.set_font("OpenSansBold", size=16)

pdf.multi_cell(0, lh, align="L", txt="Rechnung Nr. 1")

pdf.ln(lh)

pdf.set_font("OpenSans", size=10)

col_widths = [0.25, 0.6, 0.15]

data = [
    ["01.03.2021", "A work item", "12,99 €"],
    ["02.03.2021 - 12.03.2021", "A second work item", "400,00 €"],
    ["", "Zwischensummer ohne MwSt.", "412.99 €"],
    ["", "19% MwSt.", "78.74 €"],
    ["", "Gesamtbetrag", "491.46 €"],
]

for entry in data:
    for i, c in enumerate(entry):
        pdf.multi_cell(
            (width - 40) * col_widths[i],
            lh,
            align="L",
            txt=str(c),
            border=1,
            ln=3,
        )
    pdf.ln(lh)

pdf.output("test.pdf", "F")
