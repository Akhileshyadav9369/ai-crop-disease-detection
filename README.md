## AI-Based Crop Disease Detection

A lightweight AI prototype that helps farmers detect crop diseases early from a simple leaf
photo — reducing crop loss, avoiding unnecessary pesticide use, and supporting sustainable
agriculture.

---

##  Problem Statement

> How might we use AI to detect crop diseases early so that farmers can reduce crop loss and
> farming can become more sustainable?

Many small and marginal farmers lack timely access to agricultural experts or testing labs.
Diseases are often noticed only after significant crop damage has occurred, leading to lost
yield, wasted pesticide spending, and avoidable environmental harm.

##  SDG Alignment

- **Primary:** SDG 2 — Zero Hunger
- **Secondary:** SDG 13 — Climate Action, SDG 15 — Life on Land

##  How It Works

1. User uploads a photo of a crop leaf.
2. The image + a structured prompt is sent to a multimodal AI model (Claude).
3. The model returns:
   - Detected disease (with honest uncertainty — no overclaiming)
   - Confidence level
   - Safe, low-cost treatment suggestions
   - Guidance on when to consult a real agricultural expert

```
Leaf Image ──▶ Upload ──▶ AI Analysis (multimodal) ──▶ Diagnosis + Confidence ──▶ Treatment Steps
```

##  Responsible AI Considerations

| Principle | How it's addressed |
|---|---|
| **Fairness** | Designed to work across crop types and lighting conditions; avoid bias toward a single dataset. |
| **Transparency** | Every result includes a confidence score — never presented as a certain diagnosis. |
| **Ethics** | Always recommends expert consultation for severe/persistent cases. |
| **Privacy** | No personal or location data is stored; images are processed only for the current session. |

##  Getting Started

```bash
git clone https://github.com/<your-username>/ai-crop-disease-detection.git
cd ai-crop-disease-detection
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-api-key-here"   # get one at console.anthropic.com
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

##  Project Structure

```
ai-crop-disease-detection/
├── app.py              # Streamlit prototype application
├── requirements.txt    # Python dependencies
├── sample_images/       # (optional) sample leaf images for demo
└── README.md
```

##  Target Users

Small and marginal farmers, agricultural cooperatives, and extension workers who lack easy
access to in-person crop disease diagnosis.

##  Expected Impact

- Reduced crop loss through earlier detection
- Lower input costs from targeted (not blanket) pesticide use
- Reduced environmental harm from chemical overuse
- Wider access to expert-level guidance for under-served farming communities


