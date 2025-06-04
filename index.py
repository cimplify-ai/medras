from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
import streamlit as st


def all_pages(page_number):
    print("second")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 10)

    # Header
    can.drawImage("./22.png",0, 720, width=615, height=72)
    can.drawCentredString(300, 750, "Report")
    can.drawCentredString(500, 768, "No.20/6 Sengunthar Street,")
    can.drawCentredString(500, 754, "Shenoy Nagar (East)")
    can.drawCentredString(500, 739, "Chennai 600030, Tamil Nadu")
    # can.drawCentredString(300, 770, header_text)
    
    # Footer
    
    can.drawImage("./23.png",0, 0, width=620, height=72)
    can.drawCentredString(600, 25, page_number)

    can.save()
    packet.seek(0)
    return PdfReader(packet)

def first_page(data, page_height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman", 12)
    # Header
    # can.drawImage("./empty.png",0, 780, width=615, height=72)
    can.drawImage("./22.png",0, 720, width=615, height=72)
    can.drawCentredString(300, 750, "Report")
    can.drawCentredString(500, 768, "No.20/6 Sengunthar Street,")
    can.drawCentredString(500, 754, "Shenoy Nagar (East)")
    can.drawCentredString(500, 739, "Chennai 600030, Tamil Nadu")
    can.drawImage("./empty.png",30, 640, width=555, height=80)

    # print(page_height)
    if int(page_height) < 800:
        can.drawImage("./empty.png",30, 590, width=555, height=70)

    width, height = letter
    # Starting position
    x_start = 13 * mm
    y_start = height - 30 * mm
    box_width = width - 20 * mm
    box_height = 20 * mm

    # Draw outer box
    can.rect(x_start, y_start - box_height, box_width, box_height)

    # Set font
    can.setFont("Times-Roman", 12)

    # First row positions
    can.drawString(x_start + 5, y_start - 22, "Patient Name:")
    can.drawString(x_start + 30*mm, y_start - 22, data['Name'])


    can.drawString(x_start + 140*mm, y_start - 22, "Sex:")
    can.drawString(x_start + 150*mm, y_start - 22, data["sex"])  


    can.drawString(x_start + 170*mm, y_start - 22, "Age:")
    can.drawString(x_start + 180*mm, y_start - 22, str(data["age"]))  

    # Second row
    can.drawString(x_start + 5, y_start - 44, "Investigation:")
    can.drawString(x_start + 45*mm, y_start - 44, data["investigation"])  
    
    can.drawString(x_start + 140*mm, y_start - 44, "Medras ID:")
    can.drawString(x_start + 163*mm, y_start - 44, data["medras_id"])
    

    can.drawImage("./23.png",0, 0, width=620, height=72)
  
    can.drawCentredString(600, 25, "1")

    can.save()
    packet.seek(0)
    return PdfReader(packet)

st.title("Simple Form with Upload and Download")

name = st.text_input("Patient Name")
medras_id = st.text_input("Medras id")
age = st.number_input("Age", min_value=0, step=1)
sex = st.text_input("sex")
Investigation = st.text_area("Investigation")

uploaded_file = st.file_uploader("Upload a file (pdf)")

if st.button("Download Summary"):
    data = {
        "Name": name,
        "medras_id": medras_id,
        "age": age,
        "sex": sex,
        "investigation": Investigation
    }

    writer = PdfWriter()
    if uploaded_file:
        file_content = uploaded_file
        st.write("Uploaded File Content:")
        
        # Load original
        reader = PdfReader(file_content)
        box = reader.pages[0].mediabox
        # st.write([int(box.width), int(box.height)])
        height = int(box.height)
        for i, page in enumerate(reader.pages):
            page.mediabox.upper_right = (letter[0], letter[1])
            overlay =  first_page(data, height) if i == 0 else all_pages(str(i + 1))
            page.merge_page(overlay.pages[0])
            writer.add_page(page)
    # with open("labReport_with_header_footer.pdf", "wb") as f:
    #     writer.write(f)

    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)

    st.download_button(
        label="Download as pdf",
        data=buffer,
        file_name=name + ".pdf",
        mime="application/pdf"
    )

