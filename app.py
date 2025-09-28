import streamlit as st
from PIL import Image
import os

# ===== PAGE SETUP =====
st.set_page_config(
    page_title="Retina App - Educational Curriculum",
    page_icon="👁️",
    layout="wide"
)

# ===== Custom CSS for lighter theme =====
st.markdown(
    """
    <style>
    body {
        background-color: #f8f9fa;
        color: #212529;
        font-family: "Helvetica Neue", Arial, sans-serif;
    }
    .main-title {
        color: #0d47a1;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .card {
        background-color: #ffffff;
        padding: 20px;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #1976d2;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover {
        background-color: #0d47a1;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== Initialize session state =====
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "completed_modules" not in st.session_state:
    st.session_state.completed_modules = set()

# ===== Helper to load images safely =====
def _load_image(fname):
    if os.path.exists(fname):
        try:
            return Image.open(fname)
        except Exception:
            return None
    return None

# ===== App UI =====
st.markdown('<div class="main-title">👁️ Retina Interactive Curriculum</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", [
    "Introduction", "Anatomy", "Diseases", "Cases", "Quiz"
])

if section == "Introduction":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Introduction to Retina")
    st.write(
        """
        The **retina** is the light-sensitive layer of tissue at the back of the eye.  
        It converts light into electrical signals, which are sent to the brain via the optic nerve.  
        Understanding the retina is crucial for diagnosing and managing many eye diseases.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.completed_modules.add("Introduction")

elif section == "Anatomy":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Retinal Anatomy")
    st.write(
        """
        - **Macula**: Central vision, responsible for detail and color.  
        - **Fovea**: Center of the macula, highest visual acuity.  
        - **Optic Disc**: Blind spot where the optic nerve exits.  
        - **Retinal Blood Supply**: Central retinal artery + choroidal circulation.  
        """
    )
    img = _load_image("retina_anatomy.jpg")
    if img:
        st.image(img, caption="Diagram of the Retina", use_column_width=True)
    else:
        st.info("Image 'retina_anatomy.jpg' not found. Place an anatomy diagram in the app folder.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.completed_modules.add("Anatomy")

elif section == "Diseases":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Common Retinal Diseases")
    disease = st.selectbox("Choose a disease:", [
        "Diabetic Retinopathy", "Age-related Macular Degeneration (AMD)", "Retinal Detachment"
    ])

    if disease == "Diabetic Retinopathy":
        img = _load_image("diabetic_retinopathy.jpg")
        if img:
            st.image(img, caption="Fundus Photo - Diabetic Retinopathy", use_column_width=True)
        else:
            st.info("Image 'diabetic_retinopathy.jpg' not found. Add a fundus photo in the app folder.")
        st.write(
            """
            - Microaneurysms, dot-and-blot hemorrhages, hard exudates.  
            - Can progress to proliferative stage with neovascularization.  
            - Screening with fundus photography and OCT is essential.
            """
        )

    elif disease == "Age-related Macular Degeneration (AMD)":
        img = _load_image("amd_oct.jpg")
        if img:
            st.image(img, caption="OCT of Wet AMD", use_column_width=True)
        else:
            st.info("Image 'amd_oct.jpg' not found. Add an OCT image in the app folder.")
        st.write(
            """
            - **Dry AMD**: Drusen deposits, gradual vision loss.  
            - **Wet AMD**: Choroidal neovascularization causes rapid central vision loss.  
            - OCT and fluorescein angiography help in diagnosis and monitoring.
            """
        )

    elif disease == "Retinal Detachment":
        st.write(
            """
            - Symptoms: Flashes, floaters, curtain-like shadow.  
            - Rhegmatogenous detachment is most common.  
            - Emergency: prompt surgical intervention often preserves vision.
            """
        )

    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.completed_modules.add("Diseases")

elif section == "Cases":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Interactive Clinical Cases")
    st.write("Case 1: A 55-year-old presents with sudden onset of floaters and a curtain-like loss of vision.")
    case = st.radio(
        "What is the most likely diagnosis?",
        ["Retinal Detachment", "Macular Hole", "Central Retinal Vein Occlusion (CRVO)"]
    )
    if case == "Retinal Detachment":
        st.success("✅ Correct! This is a classic presentation for rhegmatogenous retinal detachment.")
    else:
        st.error("❌ Not quite — consider the hallmark symptoms of detachment: flashes, floaters, and a curtain over vision.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.completed_modules.add("Cases")

elif section == "Quiz":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Quick Quiz")
    q1 = st.radio("Which test is best for diagnosing Macular Edema?", [
        "Visual Acuity Test", "OCT", "Intraocular Pressure Measurement"
    ])
    if st.button("Check answer"):
        if q1 == "OCT":
            st.success("✅ Correct! OCT is the gold standard for detecting and quantifying macular edema.")
            st.session_state.quiz_score += 1
        else:
            st.error("❌ That's not correct. OCT is the most appropriate test for macular edema.")
        st.write(f"Your quiz score: {st.session_state.quiz_score}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.completed_modules.add("Quiz")

# ===== Progress Tracker =====
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Progress Tracker")
total_modules = 5
completed = len(st.session_state.completed_modules)
st.sidebar.progress(completed / total_modules)
st.sidebar.write(f"{completed} of {total_modules} modules completed")

# ===== Footer =====
st.markdown("---")
st.caption("Created as a postgraduate educational retina app — drop three image files in the same folder: retina_anatomy.jpg, diabetic_retinopathy.jpg, amd_oct.jpg")
