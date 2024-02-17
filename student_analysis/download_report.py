import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import io


def create_pdf(student_name, image_folder):
    output_file = f"{student_name}_performance_report.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<big><b>Students Performance Report</b></big>", styles["Title"])
    student_name_paragraph = Paragraph(f"<b>Student Name:</b> {student_name}", styles["BodyText"])

    # Image insertion
    images = []
    for image_name in sorted(os.listdir(image_folder)):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_folder, image_name)
            img = PILImage.open(img_path)
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width
            max_width = 500  # Adjust according to your preference
            img_width = min(img_width, max_width)
            img_height = int(img_width * aspect_ratio)
            img_obj = Image(img_path, width=img_width, height=img_height)
            images.append(img_obj)

    # Building PDF
    story = [title, Spacer(1, 20), student_name_paragraph, Spacer(1, 20)]
    for img in images:
        story.append(img)
        story.append(Spacer(1, 20))

    doc.build(story)
    return output_file



