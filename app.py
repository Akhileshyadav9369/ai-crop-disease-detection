"""
AI-Based Crop Disease Detection
--------------------------------
A Streamlit prototype built for the 1M1B AI for Sustainability Virtual Internship
(in collaboration with IBM SkillsBuild & AICTE).

How it works:
1. Farmer/user uploads a photo of a crop leaf.
2. The image is sent to a multimodal AI model (Claude) along with a structured prompt.
3. The model returns: detected disease, confidence level, and safe treatment steps.

Run locally:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY="your-api-key-here"
    streamlit run app.py
"""

import base64
import os

import streamlit as st
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Crop Disease Detection",
    page_icon="🌱",
    layout="centered",
)

MODEL_NAME = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are an agricultural assistant helping farmers identify possible crop
diseases from leaf images. You are not a replacement for an expert — always be honest about
uncertainty.

For every image, respond in this exact structure:

Detected Disease: <name or 'No visible disease detected'>
Confidence Level: <percentage, e.g. 65%>
Explanation: <1-2 sentences on visible symptoms that led to this conclusion>
Recommended Treatment:
- <safe, low-cost step 1>
- <safe, low-cost step 2>
Expert Consultation Advice: <when the farmer should consult a local agricultural expert
instead of relying on this tool alone>

Rules:
- Never claim certainty above 90% confidence.
- If the image is unclear or not a leaf, say so directly instead of guessing.
- Recommend only safe, widely-used, low-cost treatments (no restricted or hazardous chemicals).
- Keep the tone simple and farmer-friendly, avoiding technical jargon where possible.
"""


def encode_image(uploaded_file) -> tuple[str, str]:
    """Return (base64_data, media_type) for an uploaded image file."""
    file_bytes = uploaded_file.getvalue()
    media_type = uploaded_file.type or "image/jpeg"
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return encoded, media_type


def analyze_leaf_image(api_key: str, image_b64: str, media_type: str) -> str:
    """Send the image to Claude and return the structured diagnosis text."""
    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Analyze this crop leaf image and follow the response structure exactly.",
                    },
                ],
            }
        ],
    )

    return "".join(block.text for block in response.content if block.type == "text")


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("🌱 AI Crop Disease Detection")
st.caption(
    "1M1B AI for Sustainability Virtual Internship · SDG 2 — Zero Hunger"
)

st.write(
    "Upload a photo of a crop leaf. The AI will identify possible disease symptoms, "
    "give a confidence level, and suggest safe treatment steps."
)

with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        help="Get a key at https://console.anthropic.com",
    )
    st.markdown("---")
    st.markdown(
        "**Responsible AI note:** This tool gives AI-assisted guidance only. "
        "Always confirm severe or persistent cases with a local agricultural expert."
    )

uploaded_file = st.file_uploader(
    "Upload a leaf image", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded leaf image", use_container_width=True)

    if st.button("Analyze Image", type="primary"):
        if not api_key_input:
            st.error("Please enter your Anthropic API key in the sidebar.")
        else:
            with st.spinner("Analyzing leaf image..."):
                try:
                    image_b64, media_type = encode_image(uploaded_file)
                    result = analyze_leaf_image(api_key_input, image_b64, media_type)
                    st.success("Analysis complete")
                    st.markdown(result)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Something went wrong: {exc}")
else:
    st.info("👆 Upload an image to get started, or try a sample image below.")

    sample_dir = "sample_images"
    if os.path.isdir(sample_dir) and os.listdir(sample_dir):
        st.subheader("Sample images")
        cols = st.columns(3)
        for i, fname in enumerate(sorted(os.listdir(sample_dir))[:3]):
            with cols[i % 3]:
                st.image(os.path.join(sample_dir, fname), caption=fname)

st.markdown("---")
st.caption(
    "Built as part of the 1M1B AI for Sustainability Virtual Internship "
    "(with IBM SkillsBuild & AICTE). Not a substitute for professional agricultural advice."
)
