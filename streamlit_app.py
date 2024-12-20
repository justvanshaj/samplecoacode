import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Define the fields for user input
fields_to_fill = {
    "Customer": "",
    "Product": "",
    "Date": "",
    "Batch No.": "",
    "Shelf-life": "",
    "Invoice No.": "",
    "PO No.": "",
    "Gum Content (%)": "",
    "Moisture (%)": "",
    "Protein (%)": "",
    "ASH Content (%)": "",
    "AIR (%)": "",
    "Fat (%)": "",
    "Ph Levels": "",
    "Arsenic": "",
    "Lead": "",
    "Heavy Metals": "",
    "Through 100 Mesh": "",
    "Through 200 Mesh": "",
    "APC/gm": "",
    "Yeast & Mould": "",
    "Coliform": "",
    "Ecoli": "",
    "Salmonella": "",
    "Viscosity After 2 Hours": "",
    "Viscosity After 24 Hours": "",
}

# Custom PDF Class
class COAPDF(FPDF):
    def add_table_row(self, col1, col2, col3=None, col_widths=(60, 60, 50), row_height=6, font_size=8):
        """Add a row to the table with adjustable widths, heights, and font size."""
        self.set_font("Arial", size=font_size)  # Set custom font size

        # Ensure col_widths has enough elements for the columns being used
        if len(col_widths) < 3:
            col_widths = col_widths + (50,) * (3 - len(col_widths))  # Pad to ensure 3 elements

        # Add cells with the specified widths
        self.cell(col_widths[0], row_height, col1, border=1)
        self.cell(col_widths[1], row_height, col2, border=1)
        if col3 is not None:
            self.cell(col_widths[2], row_height, col3, border=1)
        self.ln()

    def add_section_title(self, title, font_size=8, cell_height=10, border=1):
        """Add a section title with customizable font size, cell height, and border."""
        self.set_font("Arial", "B", font_size)  # Set custom font size
        self.cell(0, cell_height, title, border=border, align="C", ln=True)

def create_pdf(data):
    pdf = COAPDF()
    pdf.add_page()

    # Header Rows
    pdf.set_font("Arial", size=8)  # Default font size for header
    pdf.cell(0, 5, f"Customer: {data['Customer']}", border=1, ln=True)

    pdf.cell(60, 5, f"Product: {data['Product']}", border=1)
    pdf.cell(60, 5, f"Date: {data['Date']}", border=1, ln=True)

    pdf.cell(60, 5, f"Batch No.: {data['Batch No.']}", border=1)
    pdf.cell(60, 5, f"Shelf-life: {data['Shelf-life']}", border=1, ln=True)

    pdf.cell(60, 5, f"Invoice No.: {data['Invoice No.']}", border=1)
    pdf.cell(60, 5, f"PO No.: {data['PO No.']}", border=1, ln=True)

    # Parameters Specifications and Results
    pdf.add_section_title("PARAMETERS SPECIFICATIONS TEST RESULTS", font_size=10, cell_height=8)
    table_data = [
        ("Gum Content (%)", "more than 80%", data["Gum Content (%)"]),
        ("Moisture (%)", "less than 12%", data["Moisture (%)"]),
        ("Protein (%)", "less than 5%", data["Protein (%)"]),
        ("ASH Content (%)", "less than 1%", data["ASH Content (%)"]),
        ("AIR (%)", "less than 6%", data["AIR (%)"]),
        ("Fat (%)", "less than 1%", data["Fat (%)"]),
        ("Ph Levels", "5.5 - 7.0", data["Ph Levels"]),
        ("Arsenic", "less than 3.0 mg/kg", data["Arsenic"]),
        ("Lead", "less than 2.0 mg/kg", data["Lead"]),
        ("Heavy Metals", "less than 1.0 mg/kg", data["Heavy Metals"]),
    ]
    for row in table_data:
        pdf.add_table_row(*row, col_widths=(50, 50, 60), row_height=5, font_size=8)

    # Organoleptic Analysis Section
    pdf.add_section_title("ORGANOLEPTIC ANALYSIS", font_size=9, cell_height=6)
    organoleptic_data = [
        ("Appearance/Colour", "Cream/White Powder"),
        ("Odour", "Natural"),
        ("Taste", "Natural"),
    ]
    for parameter, value in organoleptic_data:
        pdf.add_table_row(parameter, value, col_widths=(70, 70), row_height=5)

    # Particle Size and Granulation Section
    pdf.add_section_title("PARTICLE SIZE AND GRANULATION", font_size=9, cell_height=6)
    granulation_data = [
        ("Through 100 Mesh", "99%", data["Through 100 Mesh"]),
        ("Through 200 Mesh", "95%-99%", data["Through 200 Mesh"]),
    ]
    for row in granulation_data:
        pdf.add_table_row(*row, col_widths=(50, 50), row_height=5)

    # Viscosity Section with User Input
    pdf.add_section_title("VISCOSITY", font_size=9, cell_height=6)
    pdf.add_table_row("After 2 hours", ">= BLANK cps", data["Viscosity After 2 Hours"], col_widths=(70, 50, 50))
    pdf.add_table_row("After 24 hours", "<= BLANK cps", data["Viscosity After 24 Hours"], col_widths=(70, 50, 50))

    # Microbiological Analysis Section
    pdf.add_section_title("MICROBIOLOGICAL ANALYSIS", font_size=9, cell_height=6)
    microbiological_data = [
        ("APC/gm", "less than 5000/gm", data["APC/gm"]),
        ("Yeast & Mould", "less than 500/gm", data["Yeast & Mould"]),
        ("Coliform", "Negative", data["Coliform"]),
        ("Ecoli", "Negative", data["Ecoli"]),
        ("Salmonella", "Negative", data["Salmonella"]),
    ]
    for row in microbiological_data:
        pdf.add_table_row(*row, col_widths=(60, 60, 50), row_height=5)

    return pdf

# Streamlit App
st.title("Certificate of Analysis Generator")
st.write("Fill in the fields below to generate a COA PDF:")

# Collect user inputs, including for viscosity
user_inputs = {field: st.text_input(field, placeholder=f"Enter {field}...") for field in fields_to_fill}

if st.button("Generate PDF"):
    pdf = create_pdf(user_inputs)

    # Save PDF to buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.success("PDF generated successfully!")
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="COA_Food_Filled.pdf",
        mime="application/pdf",
    )
