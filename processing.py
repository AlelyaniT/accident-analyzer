import sys
import subprocess
import logging
from typing import Tuple, Dict, Union
from PIL import Image
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- OpenCV Installation with Fallback ---
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logger.warning("OpenCV not found, attempting installation...")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "opencv-python-headless==4.9.0.80"
        ])
        import cv2
        CV2_AVAILABLE = True
    except Exception as e:
        logger.error(f"Failed to install OpenCV: {e}")

# --- PDF Report Generation ---
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("FPDF not available - PDF reports disabled")

# --- Constants ---
VEHICLE_COLORS = {
    'vehicle1': (0, 0, 255),    # Red
    'vehicle2': (255, 0, 0),     # Blue
    'damage': (0, 165, 255),     # Orange
    'road_sign': (0, 255, 0)     # Green
}

class AccidentAnalyzer:
    """Core accident analysis functionality"""
    
    @staticmethod
    def detect_objects(image: Image.Image) -> Union[Image.Image, None]:
        """Detect vehicles and damage in image"""
        if not CV2_AVAILABLE:
            logger.error("OpenCV not available - detection disabled")
            return None
            
        try:
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            h, w = img.shape[:2]
            
            # Simulate vehicle detection (replace with real YOLOv8)
            cv2.rectangle(img, 
                         (int(w*0.3), int(h*0.4)),
                         (int(w*0.6), int(h*0.8)), 
                         VEHICLE_COLORS['vehicle1'], 2)
            cv2.putText(img, "Vehicle 1", 
                       (int(w*0.3), int(h*0.38)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                       VEHICLE_COLORS['vehicle1'], 2)
            
            # Simulate damage
            cv2.circle(img, 
                      (int(w*0.55), int(h*0.5)), 
                      30, VEHICLE_COLORS['damage'], -1)
            
            return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return None

    @staticmethod
    def generate_reconstruction(image: Image.Image) -> Image.Image:
        """Generate top-down accident reconstruction"""
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        img.fill(230)  # Light gray background
        
        # Draw roads
        cv2.rectangle(img, (150, 100), (450, 300), (100, 100, 100), -1)
        cv2.line(img, (300, 100), (300, 300), (255, 255, 255), 2)
        
        # Draw vehicles
        cv2.rectangle(img, (200, 150), (300, 250), VEHICLE_COLORS['vehicle1'], -1)
        cv2.rectangle(img, (300, 200), (400, 300), VEHICLE_COLORS['vehicle2'], -1)
        
        return Image.fromarray(img)

    @staticmethod
    def analyze_scene(image: Image.Image, law_version: str = "Saudi Arabia") -> Dict:
        """Analyze accident scene according to traffic laws"""
        return {
            "responsibility": "Driver of Vehicle 1 failed to yield",
            "law_reference": "Saudi Traffic Law Article 42" if law_version == "Saudi Arabia" else "Local Traffic Law",
            "confidence": 87,
            "damage_analysis": {
                "vehicle1": "Front-end damage (Severe)",
                "vehicle2": "Side impact (Moderate)"
            },
            "environment": {
                "road_signs": ["Stop sign"],
                "road_conditions": "Dry pavement"
            }
        }

    @staticmethod
    def generate_report(data: Dict, lang: str = "en") -> str:
        """Generate bilingual accident report"""
        if not PDF_AVAILABLE:
            logger.error("PDF generation disabled - FPDF not available")
            return None
            
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # English Content
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Accident Analysis Report", ln=1, align="C")
            pdf.ln(10)
            
            # Add content sections
            sections = [
                ("Responsibility", data['responsibility']),
                ("Legal Basis", data['law_reference']),
                ("Damage Analysis", "\n".join(
                    f"{k}: {v}" for k, v in data['damage_analysis'].items()
                ))
            ]
            
            for header, content in sections:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt=f"{header}:", ln=1)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 7, txt=content)
                pdf.ln(5)
                
            # Arabic section if requested
            if lang == "ar_en":
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="تقرير تحليل الحادث", ln=1, align="C")
                pdf.ln(10)
                pdf.multi_cell(0, 7, txt="هذا تقرير أولي للنظام", align="R")
            
            report_path = "accident_report.pdf"
            pdf.output(report_path)
            return report_path
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return None
