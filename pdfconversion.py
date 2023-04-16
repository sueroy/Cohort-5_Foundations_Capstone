import csv
from fpdf import FPDF

def pdf_conv_alluser_results():

    data = []
    with open('all_user_results.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    pdf = FPDF()
    pdf.add_page(orientation='L')

    pdf.set_font("Arial", size=8)
    col_widths = [60,35,20,35,35,45,45,40,20]
 
    for row in data:
        pdf.cell(col_widths[0], 10, row[0], align='C',border=1)
        pdf.cell(col_widths[1], 10, row[1], align='C',border=1)
        pdf.cell(col_widths[2], 10, row[2], align='C',border=1)
        pdf.cell(col_widths[3], 10, row[3], align='C',border=1)
        pdf.cell(col_widths[4], 10, row[4], align='C',border=1)
        pdf.cell(col_widths[5], 10, row[5], align='C',border=1)
        pdf.cell(col_widths[6], 10, row[6], align='C',border=1)
        pdf.cell(col_widths[7], 10, row[7], align='C',border=1)
        pdf.cell(col_widths[8], 10, row[8], align='C',border=1)
        pdf.cell(col_widths[9], 10, row[9], align='C',border=1)
        pdf.ln()

    pdf.output("alluser_results.pdf")