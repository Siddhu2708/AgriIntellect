import streamlit as st
import json
import os
from groq import Groq
import pdf_generator
from utils import translate_text, load_config

SOIL_JSON_PATH = os.path.join(os.path.dirname(__file__), "soil.json")


def save_soil_to_json(data: dict):
    """Save soil parameters to soil.json silently."""
    try:
        with open(SOIL_JSON_PATH, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        pass


def call_groq_soil_analysis(soil_data: dict, language: str = "English") -> str:
    """Call Groq AI API with soil data and return analysis in the given language."""
    try:
        config = load_config()
        groq_api_key = config.get("GROQ_API_KEY", "")
        client = Groq(api_key=groq_api_key)

        lang_instruction = (
            f"IMPORTANT: Write your ENTIRE response in {language} language.\n"
            "Do NOT change the format or structure — only the language of the content changes.\n\n"
            if language != "English" else ""
        )

        prompt = (
            f"{lang_instruction}"
            "You are an agriculture assistant.\n\n"
            "Convert the given soil analysis data into a clean, structured, farmer-friendly format.\n\n"
            "Follow STRICT formatting rules:\n"
            "1. Show main headings in bold using **heading** syntax.\n"
            "2. Keep content short, clear, and easy to understand.\n"
            "3. Do NOT give long paragraphs. Use 2-3 lines maximum for descriptions.\n"
            "4. Use numbered lists where required. Provide multiple detailed points (ideally 4-6) for each list to ensure the farmer has all necessary information.\n"
            "5. Format lists as: 1. Name: Short info\n"
            "6. Avoid repetition and unnecessary details.\n"
            "7. Do NOT include symbols like *, -, or markdown except bold headings.\n\n"
            "Output format exactly like this template:\n\n"
            "**Detected Soil:** Acidic Soil\n\n"
            "**Soil Type:** Sandy Loam\n\n"
            "**Soil Information:** This soil has low pH and nutrient levels. It requires fertilization to support plant growth.\n\n"
            "**Fertilizer Recommendations:**\n"
            "1. Name: Info\n\n"
            "2. Name: Info\n\n"
            "3. Name: Info\n\n"
            "4. Name: Info\n\n"
            "5. Name: Info\n\n"
            "6. Name: Info\n\n"
            "**Recommended Crops:**\n"
            "1. Name: Info\n\n"
            "2. Name: Info\n\n"
            "3. Name: Info\n\n"
            "4. Name: Info\n\n"
            "5. Name: Info\n\n"
            "6. Name: Info\n\n"
            "Now format the following soil data:\n"
            f"pH: {soil_data.get('ph')}\n"
            f"Nitrogen (N): {soil_data.get('nitrogen')} mg/kg\n"
            f"Phosphorus (P): {soil_data.get('phosphorus')} mg/kg\n"
            f"Potassium (K): {soil_data.get('potassium')} mg/kg\n"
            f"Organic Matter: {soil_data.get('organic_matter')}%\n"
            f"Soil Moisture: {soil_data.get('soil_moisture')}%"
        )

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            temperature=0.4,
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"AI analysis unavailable: {str(e)}\n\nPlease check your GROQ_API_KEY in config.json."


def soil_home(sarvam_client, language):

    def t(text):
        return translate_text(sarvam_client, text, language)

    # ── Welcome ───────────────────────────────────────────────────────────────
    st.title(f"🌾 {t('Welcome to Soil Health Analysis System!')}")

    st.write(t("Your intelligent assistant for understanding soil health and improving crop productivity."))
    st.write(t("Use the Soil Analysis module to:"))

    st.markdown(f"""
- {t('Analyze soil nutrients like Nitrogen, Phosphorus, and Potassium.')}
- {t('Get recommended crops suitable for your soil type.')}
- {t('Receive fertilizer suggestions to improve soil fertility.')}
- {t('Improve crop yield with data-driven decisions.')}
    """)

    st.markdown("---")

    # ── Soil Form ─────────────────────────────────────────────────────────────
    st.header(f"🧪 {t('Soil Parameter Analysis')}")
    st.write(f"📥 **{t('Enter your soil parameters below')}** *(all fields required)*")

    fc1, fc2 = st.columns(2)
    with fc1:
        ph             = st.number_input(t("Soil pH"),              min_value=0.0, max_value=14.0, step=0.1, value=None, placeholder="0.0 – 14.0")
        nitrogen       = st.number_input(t("Nitrogen (N) mg/kg"),   min_value=0.0, value=None, placeholder=t("Enter value"))
        phosphorus     = st.number_input(t("Phosphorus (P) mg/kg"), min_value=0.0, value=None, placeholder=t("Enter value"))
    with fc2:
        potassium      = st.number_input(t("Potassium (K) mg/kg"),  min_value=0.0, value=None, placeholder=t("Enter value"))
        organic_matter = st.number_input(t("Organic Matter (%)"),   min_value=0.0, max_value=100.0, value=None, placeholder="0.0 – 100.0")
        soil_moisture  = st.number_input(t("Soil Moisture (%)"),    min_value=0.0, max_value=100.0, value=None, placeholder="0.0 – 100.0")

    analyze = st.button(f"🔍 {t('Analyze Soil')}", use_container_width=True, type="primary")

    # ── Results ───────────────────────────────────────────────────────────────
    if analyze:
        # Required field validation
        missing = []
        if ph is None:             missing.append(t("Soil pH"))
        if nitrogen is None:       missing.append(t("Nitrogen (N)"))
        if phosphorus is None:     missing.append(t("Phosphorus (P)"))
        if potassium is None:      missing.append(t("Potassium (K)"))
        if organic_matter is None: missing.append(t("Organic Matter"))
        if soil_moisture is None:  missing.append(t("Soil Moisture"))

        if missing:
            st.error(f"⚠️ {t('Please fill in all required fields')}: {', '.join(missing)}")
        else:
            soil_data = {
                "ph":             ph,
                "nitrogen":       nitrogen,
                "phosphorus":     phosphorus,
                "potassium":      potassium,
                "organic_matter": organic_matter,
                "soil_moisture":  soil_moisture,
            }

            st.markdown("---")
            st.subheader(f"📊 {t('Soil Analysis Results')}")

            with st.spinner(t("Analyzing your soil... please wait")):
                ai_result = call_groq_soil_analysis(soil_data, language)

            # Save result to JSON
            soil_data_to_save = soil_data.copy()
            soil_data_to_save["ai_analysis"] = ai_result
            save_soil_to_json(soil_data_to_save)

            st.write(ai_result)

            pdf_bytes = pdf_generator.generate_pdf_bytes("SOIL ANALYSIS REPORT", soil_data, ai_result)

            if st.button(f"🏪 {t('Visit Shop for Products')}", use_container_width=True, key="soil_res_shop_btn"):
                    st.session_state["nav_idx"] = 3
                    st.rerun()

            scol1, scol2 = st.columns(2)
            with scol1:
                st.download_button(
                    label=f"📥 {t('Download Soil Report')}",
                    data=pdf_bytes,
                    file_name="soil_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                

    st.markdown("---")

        # ── Special Offer ─────────────────────────────────────────────────────────

    st.header(f"🌟 {t('Special Offer for Farmers!')}")

    col1, col2 = st.columns ( [2, 1] )
    with col1 :

        st.subheader(t("Buy Premium Fertilizers & Organic Products Now!"))
        st.write(f"""
            - {t('High-quality NPK fertilizers for all soil types.')}
            - {t('Organic compost and cow dung fertilizers available.')}
            - {t('Special **15% discount** for first-time buyers!')}
        """)

        st.subheader(f"🌟 {t('Why choose our products?')}")
        st.markdown(f"""
            - {t('Scientifically formulated for Indian soil conditions.')}
            - {t('Supports sustainable and organic farming practices.')}
            - {t('Trusted by thousands of farmers across India.')}
        """)

    if st.button(f"👉 {t('Visit Our Shop')}", key="soil_shop_btn"):
        st.session_state["nav_idx"] = 3
        st.rerun()
        

    with col2 :
        st.image(
            "./image/soil.png",
            caption=t("Fresh produce – protect your crops with early disease detection"),
            use_column_width=True
        )

    

    st.markdown("---")

    # ── Thank You ─────────────────────────────────────────────────────────────
    st.header(f"🍃 {t('Thank You for Using Soil Analysis!')}")

    st.write(f"""
{t('We are dedicated to helping farmers understand their soil and grow better crops.')}

{t('If you have any questions or need assistance, feel free to reach out.')}
    """)

    st.success(f"🌱 {t('Happy Farming!')}")
