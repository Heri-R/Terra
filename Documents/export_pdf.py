from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO

def generate_payment_pdf(patient_info, payment_info):
  # Generate filename
  timestamp = datetime.now().strftime("%Y-%m-%d")
  filename = f"payment-receipt-{patient_info['first_name']}_{patient_info['last_name']}-{timestamp}.pdf"

  buffer = BytesIO()
  
  # Create PDF document
  doc = SimpleDocTemplate(
    buffer,
    pagesize=letter,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
  )
  
  # Prepare styles
  styles = getSampleStyleSheet()
  
  # Custom styles
  styles['Title'].fontSize = 16
  styles['Title'].leading = 15
  styles['Title'].spaceAfter = 10
  
  styles.add(ParagraphStyle(
    name='Header',
    fontSize=12,
    leading=15,
    spaceAfter=10,
    textColor=colors.darkblue
  ))
  
  styles.add(ParagraphStyle(
    name='NormalBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold'
  ))
  
  # Build document content
  elements = []
  
  # Clinic header
  elements.append(Paragraph("Terra Natural Herbs", styles['Title']))
  elements.append(Paragraph("P.O.BOX 222, Arusha, Arusha", styles['Normal']))
  elements.append(Paragraph("Tel: 255 793 075 781 | bambukahombe@gmail.com", styles['Normal']))
  elements.append(Spacer(1, 30))
  
  # Receipt title
  elements.append(Paragraph("PAYMENT RECEIPT", styles['Title']))
  elements.append(Spacer(1, 20))
  
  # Transaction info
  transaction_data = [
    ["Transaction ID:", payment_info['payment_id']],
    ["Date:", payment_info['date_paid'] if isinstance(payment_info['date_paid'], str) else payment_info['date_paid'].strftime("%B %d, %Y %I:%M %p")],
    ["Status:","Paid" if payment_info['is_completed'] else "Not Paid"],
  ]
  
  transaction_table = Table(transaction_data, colWidths=[120, 300])
  transaction_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
  ]))
  
  elements.append(transaction_table)
  elements.append(Spacer(1, 30))
  
  # Patient information
  elements.append(Paragraph("PATIENT INFORMATION", styles['Header']))
  
  patient_data = [
    ["Patient Name:", f"{patient_info['first_name']} {patient_info['last_name']}"],
    ["Patient ID:", patient_info['patient_id']],
    ["Age:", str(patient_info['age'])],
    ["Gender:", patient_info['gender'].capitalize()],
    ["Phone:", patient_info['phone_number_1']]
  ]
  
  patient_table = Table(patient_data, colWidths=[120, 300])
  patient_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
  ]))
  
  elements.append(patient_table)
  elements.append(Spacer(1, 30))
  
  # Payment amount
  elements.append(Paragraph("PAYMENT DETAILS", styles['Header']))
  
  amount_data = [
    ["Amount Paid:", f"Tsh {payment_info['amount']:,}"]
  ]
  
  amount_table = Table(amount_data, colWidths=[120, 300])
  amount_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
  ]))
  
  elements.append(amount_table)
  elements.append(Spacer(1, 40))
  
  # Footer
  elements.append(Paragraph("Thank you for your payment!", styles['Normal']))
  elements.append(Spacer(1, 10))
  elements.append(Paragraph("Please keep this receipt for your records.", styles['Normal']))
  elements.append(Paragraph("For any questions, please contact our billing department.", styles['Normal']))
  
  # Generate PDF
  doc.build(elements)

  buffer.seek(0)
  return send_file(
    buffer,
    as_attachment=False,
    mimetype='application/pdf',
    download_name=filename
  )
