def create_html_report(input_data, predictions):
    """Create an HTML report with prediction results"""
    html_content = f"""
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>Weather Prediction Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f9f9f9; color: #222; }}
            .header {{ text-align: center; margin-bottom: 16px; }}
            .section {{ margin: 24px auto; max-width: 900px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }}
            .section h2 {{ color: #1976D2; border-bottom: 2px solid #1976D2; padding-bottom: 5px; margin-top: 0; }}
            .prediction-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0; }}
            .prediction-item {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.08); }}
            .prediction-item h3 {{ margin: 0 0 10px 0; font-size: 1.1em; }}
            .prediction-item .value {{ font-size: 1.8em; font-weight: bold; margin: 10px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌤 Weather Prediction Report</h1>
            <p style='margin:0;'>Designed and Developed by Varshini J</p>
        </div>
        <div class="section">
            <h2>📊 Prediction Results</h2>
            <div class="prediction-grid">
                <div class="prediction-item">
                    <h3>🌧 Rainfall Amount</h3>
                    <div class="value">{predictions['rainfall']:.2f} mm</div>
                </div>
                <div class="prediction-item">
                    <h3>🌡 Temperature</h3>
                    <div class="value">{predictions['temperature']:.2f}°C</div>
                </div>
                <div class="prediction-item">
                    <h3>☔ Rain Occurrence</h3>
                    <div class="value">{predictions['rain_class']}</div>
                </div>
                <div class="prediction-item">
                    <h3>🔥 Temperature Category</h3>
                    <div class="value">{predictions['temp_class']}</div>
                </div>
            </div>
        </div>
        <div class="section">
            <h2>📝 Input Parameters</h2>
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
    """
    parameter_descriptions = {
        "latitude": "Degrees North",
        "longitude": "Degrees East", 
        "humidity": "Percentage (%)",
        "wind_kph": "Kilometers per Hour",
        "cloud": "Percentage (%)",
        "pressure_mb": "Millibars",
        "uv_index": "UV Index Scale",
        "feels_like_celsius": "Degrees Celsius",
        "air_quality_Carbon_Monoxide": "μg/m³",
        "air_quality_Ozone": "μg/m³",
        "air_quality_Nitrogen_dioxide": "μg/m³",
        "air_quality_Sulphur_dioxide": "μg/m³",
        "air_quality_PM2.5": "μg/m³",
        "air_quality_PM10": "μg/m³"
    }
    for param, value in input_data.items():
        description = parameter_descriptions.get(param, "")
        html_content += f"""
                    <tr>
                        <td>{param.replace('_', ' ').title()}</td>
                        <td>{value:.4f}</td>
                        <td>{description}</td>
                    </tr>"""
    html_content += f"""
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import io
import base64
import os
import shutil
import tempfile
import subprocess
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


def detect_pdf_engine():
    """Return a short string describing which PDF engine is available on the system."""
    # Prefer WeasyPrint
    try:
        import weasyprint  # type: ignore
        return 'weasyprint'
    except Exception:
        pass

    # Try pdfkit+wkhtmltopdf
    try:
        import pdfkit  # type: ignore
        wk = shutil.which('wkhtmltopdf')
        if wk:
            return f'pdfkit + wkhtmltopdf ({wk})'
        # check common install locations on Windows
        candidates = [
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                return f'pdfkit + wkhtmltopdf ({c})'
        return 'pdfkit (no wkhtmltopdf found)'
    except Exception:
        pass

    # Direct wkhtmltopdf
    wk = shutil.which('wkhtmltopdf')
    if wk:
        return f'wkhtmltopdf ({wk})'

    return 'none'


def create_pdf_report(input_data, predictions):
    """Create a PDF report that matches the HTML design exactly"""
    # Try WeasyPrint first (should work now that it's installed)
    try:
        from weasyprint import HTML, CSS  # type: ignore
        html = create_html_report(input_data, predictions)
        
        # Add some CSS tweaks for better PDF rendering
        css_fixes = CSS(string='''
            @page { 
                size: A4; 
                margin: 0.5in; 
            }
            body { 
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            .prediction-item {
                break-inside: avoid;
                page-break-inside: avoid;
            }
        ''')
        
        buffer = io.BytesIO()
        HTML(string=html).write_pdf(buffer, stylesheets=[css_fixes])
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"WeasyPrint failed: {e}")
    
    # Fallback: Create a much better ReportLab version that mimics the HTML closely
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    
    # Better styles that match the HTML design
    title_style = ParagraphStyle(
        'TitleStyle', 
        parent=styles['Title'], 
        fontSize=24, 
        spaceAfter=10, 
        textColor=colors.HexColor('#333'), 
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle', 
        parent=styles['Normal'], 
        fontSize=12, 
        spaceAfter=20, 
        textColor=colors.HexColor('#666'), 
        alignment=1
    )
    
    section_style = ParagraphStyle(
        'SectionStyle', 
        parent=styles['Heading2'], 
        fontSize=16, 
        spaceAfter=10, 
        textColor=colors.HexColor('#1976D2'), 
        leftIndent=0,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Header section
    story.append(Paragraph("Weather Prediction Report", title_style))
    story.append(Paragraph("Designed and Developed by Varshini J", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Prediction Results section
    story.append(Paragraph("Prediction Results", section_style))
    story.append(Spacer(1, 10))
    
    # Create a better-looking prediction grid (replace emojis with text)
    pred_data = [
        ["Rainfall Amount", f"{predictions['rainfall']:.2f} mm"],
        ["Temperature", f"{predictions['temperature']:.2f}°C"],
        ["Rain Occurrence", predictions['rain_class']],
        ["Temperature Category", predictions['temp_class']]
    ]
    
    pred_table = Table(pred_data, colWidths=[3*inch, 3*inch])
    pred_table.setStyle(TableStyle([
        # Background colors to mimic the gradient
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#764ba2')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#667eea'), colors.HexColor('#764ba2')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    
    story.append(pred_table)
    story.append(Spacer(1, 30))
    
    # Input Parameters section
    story.append(Paragraph("Input Parameters", section_style))
    story.append(Spacer(1, 10))
    
    parameter_descriptions = {
        "latitude": "Degrees North",
        "longitude": "Degrees East",
        "humidity": "Percentage (%)",
        "wind_kph": "Kilometers per Hour",
        "cloud": "Percentage (%)",
        "pressure_mb": "Millibars",
        "uv_index": "UV Index Scale",
        "feels_like_celsius": "Degrees Celsius",
        "air_quality_Carbon_Monoxide": "μg/m³",
        "air_quality_Ozone": "μg/m³",
        "air_quality_Nitrogen_dioxide": "μg/m³",
        "air_quality_Sulphur_dioxide": "μg/m³",
        "air_quality_PM2.5": "μg/m³",
        "air_quality_PM10": "μg/m³"
    }
    
    input_data_list = [['Parameter', 'Value', 'Description']]
    for param, value in input_data.items():
        description = parameter_descriptions.get(param, "")
        formatted_param = param.replace('_', ' ').title()
        input_data_list.append([formatted_param, f"{value:.4f}", description])
    
    input_table = Table(input_data_list, colWidths=[2.2*inch, 1.3*inch, 2.5*inch])
    input_table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows styling  
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    
    story.append(input_table)
    story.append(Spacer(1, 30))
    
    # Environmental Awareness section (PDF only)
    story.append(Paragraph("Environmental Awareness & Air Quality Impact", section_style))
    story.append(Spacer(1, 10))
    
    env_style = ParagraphStyle(
        'EnvStyle', 
        parent=styles['Normal'], 
        fontSize=10, 
        spaceAfter=8, 
        textColor=colors.HexColor('#444'), 
        leftIndent=10,
        rightIndent=10,
        alignment=4  # Justify alignment
    )
    
    story.append(Paragraph("<b>Protecting Our Mother Earth:</b> Our planet's atmosphere is under constant threat from various pollutants that not only harm human health but also disrupt ecological balance. The air quality parameters measured in this weather prediction report directly correlate with environmental degradation and public health crises. Understanding these pollutants and their sources empowers us to make informed decisions that can help preserve our planet for future generations.", env_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Detailed Air Pollutants & Their Environmental Impact:</b>", env_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("• <b>Carbon Monoxide (CO):</b> A colorless, odorless gas primarily produced by vehicle emissions and industrial processes. It reduces the blood's ability to carry oxygen, leading to headaches, dizziness, and fatigue. In the environment, CO contributes to ground-level ozone formation and climate change.", env_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("• <b>Nitrogen Dioxide (NO<sub>2</sub>):</b> A reddish-brown gas from vehicle exhausts and power plants. It irritates airways, triggers asthma attacks, and reduces lung function. Environmentally, NO<sub>2</sub> contributes to acid rain formation, soil acidification, and eutrophication of water bodies, damaging forests and aquatic ecosystems.", env_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("• <b>Sulphur Dioxide (SO<sub>2</sub>):</b> Released mainly from fossil fuel combustion in power plants and industrial facilities. It causes respiratory problems, particularly in children and elderly. SO<sub>2</sub> is a major contributor to acid rain, which corrodes buildings, damages crops, and acidifies lakes and streams, killing fish and other aquatic life.", env_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("• <b>Particulate Matter (PM2.5 & PM10):</b> Microscopic particles that penetrate deep into lungs and bloodstream, causing heart disease, stroke, and lung cancer. These particles reduce visibility (haze), damage vegetation, and alter weather patterns. PM2.5 can travel thousands of kilometers, making it a global environmental concern.", env_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("• <b>Ground-level Ozone (O<sub>3</sub>):</b> Formed when other pollutants react in sunlight. While beneficial in the upper atmosphere, ground-level ozone irritates eyes and respiratory system, and damages plant tissues, reducing crop yields and forest productivity. It's a major component of urban smog.", env_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Comprehensive Environmental Protection Strategies:</b>", env_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Individual Actions:</b>", env_style))
    story.append(Paragraph("• Choose public transportation, cycling, or walking over private vehicles", env_style))
    story.append(Paragraph("• Invest in energy-efficient appliances and renewable energy sources", env_style))
    story.append(Paragraph("• Practice waste reduction, reuse, and recycling", env_style))
    story.append(Paragraph("• Support organic farming and sustainable products", env_style))
    story.append(Paragraph("• Monitor and report air quality in your community", env_style))
    story.append(Paragraph("• Plant native trees and maintain green spaces", env_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Community Initiatives:</b>", env_style))
    story.append(Paragraph("• Advocate for stricter emission standards and clean energy policies", env_style))
    story.append(Paragraph("• Support urban planning that promotes green infrastructure", env_style))
    story.append(Paragraph("• Participate in community tree-planting and cleanup programs", env_style))
    story.append(Paragraph("• Encourage businesses to adopt sustainable practices", env_style))
    story.append(Paragraph("• Promote awareness about environmental health connections", env_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Global Impact:</b> The air quality data you analyze contributes to our understanding of climate change, public health patterns, and environmental justice issues. By monitoring these parameters, we can identify pollution hotspots, track improvement efforts, and develop targeted interventions to protect vulnerable communities and ecosystems.", env_style))
    story.append(Spacer(1, 20))
    story.append(Spacer(1, 20))
    
    # Footer
    footer_style = ParagraphStyle(
        'FooterStyle', 
        parent=styles['Normal'], 
        fontSize=10, 
        textColor=colors.HexColor('#666'), 
        alignment=1
    )
    story.append(Paragraph("Weather Prediction Tool | Designed and Developed by Varshini J", footer_style))
    story.append(Spacer(1, 30))
    
    # Add character image at the end - spread across full page width
    try:
        page_width = A4[0] - 2*inch  # Account for margins - use A4 from function scope
        
        character_img = Image("character.png", width=page_width, height=3*inch)
        character_img.hAlign = 'CENTER'
        
        # Add the image with proper spacing
        story.append(character_img)
        story.append(Spacer(1, 15))
        
    except Exception as e:
        print(f"Character image error: {e}")
        pass  # If image fails to load, continue without it
    
    # Add a thoughtful closing message after the character image
    closing_style = ParagraphStyle(
        'ClosingStyle', 
        parent=styles['Normal'], 
        fontSize=11, 
        spaceAfter=8, 
        textColor=colors.HexColor('#2c5530'), 
        leftIndent=15,
        rightIndent=15,
        alignment=1,  # Center alignment
        fontName='Helvetica-Oblique'
    )
    
    story.append(Paragraph(" <b>Thank you for using our Weather Prediction Tool!</b> ", closing_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("May this report empower you to make informed decisions for a healthier tomorrow. Together, let's breathe cleaner air, protect our precious environment, and create a sustainable future for generations to come.", closing_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Stay safe, stay healthy, and stay environmentally conscious!</b>", closing_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Load models
et_reg_rain = joblib.load("et_reg_rain.pkl")
et_reg_temp = joblib.load("et_reg_temp.pkl")
et_cls_rain = joblib.load("et_cls_rain.pkl")
et_cls_temp = joblib.load("et_cls_temp.pkl")

required_features = [
    "latitude", "longitude", "humidity", "wind_kph", "cloud", "pressure_mb", "uv_index", "feels_like_celsius",
    "air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_Nitrogen_dioxide",
    "air_quality_Sulphur_dioxide", "air_quality_PM2.5", "air_quality_PM10"
]

rain_occurred_map = {0: "No Rain", 1: "Rain"}
temp_class_map = {0: "Cold", 1: "Moderate", 2: "Hot"}

st.set_page_config(page_title="🌤 Weather Predictor", layout="wide")

st.markdown("""
<div style='text-align: center;'>
    <h1>🌤 ForecastIQ : Weather Prediction Tool</h1>
    <div style='font-size: 1.2rem;'>
        Enter the weather feature values to get predictions:
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("input_form"):
    st.subheader("📊 Input Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latitude = st.number_input("Latitude", value=0.0, format="%.4f", key="latitude")
        longitude = st.number_input("Longitude", value=0.0, format="%.4f", key="longitude")
        humidity = st.number_input("Humidity", value=0.0, format="%.4f", key="humidity")
        wind_kph = st.number_input("Wind KPH", value=0.0, format="%.4f", key="wind_kph")
        cloud = st.number_input("Cloud", value=0.0, format="%.4f", key="cloud")
        
    with col2:
        pressure_mb = st.number_input("Pressure MB", value=0.0, format="%.4f", key="pressure_mb")
        uv_index = st.number_input("UV Index", value=0.0, format="%.4f", key="uv_index")
        feels_like_celsius = st.number_input("Feels Like Celsius", value=0.0, format="%.4f", key="feels_like_celsius")
        air_quality_Carbon_Monoxide = st.number_input("Air Quality Carbon Monoxide", value=0.0, format="%.4f", key="air_quality_Carbon_Monoxide")
        air_quality_Ozone = st.number_input("Air Quality Ozone", value=0.0, format="%.4f", key="air_quality_Ozone")
        
    with col3:
        air_quality_Nitrogen_dioxide = st.number_input("Air Quality Nitrogen Dioxide", value=0.0, format="%.4f", key="air_quality_Nitrogen_dioxide")
        air_quality_Sulphur_dioxide = st.number_input("Air Quality Sulphur Dioxide", value=0.0, format="%.4f", key="air_quality_Sulphur_dioxide")
        air_quality_PM25 = st.number_input("Air Quality PM2.5", value=0.0, format="%.4f", key="air_quality_PM25")
        air_quality_PM10 = st.number_input("Air Quality PM10", value=0.0, format="%.4f", key="air_quality_PM10")
    
    # Submit button
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        submitted = st.form_submit_button("🔮 Predict", type="primary")

if submitted:
    # Collect inputs
    inputs = {
        "latitude": latitude,
        "longitude": longitude, 
        "humidity": humidity,
        "wind_kph": wind_kph,
        "cloud": cloud,
        "pressure_mb": pressure_mb,
        "uv_index": uv_index,
        "feels_like_celsius": feels_like_celsius,
        "air_quality_Carbon_Monoxide": air_quality_Carbon_Monoxide,
        "air_quality_Ozone": air_quality_Ozone,
        "air_quality_Nitrogen_dioxide": air_quality_Nitrogen_dioxide,
        "air_quality_Sulphur_dioxide": air_quality_Sulphur_dioxide,
        "air_quality_PM2.5": air_quality_PM25,
        "air_quality_PM10": air_quality_PM10
    }
    
    # Check which fields are missing (still have default value 0.0)
    missing_fields = [field for field, value in inputs.items() if value == 0.0]
    
    if len(missing_fields) == len(required_features):
        # No input provided at all
        st.info("💡 Please enter values for the weather features to get predictions.")
    elif len(missing_fields) > 0:
        # Some fields are missing - show specific missing fields and prevent prediction
        st.warning("⚠️ Please fill in all required fields before making predictions!")
        st.error("🔴 Missing values for the following fields:")
        
        # Display missing fields in a nice format
        missing_text = ""
        for i, field in enumerate(missing_fields):
            if i % 3 == 0 and i > 0:  # New line every 3 fields
                missing_text += "\n"
            missing_text += f"• **{field.replace('_', ' ').title()}**   "
        
        st.markdown(missing_text)
        st.info(f"📊 You have filled {len(required_features) - len(missing_fields)} out of {len(required_features)} required fields.")
        
        # Stop execution here - no predictions will be made
        st.stop()
    else:
        # All fields have been provided - proceed with prediction
        input_df = pd.DataFrame([inputs])
        # Convert to numpy array to avoid sklearn feature name warnings
        input_array = input_df.values
        pred_log_rain = et_reg_rain.predict(input_array)
        pred_rain_mm = np.expm1(pred_log_rain)[0]
        pred_temp = et_reg_temp.predict(input_array)[0]
        pred_cls_rain = et_cls_rain.predict(input_array)[0]
        pred_temp_cls = et_cls_temp.predict(input_array)[0]

        pred_cls_rain_label = rain_occurred_map.get(pred_cls_rain, "Unknown")
        pred_temp_cls_label = temp_class_map.get(pred_temp_cls, "Unknown")

        st.success("✅ Prediction Completed")
        
        # Display predictions in metrics format
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🌧 Rainfall Amount",
                value=f"{pred_rain_mm:.2f} mm",
                help="Predicted rainfall amount in millimeters"
            )
        
        with col2:
            st.metric(
                label="🌡 Temperature",
                value=f"{pred_temp:.2f}°C",
                help="Predicted temperature in Celsius"
            )
        
        with col3:
            st.metric(
                label="☔ Rain Occurrence",
                value=pred_cls_rain_label,
                help="Likelihood of rain occurrence"
            )
        
        with col4:
            st.metric(
                label="🔥 Temperature Category",
                value=pred_temp_cls_label,
                help="Temperature classification category"
            )

        # Prepare data for HTML report
        predictions = {
            'rainfall': pred_rain_mm,
            'temperature': pred_temp,
            'rain_class': pred_cls_rain_label,
            'temp_class': pred_temp_cls_label
        }

        # Store data in session state
        st.session_state.inputs = inputs
        st.session_state.predictions = predictions
        
        # Show the full HTML report in the Streamlit page
        html_report = create_html_report(inputs, predictions)
        st.subheader("📋 Full Weather Prediction Report")
        st.components.v1.html(html_report, height=900, scrolling=True)
        
        # Print button for PDF
        try:
            pdf_buffer = create_pdf_report(inputs, predictions)
            
            # Download PDF button - downloads the exact same report as PDF
            st.download_button(
                label="🖨 Download PDF Report", 
                data=pdf_buffer.getvalue(), 
                file_name="weather_prediction_report.pdf", 
                mime="application/pdf",
                help="Download the full weather prediction report as PDF"
            )
        except Exception as e:
            # Provide a clearer error and install instructions for the PDF converters
            st.error("PDF generation failed. To produce a PDF that preserves the HTML template, install either WeasyPrint or wkhtmltopdf + pdfkit on your machine.")
            st.markdown("**Quick steps (PowerShell):**")
            st.code("pip install pdfkit\n# Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html and add it to your PATH\n# Or, if you use Chocolatey: choco install wkhtmltopdf -y\n# Alternatively try: pip install weasyprint (WeasyPrint has system deps on Windows).", language="powershell")

            st.markdown(f"**Error details:** {e}")
            # Fallback: allow user to download the HTML report (so they can convert/print locally)
            try:
                html_bytes = html_report.encode('utf-8')
                st.download_button("⬇️ Download HTML (fallback)", data=html_bytes, file_name="weather_report.html", mime="text/html")
            except Exception:
                pass

