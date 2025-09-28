import streamlit as st
from PIL import Image
import base64
import os

# ===== PAGE SETUP =====
st.set_page_config(
    page_title="Retina LMS — Polished",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS (Polished LMS look) =====
_STYLES = """
<style>
:root{
  --bg:#0f1724; /* deep navy */
  --card:#0b1220; /* card bg */
  --muted:#94a3b8;
  --accent:#0ea5a4; /* teal */
  --glass: rgba(255,255,255,0.03);
}
html, body, [data-testid='stAppViewContainer'] {
  background: linear-gradient(180deg, #071020 0%, #0b1220 100%);
  color: #e6eef6;
}
.stApp {
  font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
}
.header-card {
  background: linear-gradient(90deg, rgba(14,165,164,0.12), rgba(59,130,246,0.08));
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.6);
  margin-bottom: 16px;
}
.card {
  background: var(--card);
  border-radius: 10px;
  padding: 14px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.5);
  border: 1px solid rgba(255,255,255,0.03);
}
.module-title { font-size: 18px; font-weight: 700; color: #e6f0ff; }
.objective { color: var(--muted); margin-bottom:6px }
.topic { background: var(--glass); padding:10px; border-radius:8px; margin-bottom:8px }
.small-muted { color: var(--muted); font-size:13px }
.case-q { background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); padding:10px; border-radius:8px; }
.btn-primary{ background-color: var(--accent); color: #042027; padding:8px 12px; border-radius:8px; }
.progress-pill { background: rgba(255,255,255,0.04); padding:6px 10px; border-radius:999px; display:inline-block }
</style>
"""

st.markdown(_STYLES, unsafe_allow_html=True)

# ===== Initialize session state for tracking =====
if "modules_done" not in st.session_state:
    st.session_state.modules_done = set()
if "cases_done" not in st.session_state:
    st.session_state.cases_done = set()
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

# ===== Embedded curriculum (plain text) =====
CURRICULUM = [
    {
        "id": "foundations",
        "title": "Foundations & Anatomy",
        "objectives": [
            "Understand retinal layers and blood supply",
            "Perform slit-lamp + 90D and indirect ophthalmoscopy",
            "Interpret basic OCT features"
        ],
        "topics": [
            {"id": "retina_anatomy", "title": "Retina Anatomy & Histology", "content": "The retina comprises multiple layers (RPE, photoreceptors, ONL, INL, GCL etc). Macula and fovea are specialized for central vision.", "image": None},
            {"id": "imaging_basics", "title": "Imaging Basics (OCT, Fundus)", "content": "OCT cross-sections, fundus photography overview, how OCT reflects layers.", "image": None}
        ]
    },
    {
        "id": "medical_retina",
        "title": "Medical Retina Diseases",
        "objectives": [
            "Differentiate NPDR vs PDR",
            "Recognize dry vs wet AMD",
            "Interpret OCT changes of macular edema"
        ],
        "topics": [
            {"id": "diabetic_retinopathy", "title": "Diabetic Retinopathy", "content": "Microaneurysms, dot-blot hemorrhages, hard exudates and macular edema. Indications for laser and anti-VEGF.", "image": None},
            {"id": "amd", "title": "Age-related Macular Degeneration (AMD)", "content": "Dry: drusen and RPE atrophy. Wet: CNV, subretinal fluid; treated with anti-VEGF.", "image": None},
            {"id": "vascular_occlusions", "title": "Retinal Vascular Occlusions", "content": "CRVO/BRVO: sudden painless loss, may cause macular edema and neovascularization.", "image": None}
        ]
    },
    {
        "id": "surgical_retina",
        "title": "Surgical & Procedural Retina",
        "objectives": [
            "Understand indications for retinal detachment repair",
            "Principles of vitrectomy and scleral buckle",
            "Safe intravitreal injection technique"
        ],
        "topics": [
            {"id": "retinal_detachment", "title": "Retinal Detachment", "content": "Rhegmatogenous, tractional, exudative detachments; symptoms: flashes, floaters, curtain vision.", "image": None},
            {"id": "laser_injections", "title": "Laser & Intravitreal Injections", "content": "PRP, focal/grid laser, anti-VEGF injections; asepsis and complications.", "image": None}
        ]
    }
]

# ===== Embedded Cases (plain text) =====
CASES = [
    {
        "id": "case1",
        "title": "Sudden Curtain Vision Loss",
        "history": "55-year-old male with sudden floaters and a curtain coming over the right eye since 3 hours.",
        "questions": [
            {"id": "c1q1", "q": "Most likely diagnosis?", "options": ["Retinal Detachment", "Macular Hole", "CRVO"], "correct": "Retinal Detachment", "explanation": "Curtain-like vision with floaters is classic for rhegmatogenous retinal detachment."},
            {"id": "c1q2", "q": "Next best diagnostic test if view is limited?", "options": ["OCT", "B-scan Ultrasound", "Fluorescein Angiography"], "correct": "B-scan Ultrasound", "explanation": "B-scan confirms detachment when media opacities prevent fundus view."}
        ]
    },
    {
        "id": "case2",
        "title": "Diabetic Macular Edema",
        "history": "60-year-old with diabetes and progressive central blur. OCT shows intraretinal cysts in the macula.",
        "questions": [
            {"id": "c2q1", "q": "Most likely condition?", "options": ["Macular Edema", "CRVO", "AMD"], "correct": "Macular Edema", "explanation": "Cystic intraretinal spaces in a diabetic patient indicate diabetic macular edema (DME)."},
            {"id": "c2q2", "q": "First-line management for center-involving DME?", "options": ["PRP", "Intravitreal anti-VEGF", "Immediate vitrectomy"], "correct": "Intravitreal anti-VEGF", "explanation": "Anti-VEGF therapy is standard of care for center-involving DME."}
        ]
    }
]

# ===== Utility functions =====

def _coloured_markdown(txt, size=14):
    st.markdown(f"<div style='color:#e6eef6;font-size:{size}px'>{txt}</div>", unsafe_allow_html=True)


def _show_progress():
    total_modules = len(CURRICULUM)
    done = len(st.session_state.modules_done)
    pct = int((done / total_modules) * 100) if total_modules else 0
    st.markdown(f"<div class='progress-pill'>Modules complete: <b>{done}/{total_modules}</b> &nbsp; • &nbsp; <b>{pct}%</b></div>", unsafe_allow_html=True)


# ===== HEADER =====
with st.container():
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center'>")
    st.markdown("<div><h2 style='margin:0'>👁️ Retina Curriculum — Postgraduate</h2><div class='small-muted'>Comprehensive, case-based modules for residents</div></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:right'><span style='font-size:14px;color:var(--muted)'>Progress</span><br/>")
    _show_progress()
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== SIDEBAR NAVIGATION & QUICK STATS =====
st.sidebar.markdown("# Navigation")
nav_choice = st.sidebar.selectbox("Open:", ["Curriculum", "Cases", "My Progress", "About"], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("<div class='small-muted'>Quick actions</div>", unsafe_allow_html=True)
if st.sidebar.button("Mark all modules done"):
    for m in CURRICULUM:
        st.session_state.modules_done.add(m['id'])
if st.sidebar.button("Reset progress"):
    st.session_state.modules_done = set()
    st.session_state.cases_done = set()
    st.session_state.quiz_score = 0

st.sidebar.markdown("---")
st.sidebar.markdown("<div class='small-muted'>Support</div>", unsafe_allow_html=True)
st.sidebar.markdown("Email: training@retina.example (placeholder)")

# ===== MAIN VIEWS =====
if nav_choice == "Curriculum":
    st.header("📚 Curriculum Modules")
    for module in CURRICULUM:
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"<div class='card'> <div class='module-title'>🔹 {module['title']}</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:600;color:var(--muted)'>Objectives</div>", unsafe_allow_html=True)
            for obj in module['objectives']:
                st.markdown(f"<div class='objective'>• {obj}</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:600;color:var(--muted)'>Topics</div>", unsafe_allow_html=True)
            for topic in module['topics']:
                st.markdown(f"<div class='topic'><b>{topic['title']}</b><div class='small-muted'>{topic['content']}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            done_flag = module['id'] in st.session_state.modules_done
            if done_flag:
                st.markdown("<div class='card' style='text-align:center'>✅ Module completed</div>", unsafe_allow_html=True)
                if st.button(f"Mark as not done", key=f"undo_{module['id']}"):
                    st.session_state.modules_done.discard(module['id'])
            else:
                st.markdown("<div class='card' style='text-align:center'>Progress</div>", unsafe_allow_html=True)
                if st.button(f"Mark as done", key=f"done_{module['id']}"):
                    st.session_state.modules_done.add(module['id'])
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

elif nav_choice == "Cases":
    st.header("🩺 Case Bank & Interactive Cases")
    for case in CASES:
        with st.expander(f"{case['title']}"):
            st.markdown(f"<div class='card'><div style='font-weight:700'>{case['title']}</div><div class='small-muted' style='margin-bottom:8px'>{case['history']}</div>", unsafe_allow_html=True)
            for q in case['questions']:
                st.markdown(f"<div class='case-q'><b>{q['q']}</b></div>", unsafe_allow_html=True)
                cols = st.columns([3,1])
                with cols[0]:
                    choice = st.radio("Select:", q['options'], key=f"{case['id']}_{q['id']}")
                with cols[1]:
                    if st.button("Check", key=f"chk_{case['id']}_{q['id']}"):
                        if choice == q['correct']:
                            st.success(f"Correct — {q['explanation']}")
                            st.session_state.quiz_score += 1
                        else:
                            st.error(f"Incorrect — {q['explanation']}")
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button(f"Mark case '{case['id']}' complete", key=f"mark_{case['id']}"):
                st.session_state.cases_done.add(case['id'])

elif nav_choice == "My Progress":
    st.header("📈 My Progress & Scores")
    st.markdown("<div class='card' style='padding:18px'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700'>Modules completed: {len(st.session_state.modules_done)} / {len(CURRICULUM)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700'>Cases completed: {len(st.session_state.cases_done)} / {len(CASES)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700'>Quiz score (session): {st.session_state.quiz_score}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Tip: your progress is stored in the current session. For long-term tracking, integrate this with a backend or Google Sheets export.</div>", unsafe_allow_html=True)

else:
    st.header("About this App")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<b>Retina Curriculum — Polished LMS-style</b>", unsafe_allow_html=True)
    st.markdown("This single-file app includes a curriculum, case bank, and light progress tracking for postgraduate ophthalmology residents.", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("---")
st.caption("Built for postgraduate retina education — editable plain-text curriculum & cases inside this file.")
