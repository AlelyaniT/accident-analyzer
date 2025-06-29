import cv2
import numpy as np
from PIL import Image
from fpdf import FPDF
import os

# Simulated YOLOv8 Detection (replace with real model)
def detect_objects(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    h, w = img.shape[:2]
    
    # Simulate vehicle detection
    cv2.rectangle(img, (int(w*0.3), int(h*0.4)), (int(w*0.6), int(h*0.8)), (0, 0, 255), 2)
    cv2.putText(img, "Vehicle 1", (int(w*0.3), int(h*0.38)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    # Simulate damage zones
    cv2.circle(img, (int(w*0.55), int(h*0.5)), 30, (0,165,255), -1)
    cv2.putText(img, "Severe Damage", (int(w*0.55)-50, int(h*0.5)+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 2)
    
    # Simulate traffic signs
    cv2.putText(img, "STOP SIGN", (int(w*0.1), int(h*0.2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Top-down reconstruction
def generate_reconstruction(image):
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    img.fill(230)  # Light gray background
    
    # Draw roads
    cv2.rectangle(img, (150, 100), (450, 300), (100, 100, 100), -1)
    cv2.line(img, (300, 100), (300, 300), (255, 255, 255), 2)  # Lane divider
    
    # Draw vehicles
    cv2.rectangle(img, (200, 150), (300, 250), (0, 0, 255), -1)  # Vehicle 1
    cv2.rectangle(img, (300, 200), (400, 300), (255, 0, 0), -1)   # Vehicle 2
    
    # Add annotations
    cv2.putText(img, "Vehicle 1 (At Fault)", (200, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.putText(img, "Vehicle 2", (300, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.putText(img, "Stop Sign", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,0), 2)
    
    return Image.fromarray(img)

# Legal analysis (simulated)
def analyze_scene(image, law_version="Saudi Arabia"):
    return {
        "responsibility": "Driver of Vehicle 1 failed to yield at intersection",
        "law_reference": "Saudi Traffic Law Article 42: Right of Way",
        "confidence": 87,
        "damage_analysis": "Vehicle 1: Front-end damage (Severe)\nVehicle 2: Side impact (Moderate)",
        "scene_analysis": "Stop sign visible for Vehicle 1\nNo skid marks detected"
    }

# Bilingual PDF report
def generate_report(data, lang="ar_en"):
    pdf = FPDF()
    pdf.add_page()
    
    # English Section
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Accident Analysis Report", ln=1, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 7, txt=f"Responsibility: {data['responsibility']}")
    pdf.multi_cell(0, 7, txt=f"Legal Basis: {data['law_reference']}")
    pdf.multi_cell(0, 7, txt=f"Confidence: {data['confidence']}%")
    
    # Arabic Section (if bilingual)
    if lang == "ar_en":
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="تقرير تحليل الحادث", ln=1, align="C")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 7, txt="هذا نموذج أولي للنظام", align="R")
    
    pdf_path = "accident_report.pdf"
    pdf.output(pdf_path)
    return pdf_path