# Single app-level footer (appears once at the bottom of the page)
st.markdown("""
<div style='width:100%; text-align:center; margin-top:30px; padding-top:12px; border-top:1px solid #e6e6e6; color:#444;'>
    <div style='font-size:0.95rem; margin-bottom:6px;'>🌍 Weather Prediction Tool — Designed and Developed by Varshini J</div>
    <div style='margin-bottom:8px;'>
        <a href='https://github.com/varshinijayaprabhu' target='_blank' style='margin-right:12px; color:#0b69ff; text-decoration:none;'>
            <!-- GitHub (blue-themed) -->
            <svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='currentColor' style='vertical-align:middle;'><path d='M12 2C6.477 2 2 6.484 2 12.012c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.483 0-.237-.009-.868-.013-1.703-2.782.605-3.369-1.342-3.369-1.342-.454-1.155-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.004.07 1.532 1.032 1.532 1.032.892 1.529 2.341 1.088 2.91.833.091-.646.35-1.088.636-1.34-2.221-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.254-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.025A9.564 9.564 0 0 1 12 6.844c.85.004 1.705.115 2.504.338 1.909-1.295 2.748-1.025 2.748-1.025.546 1.378.202 2.396.1 2.65.64.7 1.028 1.595 1.028 2.688 0 3.847-2.337 4.695-4.566 4.944.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.749 0 .268.18.579.688.481C19.138 20.175 22 16.427 22 12.012 22 6.484 17.523 2 12 2z'/></svg>
        </a>
        <a href='https://www.linkedin.com/in/varshinij2004' target='_blank' style='color:#0b69ff; text-decoration:none;'>
            <!-- LinkedIn (blue themed) -->
            <svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='currentColor' style='vertical-align:middle;'><path d='M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.761 0 5-2.239 5-5v-14c0-2.761-2.239-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 11.268h-3v-5.604c0-1.337-.026-3.063-1.868-3.063-1.868 0-2.156 1.459-2.156 2.967v5.7h-3v-10h2.881v1.367h.041c.401-.761 1.379-1.563 2.838-1.563 3.036 0 3.6 2.001 3.6 4.601v5.595z'/></svg>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)