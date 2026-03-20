import streamlit as st

from utils import translate_text

def home_default(sarvam_client, language):

    def t(text):
        return translate_text(sarvam_client, text, language)

    # ── Welcome ───────────────────────────────────────────────────────────────
    st.title(f"🌱 {t('Welcome to AgrIntellect')}")
    st.subheader(t("Smart AI Platform for Modern Agriculture"))

    st.write(t(
        "AgrIntellect helps farmers make better decisions using AI-powered agriculture tools. "
        "Our platform integrates soil intelligence, disease detection, and crop residue management "
        "to improve productivity and promote sustainable farming."
    ))

    st.markdown("---")

    # ── Module 1: Soil Analysis ───────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"🌾 {t('Soil Health Analysis System')}")
        st.write(t("Your ultimate companion for understanding soil conditions and improving crop productivity."))
        st.write(t("Use the Soil Analysis System to:"))
        st.markdown(f"""
- {t('Analyze soil nutrients and health.')}
- {t('Get crop recommendations based on soil conditions.')}
- {t('Receive fertilizer suggestions for better yields.')}
- {t('Improve soil fertility using data-driven insights.')}
        """)
        st.subheader(f"🌿 {t('What Our System Provides')}")
        st.markdown(f"""
- {t('Soil health status evaluation')}
- {t('Recommended crops for your land')}
- {t('Fertilizer suggestions and soil improvement tips')}
        """)

    with col2:
        st.image(
            "https://sustainable-earth.org/wp-content/uploads/AOE-Blog-Organic-Soil-e1678985025262.jpeg",
            caption=t("Healthy soil – the foundation of great farming"),
            use_column_width=True
        )

    st.markdown("---")

    # ── Module 2: Disease Detection ───────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"🩺 {t('Plant Disease Detection System')}")
        st.write(t("Your intelligent assistant for identifying crop diseases and protecting plant health."))
        st.write(t("Use the Disease Detection System to:"))
        st.markdown(f"""
- {t('Detect and diagnose diseases in plant leaves.')}
- {t('Get expert advice and treatment recommendations.')}
- {t('Receive pesticide suggestions and prevention methods.')}
- {t('Protect your harvest with early disease identification.')}
        """)
        st.subheader(f"🔍 {t('What Our System Provides')}")
        st.markdown(f"""
- {t('AI-powered leaf disease diagnosis')}
- {t('Expert pesticide & treatment recommendations')}
- {t('Disease prevention and crop protection tips')}
        """)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=600&q=80",
            caption=t("Fresh produce – protect your crops with early disease detection"),
            use_column_width=True
        )

    st.markdown("---")

    # ── Module 3: Residue Management ─────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"♻️ {t('Crop Residue Management System')}")
        st.write(t(
            "Your smart solution for converting crop residue into valuable resources "
            "instead of burning it."
        ))
        st.write(t("Use the Residue Management System to:"))
        st.markdown(f"""
- {t('Estimate crop residue after harvest.')}
- {t('Connect farmers with residue buyers.')}
- {t('Explore profitable residue uses like biochar or compost.')}
- {t('Check eligibility for government subsidy programs.')}
        """)
        st.subheader(f"💰 {t('Benefits for Farmers')}")
        st.markdown(f"""
- {t('Earn extra income by selling crop residue')}
- {t('Connect with biomass industries and buyers')}
- {t('Access government subsidy schemes')}
- {t('Reduce pollution caused by stubble burning')}
        """)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1625246333195-78d9c38ad449",
            use_column_width=True
        )

    st.markdown("---")

    # ── Closing Banner ────────────────────────────────────────────────────────
    st.markdown(f"""
<h2>🍃 {t('Thank you for using AgrIntellect!')}</h2>

{t('We are dedicated to helping farmers adopt **smart, sustainable, and profitable farming practices**.')}

<h4>🌱 {t('Happy Farming!')}</h4>
    """, unsafe_allow_html=True)