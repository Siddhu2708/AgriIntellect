import streamlit as st
import streamlit.components.v1 as components
import json
import os
from groq import Groq
import pdf_generator
import pandas as pd
from utils import translate_text, load_config

def call_groq_residue_analysis(data: dict, language: str = "English") -> str:
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
            "You are an agriculture assistant specialized in crop residue management.\n\n"
            "Your task is to process farmer input and provide a structured management report.\n\n"
            "Rules for processing input:\n"
            "1. Normalize inputs: Convert crop and equipment names into clean, readable format. Remove duplicates if any.\n"
            "2. Crop Type: If user selected 'Other', use the custom name they provided. Otherwise use the standard name.\n"
            "3. Equipment: Normalize names (e.g., 'tractor' to 'Tractor'). Handle custom equipment if provided.\n\n"
            "Follow STRICT formatting rules for the report:\n"
            "1. Show main headings in bold using **heading** syntax.\n"
            "2. Keep explanations short (2–3 lines only).\n"
            "3. Use numbered lists for methods.\n"
            "4. Format lists as: 1. Name: Short explanation\n"
            "5. Do NOT write long paragraphs.\n"
            "6. Keep output clean and easy to read.\n\n"
            "---\n"
            "Output format EXACTLY like this:\n\n"
            "**Crop:** <final normalized crop name>\n\n"
            "**Location:** <normalized location>\n\n"
            "**Field Size:** <value> acres\n\n"
            "**Available Equipment:**\n"
            "1. <equipment 1>\n"
            "2. <equipment 2>\n\n"
            "**Estimated Residue:** <value>\n\n"
            "**CO₂ Saved:** <value>\n\n"
            "**Residue Information:**\n"
            "<short explanation>\n\n"
            "**Residue Management Methods:**\n"
            "1. Biochar: Info + process\n"
            "2. Biomass Pellets: Info + process\n"
            "3. Composting: Info + process\n"
            "4. Direct Incorporation: Info + process\n\n"
            "**Best Recommended Method:**\n"
            "<method name + short reason based on input>\n\n"
            "**Buyer Suggestion:**\n"
            "<short note like \"Buyers available based on your location\">\n\n"
            "**Government Subsidy:**\n"
            "<short note about subsidy availability based on location>\n\n"
            "---\n\n"
            "Important:\n"
            "- Recommendation must depend on residue amount, crop type, and available equipment.\n"
            "- Keep everything simple for farmers.\n"
            "- Do NOT include unnecessary text or extra explanation.\n\n"
            "Now process the following farmer input:\n"
            f"Location: {data.get('location')}\n"
            f"Crop Type: {data.get('crop')}\n"
            f"Field Size: {data.get('size')} acres\n"
            f"Harvest Season: {data.get('season')}\n"
            f"Available Equipment: {data.get('equipment')}"
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


