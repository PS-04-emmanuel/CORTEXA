from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

class PDFService:
    def generate_report_pdf(self, report_data: dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, spaceAfter=20)
        story.append(Paragraph("Business Feasibility Report", title_style))
        story.append(Spacer(1, 12))

        # Feasibility Score
        score = report_data.get('feasibility_score', 0)
        score_color = colors.green if score > 70 else colors.orange
        score_style = ParagraphStyle('Score', parent=styles['Heading2'], textColor=score_color)
        story.append(Paragraph(f"Feasibility Score: {score}/100", score_style))
        story.append(Spacer(1, 20))

        # Summary
        story.append(Paragraph("Summary", styles['Heading3']))
        story.append(Paragraph(report_data.get('summary', ''), styles['Normal']))
        story.append(Spacer(1, 12))

        # Economic Analysis
        story.append(Paragraph("Economic Analysis", styles['Heading3']))
        story.append(Paragraph(report_data.get('economic_analysis', ''), styles['Normal']))
        story.append(Spacer(1, 12))

        # Pros Section
        story.append(Paragraph("Pros", styles['Heading3']))
        pros = report_data.get('pros', [])
        for p in pros:
            story.append(Paragraph(f"• {p}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Cons Section
        story.append(Paragraph("Cons", styles['Heading3']))
        cons = report_data.get('cons', [])
        for c in cons:
            story.append(Paragraph(f"• {c}", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

pdf_service = PDFService()
