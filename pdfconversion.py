import csv
from fpdf import FPDF

# Read CSV data into a list
data = []
with open('user_competency.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Create PDF object
pdf = FPDF()
pdf.add_page(orientation='L')

# Set font and font size
pdf.set_font("Arial", size=8)

# Add table to PDF
for row in data:
    for item in row:
        pdf.cell(50, 10, str(item), align= 'C',border=.25)
    pdf.ln()

# Save PDF
pdf.output("output.pdf")