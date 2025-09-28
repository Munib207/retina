import streamlit as st

# ===== PAGE SETUP =====
st.set_page_config(
    page_title="Retina Curriculum App",
    page_icon="👁️",
    layout="wide"
)

# ===== DATA EMBEDDED (Curriculum + Case Bank) =====
CURRICULUM = {
    "modules": [
        {
            "id": "foundations",
            "title": "Foundations & Anatomy",
            "objectives": [
                "Understand retinal layers and blood supply",
                "Perform indirect ophthalmoscopy and slit lamp fundus exam",
                "Interpret basic OCT features"
            ],
            "topics": [
                {
                    "id": "retina_anatomy",
                    "title": "Retina Anatomy & Histology",
                    "content": "The retina has 10 layers, with the macula and fovea specialized for central vision. The optic disc is the exit point of the optic nerve.",
                    "image": None
                },
                {
                    "id": "imaging_basics",
                    "title": "Imaging Basics (OCT, Fundus)",
                    "content": "OCT provides cross-sectional imaging. Fundus photos give a color overview of retinal health.",
                    "image": None
                }
            ]
        },
        {
            "id": "medical_retina",
            "title": "Medical Retina Diseases",
            "objectives": [
                "Differentiate NPDR vs PDR in diabetic retinopathy",
                "Recognize dry vs wet AMD",
                "Interpret OCT changes of macular edema"
            ],
            "topics": [
                {
                    "id": "diabetic_retinopathy",
                    "title": "Diabetic Retinopathy",
                    "content": "Microaneurysms, hemorrhages, and exudates are hallmarks. May progress to proliferative DR with neovascularization.",
                    "image": None
                },
                {
                    "id": "amd",
                    "title": "Age-Related Macular Degeneration (AMD)",
                    "content": "Dry AMD has drusen. Wet AMD has choroidal neovascularization and subretinal fluid.",
                    "image": None
                },
                {
                    "id": "vascular_occlusions",
                    "title": "Retinal Vascular Occlusions",
                    "content": "Includes CRVO and BRVO; often cause sudden painless vision loss.",
                    "image": None
                }
            ]
        },
        {
            "id": "surgical_retina",
            "title": "Surgical & Procedural Retina",
            "objectives": [
                "Understand indications for retinal detachment repair",
                "Know steps of vitrectomy and PRP",
                "Perform intravitreal injections safely"
            ],
            "topics": [
                {
                    "id": "retinal_detachment",
                    "title": "Retinal Detachment",
                    "content": "Rhegmatogenous, tractional, and exudative types. Symptoms: flashes, floaters, curtain vision.",
                    "image": None
                },
                {
                    "id": "laser_and_injections",
                    "title": "Laser & Injections",
                    "content": "PRP and intravitreal anti-VEGF are common treatments.",
                    "image": None
                }
            ]
        }
    ]
}

CASES = [
    {
        "id": "case1",
        "title": "Sudden Curtain Vision Loss",
        "history": "55-year-old male with sudden floaters and curtain vision.",
        "questions": [
            {
                "q": "Most likely diagnosis?",
                "options": ["Retinal Detachment", "Macular Hole", "CRVO"],
                "correct": "Retinal Detachment",
                "explanation": "Curtain vision with floaters is classic for detachment."
            },
            {
                "q": "Best diagnostic test?",
                "options": ["OCT", "B-scan Ultrasound", "FA"],
                "correct": "B-scan Ultrasound",
                "explanation": "B-scan helps confirm detachment if fundus view is poor."
            }
        ]
    },
    {
        "id": "case2",
        "title": "Blurred Central Vision in Diabetes",
        "history": "60-year-old diabetic with central blur. OCT shows cystic spaces.",
        "questions": [
            {
                "q": "Most likely condition?",
                "options": ["Macular Edema", "CRVO", "AMD"],
                "correct": "Macular Edema",
                "explanation": "Cystic spaces in diabetes = DME."
            },
            {
                "q": "Best treatment?",
                "options": ["Laser PRP", "Anti-VEGF injection", "Vitrectomy"],
                "correct": "Anti-VEGF injection",
                "explanation": "Anti-VEGF is first-line for DME."
            }
        ]
    }
]

# ===== APP LAYOUT =====
st.title("👁️ Retina Educational App")

st.sidebar.title("Navigation")
section = st.sidebar.radio("Choose section:", ["Curriculum", "Cases"])

# ---- CURRICULUM SECTION ----
if section == "Curriculum":
    st.header("📚 Retina Curriculum")
    for module in CURRICULUM["modules"]:
        with st.expander(f"🔹 {module['title']}"):
            st.subheader("Objectives")
            for obj in module["objectives"]:
                st.write(f"- {obj}")
            st.subheader("Topics")
            for topic in module["topics"]:
                st.markdown(f"**{topic['title']}**")
                st.write(topic["content"])
                st.markdown("---")

# ---- CASES SECTION ----
elif section == "Cases":
    st.header("🩺 Clinical Cases")
    for case in CASES:
        with st.expander(f"Case: {case['title']}"):
            st.write(f"**History:** {case['history']}")
            for i, q in enumerate(case["questions"], 1):
                ans = st.radio(f"Q{i}. {q['q']}", q["options"], key=f"{case['id']}_{i}")
                if st.button(f"Check Q{i}", key=f"btn_{case['id']}_{i}"):
                    if ans == q["correct"]:
                        st.success(f"✅ Correct! {q['explanation']}")
                    else:
                        st.error(f"❌ Wrong. {q['explanation']}")

# ===== FOOTER =====
st.markdown("---")
st.caption("Lightweight Retina App — single-file deployment version.")
