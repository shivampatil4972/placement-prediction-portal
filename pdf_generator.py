"""
PDF Report Generation Utility
Creates downloadable placement prediction reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class ReportGenerator:
    """Generate PDF reports for placement predictions"""
    
    @staticmethod
    def generate_placement_report(filename, user_data, profile_data, prediction_data, 
                                  skill_gap_data, suggestions):
        """
        Generate comprehensive placement prediction report
        
        Args:
            filename: Output PDF filename
            user_data: User information
            profile_data: Student profile data
            prediction_data: ML prediction results
            skill_gap_data: Skill gap analysis
            suggestions: Personalized suggestions
        
        Returns:
            Path to generated PDF
        """
        
        # Create PDF document
        pdf = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("Placement Prediction Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Generated On:</b> {report_date}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Student Information
        story.append(Paragraph("Student Information", heading_style))
        
        student_info = [
            ["Name:", user_data.get('full_name', 'N/A')],
            ["Email:", user_data.get('email', 'N/A')],
            ["Enrollment:", profile_data.get('enrollment_number', 'N/A')],
            ["Branch:", profile_data.get('branch', 'N/A')],
            ["CGPA:", str(profile_data.get('cgpa', 'N/A'))],
            ["Semester:", str(profile_data.get('semester', 'N/A'))]
        ]
        
        student_table = Table(student_info, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        
        story.append(student_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Academic & Extracurricular Profile
        story.append(Paragraph("Academic & Extracurricular Profile", heading_style))
        
        profile_info = [
            ["Internships Completed:", str(profile_data.get('internship_count', 0))],
            ["Projects Completed:", str(profile_data.get('project_count', 0))],
            ["Certifications:", str(profile_data.get('certification_count', 0))],
            ["Skills Count:", str(len(profile_data.get('skills', '').split(',')) if profile_data.get('skills') else 0)]
        ]
        
        profile_table = Table(profile_info, colWidths=[2.5*inch, 3.5*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(profile_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Prediction Results (Highlighted)
        story.append(Paragraph("Prediction Results", heading_style))
        
        # Determine color based on probability
        prob = prediction_data.get('placement_probability', 0)
        if prob >= 70:
            prob_color = colors.green
            prob_bg_color = colors.HexColor('#c8e6c9')  # light green
        elif prob >= 40:
            prob_color = colors.orange
            prob_bg_color = colors.HexColor('#ffe0b2')  # light orange
        else:
            prob_color = colors.red
            prob_bg_color = colors.HexColor('#ffcdd2')  # light red
        
        prediction_info = [
            ["Placement Probability:", f"{prob}%"],
            ["Risk Level:", prediction_data.get('risk_level', 'N/A')],
            ["Expected Salary:", f"₹ {prediction_data.get('predicted_salary', 'N/A')} LPA"]
        ]
        
        prediction_table = Table(prediction_info, colWidths=[2.5*inch, 3.5*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('BACKGROUND', (1, 0), (1, 0), prob_bg_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 2, colors.grey)
        ]))
        
        story.append(prediction_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Skill Gap Analysis
        if skill_gap_data:
            story.append(Paragraph("Skill Gap Analysis", heading_style))
            
            missing_skills_text = skill_gap_data.get('missing_skills', 'None identified')
            story.append(Paragraph(f"<b>Missing Skills:</b> {missing_skills_text}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            priority = skill_gap_data.get('priority', 'Medium')
            priority_color = 'red' if priority == 'High' else 'orange' if priority == 'Medium' else 'green'
            story.append(Paragraph(f"<b>Priority:</b> <font color='{priority_color}'>{priority}</font>", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Personalized Suggestions
        story.append(Paragraph("Personalized Recommendations", heading_style))
        
        for i, suggestion in enumerate(suggestions, 1):
            story.append(Paragraph(f"{i}. {suggestion}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("This report is generated by the Student Placement Prediction & Strategy Portal", footer_style))
        story.append(Paragraph("For educational purposes only. Predictions are based on historical data and ML models.", footer_style))
        
        # Build PDF
        pdf.build(story)
        
        return filename


# Convenience instance
report_generator = ReportGenerator()