def residue_home(sarvam_client, language):

    def t(text):
        return translate_text(sarvam_client, text, language)

    if "residue_estimated" not in st.session_state:
        st.session_state.residue_estimated = False
    if "ai_result" not in st.session_state:
        st.session_state.ai_result = None
    if "residue_data" not in st.session_state:
        st.session_state.residue_data = None
    if "residue_video" not in st.session_state:
        st.session_state.residue_video = None

    # ── Welcome ───────────────────────────────────────────────────────────────
    st.title(f"♻️ {t('Welcome to Crop Residue Management System!')}")

    st.write(t("Your eco-friendly assistant for managing and converting crop residue into value."))
    st.write(t("Use the Residue Management module to:"))

    st.markdown(f"""
- {t('Estimate the amount of crop residue from your field.')}
- {t('Discover profitable alternatives to stubble burning.')}
- {t('Convert residue into biochar, pellets, or compost.')}
- {t('Calculate earnings and available government subsidies.')}
    """)

    st.markdown("---")

    # ── Main Feature: Residue Input Form ──────────────────────────────────────
    st.header(f"🌾 {t('Crop Residue Estimator')}")

    st.write(f"📥 **{t('Enter your crop and field details below')}**")

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input(t("Location (State / District)"), value=st.session_state.get('user_location', ''), placeholder="e.g., Punjab, Ludhiana")
        crop_type = st.selectbox(t("Crop Type"), ["Rice", "Wheat", "Corn", "Sugarcane", "Cotton", "Other"])
        custom_crop = ""
        if crop_type == "Other":
            custom_crop = st.text_input(t("Enter Crop Name"), placeholder=t("e.g., Mustard, Barley"))
        field_size = st.number_input(t("Field Size / Land Area (acres)"), min_value=0.1, step=0.1)
    with col2:
        harvest_season = st.selectbox(t("Harvest Season"), ["Kharif", "Rabi", "Zaid"])
        equipment_options = ["None", "Tractor", "Baler", "Rotavator", "Happy Seeder", "Other"]
        equipment = st.multiselect(t("Available Equipment"), equipment_options)
        custom_equipment = ""
        if "Other" in equipment:
            custom_equipment = st.text_input(t("Enter Equipment Name"), placeholder=t("e.g., Mulcher, Shredder"))

    estimate_btn = st.button(f"♻️ {t('Estimate Residue')}", use_container_width=True, type="primary")
    if estimate_btn:
        if not location:
            st.error(t("Please enter your Location."))
        elif crop_type == "Other" and not custom_crop:
            st.error(t("Please enter your Crop Name."))
        elif "Other" in equipment and not custom_equipment:
            st.error(t("Please enter your Equipment Name."))
        else:
            final_crop = custom_crop if crop_type == "Other" else crop_type
            
            # Process multiple equipment
            selected_equipment = [e for e in equipment if e != "Other"]
            if custom_equipment:
                # Add custom equipment to the list
                selected_equipment.append(custom_equipment)
            
            final_equipment = ", ".join(selected_equipment) if selected_equipment else "None"

            residue_data = {
                "location": location,
                "crop": final_crop,
                "size": field_size,
                "season": harvest_season,
                "equipment": final_equipment
            }

            with st.spinner(t("Generating AI Report... please wait")):
                ai_result = call_groq_residue_analysis(residue_data, language)
            
            # Save to session state
            st.session_state.ai_result = ai_result
            st.session_state.residue_estimated = True
            st.session_state.residue_data = residue_data

            # Save input and result to JSON
            residue_data_to_save = residue_data.copy()
            residue_data_to_save["ai_analysis"] = ai_result
            working_dir = os.path.dirname(os.path.abspath(__file__))
            try:
                with open(os.path.join(working_dir, "residue.json"), "w") as f:
                    json.dump(residue_data_to_save, f, indent=4)
            except Exception:
                pass

    if st.session_state.residue_estimated:
        st.markdown("---")
        st.subheader(f"📊 {t('AI Residue Estimation Report')}")
        st.write(st.session_state.ai_result)

        if st.button(f"🏪 {t('Go to Market (Buyers/Sellers/Subsidies)')}", use_container_width=True, key="res_market_redirect"):
            st.session_state["nav_idx"] = 2
            st.rerun()

        st.markdown("---")
        st.subheader(f"🎥 {t('Watch Residue Management Methods')}")
        
        vcol1, vcol2, vcol3, vcol4 = st.columns(4)
        
        with vcol1:
            if st.button(t("Biochar"), use_container_width=True, key="vid_biochar"):
                st.session_state.residue_video = "biochar"
                st.rerun()
        with vcol2:
            if st.button(t("Pellets"), use_container_width=True, key="vid_pellets"):
                st.session_state.residue_video = "pellets"
                st.rerun()
        with vcol3:
            if st.button(t("Composting"), use_container_width=True, key="vid_compost"):
                st.session_state.residue_video = "compost"
                st.rerun()
        with vcol4:
            if st.button(t("Direct"), use_container_width=True, key="vid_direct"):
                st.session_state.residue_video = "direct"
                st.rerun()

        # Display selected video
        if st.session_state.residue_video:
            video_links = {
                "biochar": "https://github.com/rutujdhodapkar/hackthone-2/raw/585a115297cd7939d1789195348d557e5b81e8a5/biochar.mp4",
                "pellets": "https://github.com/rutujdhodapkar/hackthone-2/raw/585a115297cd7939d1789195348d557e5b81e8a5/pellat.mp4",
                "compost": "https://github.com/rutujdhodapkar/hackthone-2/raw/585a115297cd7939d1789195348d557e5b81e8a5/compost.mp4",
                "direct": "https://github.com/rutujdhodapkar/hackthone-2/raw/585a115297cd7939d1789195348d557e5b81e8a5/incorporation.mp4"
            }
            
            st.write(f"📺 **{t('Playing:')} {t(st.session_state.residue_video.capitalize())} {t('Method')}**")
            video_url = video_links[st.session_state.residue_video]
            
            # Use components.html for exact 400x400 sizing and better playback control
            components.html(f"""
                <div style="display: flex; justify-content: center;">
                    <video width="400" height="400" controls key="{st.session_state.residue_video}">
                        <source src="{video_url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            """, height=420)

        st.markdown("---")
        pdf_bytes = pdf_generator.generate_pdf_bytes("CROP RESIDUE ESTIMATION REPORT", st.session_state.residue_data, st.session_state.ai_result)

        st.download_button(
            label=f"📥 {t('Download Residue Report')}",
            data=pdf_bytes,
            file_name="residue_estimation_report.pdf",
            mime="application/pdf"
        )

    st.markdown("---")


    # ── Special Offer ─────────────────────────────────────────────────────────
    st.header(f"🌟 {t('Special Offer for Eco-Friendly Farmers!')}")
    
    col1, col2 = st.columns([2, 1])
    with col1:

        
        st.subheader(t("Buy Organic Compost & Biochar Products Now!"))
        st.write(f"""
    - {t('Premium quality organic compost for soil enrichment.')}
    - {t('Biochar improves soil water retention and fertility.')}
    - {t('Special **10% discount** this season!')}
        """)

        st.subheader(f"🌟 {t('Why choose organic residue products?')}")
        st.markdown(f"""
    - {t('Reduces dependence on chemical fertilizers.')}
    - {t('Improves long-term soil health and biodiversity.')}
    - {t('Supports government sustainability goals.')}
        """)

    if st.button(f"👉 {t('Visit Our Shop')}", key="soil_shop_btn"):
        st.session_state["nav_idx"] = 3
        st.rerun()

    with col2:
        st.image(
            "./image/residue.png",
            caption=t("Buy Organic Compost & Biochar Products Now!"),
            use_column_width=True
        )
    st.markdown("---")

    # ── Thank You ─────────────────────────────────────────────────────────────
    st.header(f"🍃 {t('Thank You for Using Residue Management!')}")

    st.write(f"""
{t('We are dedicated to helping farmers manage crop residue sustainably and profitably.')}

{t('If you have any questions or need assistance, feel free to reach out.')}
    """)

    st.success(f"🌱 {t('Happy Farming!')}")
