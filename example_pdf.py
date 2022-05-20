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

back_addr="Company 1 | Second Ave 2131 | 54321 Nowhere\n\n"

width = 210
height = 297

lh = 5

pdf = FPDF()

pdf.add_page()

pdf.set_margins(left=20, top=40)

pdf.set_font("Helvetica", size=10)

pdf.multi_cell(0, lh, align="R", txt=sender)

# TODO: margin

pdf.set_font("Helvetica", size=8)

pdf.multi_cell(0, lh, align="L", txt=back_addr)


pdf.set_font("Helvetica", size=10)

pdf.multi_cell(0, lh, align="L", txt=recipient)

pdf.multi_cell(0, lh, align="R", txt="12. März 2021\n\n")

pdf.set_font("Helvetica", "B", size=16)

pdf.multi_cell(0, lh, align="L", txt="Rechnung Nr. 1")

# TODO: table (try 10%, 83% 7%)

# TODO: footer

pdf.output("test.pdf", "F")
