"""
AI-Based Crop Disease Detection (DEMO / MOCK VERSION)
-------------------------------------------------------
This version runs WITHOUT needing an API key. It simulates AI-based diagnosis
using simple image analysis (color/pattern heuristics) so you can demo the
full app workflow for free.

For the REAL version (using Claude's vision model), see app.py and set your
ANTHROPIC_API_KEY.

Run:
    pip install -r requirements.txt
    streamlit run app_demo.py
"""

import random

import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="AI Crop Disease Detection (Demo)",
    page_icon="🌱",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Mock "AI" logic — simple image heuristics, not a real trained model.
# This exists purely so the workflow can be demoed without an API key.
# ---------------------------------------------------------------------------
DISEASE_LIBRARY = [
    {
        "name": "Leaf Blight",
        "explanation": "Brownish, irregular patches detected near the leaf edges, "
        "consistent with fungal blight symptoms.",
        "treatment": [
            "Remove and destroy affected leaves to stop the spread.",
            "Apply a copper-based fungicide as a safe first step.",
        ],
    },
    {
        "name": "Powdery Mildew",
        "explanation": "Light, powder-like discoloration detected across the leaf "
        "surface, typical of mildew infection.",
        "treatment": [
            "Improve air circulation around the plant.",
            "Apply a diluted neem oil spray weekly.",
        ],
    },
    {
        "name": "Bacterial Spot",
        "explanation": "Small, dark, water-soaked spots detected, often a sign of "
        "bacterial infection rather than fungal.",
        "treatment": [
            "Avoid overhead watering to reduce spread.",
            "Apply a copper-based bactericide as recommended for the crop type.",
        ],
    },
    {
        "name": "No visible disease detected",
        "explanation": "The leaf appears largely uniform in color and texture, "
        "with no strong indicators of common disease patterns.",
        "treatment": [
            "Continue regular monitoring for early signs of stress or discoloration.",
            "Maintain consistent watering and nutrient schedule.",
        ],
    },
]


def mock_analyze(image: Image.Image) -> dict:
    """
    Very simple heuristic "analysis" based on average image color, just to make
    the demo feel responsive to the actual uploaded image (not pure random).
    This is NOT a real disease-detection model.
    """
    img_array = np.array(image.convert("RGB").resize((100, 100)))
    avg_color = img_array.mean(axis=(0, 1))  # [R, G, B]
    brightness = avg_color.mean()
    greenness = avg_color[1] - (avg_color[0] + avg_color[2]) / 2

    # Simple deterministic-ish bucketing so same image tends to give same result
    seed = int(brightness + greenness) % len(DISEASE_LIBRARY)
    disease = DISEASE_LIBRARY[seed]

    if disease["name"] == "No visible disease detected":
        confidence = random.randint(55, 75)
    else:
        confidence = random.randint(60, 88)

    return {
        "disease": disease["name"],
        "confidence": confidence,
        "explanation": disease["explanation"],
        "treatment": disease["treatment"],
    }


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("🌱 AI Crop Disease Detection")
st.caption("1M1B AI for Sustainability Virtual Internship · SDG 2 — Zero Hunger")

st.warning(
    "⚠️ **Demo Mode:** This version uses simple image heuristics to simulate "
    "AI output for demonstration purposes — it does NOT call a real AI model "
    "and is not a certified diagnostic tool. The full version (`app.py`) uses "
    "Claude's vision model with a real API key.",
    icon="⚠️",
)

st.write(
    "Upload a photo of a crop leaf. The demo will simulate disease detection, "
    "confidence scoring, and treatment suggestions — exactly how the real "
    "AI-powered version behaves."
)

uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded leaf image", use_container_width=True)

    if st.button("Analyze Image", type="primary"):
        with st.spinner("Analyzing leaf image..."):
            result = mock_analyze(image)

        st.success("Analysis complete")

        st.markdown(f"**Detected Disease:** {result['disease']}")
        st.markdown(f"**Confidence Level:** {result['confidence']}%")
        st.progress(result["confidence"] / 100)
        st.markdown(f"**Explanation:** {result['explanation']}")
        st.markdown("**Recommended Treatment:**")
        for step in result["treatment"]:
            st.markdown(f"- {step}")
        st.info(
            "🩺 **Expert Consultation Advice:** If symptoms persist beyond 5–7 "
            "days or worsen, consult a local agricultural expert before applying "
            "further treatment."
        )
else:
    st.info("👆 Upload a leaf image to see a simulated AI diagnosis.")

st.markdown("---")
st.caption(
    "Built as part of the 1M1B AI for Sustainability Virtual Internship "
    "(with IBM SkillsBuild & AICTE). Demo mode — not a substitute for "
    "professional agricultural advice."
)
