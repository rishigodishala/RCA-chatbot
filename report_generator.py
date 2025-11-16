import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime

class ReportGenerator:
    def __init__(self, metrics, history, problem_context=None, workflow="8D", evidence_images=None):
        self.metrics = metrics
        self.history = history
        self.problem_context = problem_context or {}
        self.workflow = workflow
        self.evidence_images = evidence_images or []

    def generate_text_report(self):
        report = f"{'='*80}\n"
        report += f"ROOT CAUSE ANALYSIS REPORT - {self.workflow} METHODOLOGY\n"
        report += f"{'='*80}\n\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Problem Context Section
        report += f"{'-'*80}\n"
        report += "PROBLEM CONTEXT\n"
        report += f"{'-'*80}\n"
        if self.problem_context:
            for key, value in self.problem_context.items():
                report += f"{key.replace('_', ' ').title()}: {value}\n"
            report += "\n"
        
        # Investigation Metrics
        report += f"{'-'*80}\n"
        report += "INVESTIGATION METRICS\n"
        report += f"{'-'*80}\n"
        for metric, value in self.metrics.items():
            report += f"{metric}: {value:.1f}\n"
        report += "\n"
        
        # Methodology-specific sections
        if self.workflow == "8D":
            report += self._generate_8d_section()
        elif self.workflow == "5-Why":
            report += self._generate_5why_section()
        elif self.workflow == "A3":
            report += self._generate_a3_section()
        
        # Investigation History
        report += f"{'-'*80}\n"
        report += "INVESTIGATION HISTORY\n"
        report += f"{'-'*80}\n"
        for i, (q, a) in enumerate(self.history):
            if q != "System" and not q.startswith(self.workflow):
                report += f"\nQ{i}: {q}\n"
                report += f"A{i}: {a}\n"
        report += "\n"
        
        # Evidence Section
        if self.evidence_images:
            report += f"{'-'*80}\n"
            report += "EVIDENCE IMAGES\n"
            report += f"{'-'*80}\n"
            for img in self.evidence_images:
                report += f"- {img}\n"
            report += "\n"
        
        # Recommendations
        report += f"{'-'*80}\n"
        report += "RECOMMENDATIONS\n"
        report += f"{'-'*80}\n"
        report += self._generate_recommendations()
        
        report += f"\n{'='*80}\n"
        report += "END OF REPORT\n"
        report += f"{'='*80}\n"
        
        return report
    
    def _generate_8d_section(self):
        section = f"{'-'*80}\n"
        section += "8D METHODOLOGY ANALYSIS\n"
        section += f"{'-'*80}\n"
        section += """
D0: Prepare and Plan - Investigation initiated
D1: Establish Team - Cross-functional investigation team
D2: Problem Description - Documented in problem context
D3: Interim Containment - Immediate actions to be determined
D4: Root Cause Analysis - Investigation in progress
D5: Corrective Actions - To be developed based on findings
D6: Implementation - Pending corrective action selection
D7: Prevention - Standardization and lessons learned
D8: Team Recognition - Upon successful completion

"""
        return section
    
    def _generate_5why_section(self):
        section = f"{'-'*80}\n"
        section += "5-WHY ANALYSIS\n"
        section += f"{'-'*80}\n"
        section += """
The 5-Why technique has been applied to identify root causes through
iterative questioning. Each "why" builds upon the previous answer to
dig deeper into the underlying systemic issues.

Key Findings:
- Investigation focused on cause-and-effect relationships
- Multiple potential root causes identified
- Verification of root causes recommended before implementing solutions

"""
        return section
    
    def _generate_a3_section(self):
        section = f"{'-'*80}\n"
        section += "A3 PROBLEM SOLVING FORMAT\n"
        section += f"{'-'*80}\n"
        section += """
Background: Problem context documented
Current Condition: Investigation findings captured
Goal/Target: Problem resolution and prevention
Root Cause Analysis: Systematic investigation conducted
Countermeasures: To be developed based on findings
Implementation Plan: Pending countermeasure selection
Follow-up: Monitoring and verification required

"""
        return section
    
    def _generate_recommendations(self):
        recommendations = """
Based on the investigation conducted:

1. IMMEDIATE ACTIONS:
   - Verify identified root causes with additional data
   - Implement interim containment measures if not already done
   - Document all findings and evidence

2. CORRECTIVE ACTIONS:
   - Develop specific corrective actions targeting root causes
   - Test proposed solutions before full implementation
   - Establish metrics to measure effectiveness

3. PREVENTIVE MEASURES:
   - Update procedures and work instructions
   - Implement mistake-proofing (Poka-Yoke) where applicable
   - Share lessons learned across organization
   - Establish monitoring to prevent recurrence

4. FOLLOW-UP:
   - Schedule regular reviews to verify effectiveness
   - Monitor key metrics for sustained improvement
   - Document lessons learned for future reference

"""
        return recommendations

    def generate_chart(self):
        metrics = list(self.metrics.keys())
        values = list(self.metrics.values())

        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        ax.barh(metrics, values, color=colors[:len(metrics)])
        ax.set_xlabel('Score / Progress (%)')
        ax.set_title(f'RCA Investigation Metrics - {self.workflow} Methodology')
        ax.set_xlim(0, 100)
        
        # Add value labels on bars
        for i, v in enumerate(values):
            ax.text(v + 2, i, f'{v:.1f}', va='center')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_data = buf.read()
        plt.close(fig)
        return img_data

    def generate_pdf_report(self, filename="rca_report.pdf"):
        text_report = self.generate_text_report()
        chart_img = self.generate_chart()

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, height - 80, f"Root Cause Analysis Report")
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, f"{self.workflow} Methodology")
        c.drawString(100, height - 115, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Problem Context
        y = height - 160
        if self.problem_context:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y, "Problem Context:")
            y -= 25
            c.setFont("Helvetica", 11)
            for key, value in self.problem_context.items():
                text = f"{key.replace('_', ' ').title()}: {value}"
                # Wrap long text
                if len(text) > 70:
                    text = text[:70] + "..."
                c.drawString(120, y, text)
                y -= 18

        # Metrics
        y -= 25
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, "Investigation Metrics:")
        y -= 25
        c.setFont("Helvetica", 11)
        for metric, value in self.metrics.items():
            c.drawString(120, y, f"{metric}: {value:.1f}")
            y -= 18

        # Embed chart image
        y -= 30
        if y < 250:
            c.showPage()
            y = height - 100
        
        img = ImageReader(io.BytesIO(chart_img))
        c.drawImage(img, 80, y - 220, width=450, height=200, preserveAspectRatio=True)
        y -= 240

        # Summary
        if y < 150:
            c.showPage()
            y = height - 100
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, "Summary:")
        y -= 25
        c.setFont("Helvetica", 10)
        c.drawString(100, y, "Detailed investigation conducted using systematic RCA methodology.")
        y -= 15
        c.drawString(100, y, "Root causes identified through structured questioning and analysis.")
        y -= 15
        c.drawString(100, y, "Recommendations provided for corrective and preventive actions.")
        
        # Evidence
        if self.evidence_images:
            y -= 30
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y, f"Evidence Images: {len(self.evidence_images)} file(s) attached")

        c.save()
        return filename
