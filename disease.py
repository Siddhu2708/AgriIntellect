import streamlit as st
from PIL import Image
import json
import os
import base64
import io
import numpy as np
import tensorflow as tf
from groq import Groq
import pdf_generator
from utils import translate_text, load_config

# Tomato disease classes (PlantVillage order — must match model output indices)
TOMATO_CLASSES = [
    "Bacterial Spot",
    "Early Blight",
    "Late Blight",
    "Leaf Mold",
    "Septoria Leaf Spot",
    "Spider Mites (Two-spotted spider mite)",
    "Target Spot",
    "Tomato Yellow Leaf Curl Virus",
    "Tomato Mosaic Virus",
    "Healthy"
]

# Confidence threshold — lowered to avoid false negatives for valid leaves
CONFIDENCE_THRESHOLD = 0.30


@st.cache_resource
def load_tomato_model():
    """Load the H5 model once and cache it for the lifetime of the app."""
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tomato_disease_model.h5")
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        return None


def predict_tomato_disease(uploaded_file):
    """
    Run the tomato model on the uploaded image.
    Returns (class_name, confidence) or (None, 0.0) if rejected.
    """
    try:
        model = load_tomato_model()
        if model is None:
            return None, 0.0

        # Read image and preprocess
        image = Image.open(io.BytesIO(uploaded_file.getvalue())).convert("RGB")
        image = image.resize((128, 128))
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 128, 128, 3)

        predictions = model.predict(img_array, verbose=0)
        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_idx])

        if confidence < CONFIDENCE_THRESHOLD:
            return None, confidence  # wrong or unrecognized image

        return TOMATO_CLASSES[predicted_idx], confidence

    except Exception as e:
        return None, 0.0


def call_groq_disease_analysis(crop_name: str, language: str = "English", detected_disease: str = None, image_b64 = None) -> str:
    try:
        config = load_config()
        groq_api_key = config.get("GROQ_API_KEY", "")
        client = Groq(api_key=groq_api_key)

        lang_instruction = (
            f"IMPORTANT: Write your ENTIRE response in {language} language.\n"
            "Do NOT change the format or structure — only the language of the content changes.\n\n"
            if language != "English" else ""
        )

        # If model detected a specific disease, use it; otherwise describe generically
        if detected_disease:
            disease_context = (
                f"The AI model has already detected '{detected_disease}' on this {crop_name} leaf.\n"
                f"Provide detailed information specifically about '{detected_disease}'.\n"
            )
        else:
            disease_context = (
                f"The farmer has uploaded an image of a {crop_name} leaf that appears diseased.\n"
                "Analyze the image and identify the most likely disease.\n"
            )

        prompt_text = (
            f"{lang_instruction}"
            "You are an agriculture assistant.\n\n"
            f"{disease_context}"
            "Convert the disease analysis into a clean, structured, farmer-friendly format.\n\n"
            "Follow STRICT formatting rules:\n"
            "1. Show main headings in bold using **heading** syntax.\n"
            "2. Keep explanation short — 2-3 lines only.\n"
            "3. Use numbered lists where required. Provide multiple detailed points (not just one or two) for each list to ensure the farmer has all necessary information.\n"
            "4. Format lists as: 1. Name: Short info\n"
            "5. Do NOT write long paragraphs.\n"
            "6. Keep output simple, clean, and structured.\n"
            "7. Do NOT use symbols like *, - except bold headings.\n\n"
            "Output format exactly like this template:\n\n"
            "**Detected Disease:** <value>\n\n"
            "**Affected Crop:** <value>\n\n"
            "**Disease Severity:** <Low / Medium / High>\n\n"
            "**Disease Information:**\n"
            "<short explanation, 2-3 lines>\n\n"
            "**Treatment Recommendations:**\n"
            "1. Step: Info\n\n"
            "2. Step: Info\n\n"
            "3. Step: Info\n\n"
            "4. Step: Info\n\n"
            "**Pesticide Recommendations:**\n"
            "1. Pesticide Name: Usage\n\n"
            "2. Pesticide Name: Usage\n\n"
            "3. Pesticide Name: Usage\n\n"
            "**Fertilizer Suggestions:**\n"
            "1. Fertilizer Name: Purpose\n\n"
            "2. Fertilizer Name: Purpose\n\n"
            "3. Fertilizer Name: Purpose\n\n"
            "**Solution Process:**\n"
            "1. Step: What farmer should do\n\n"
            "2. Step: What farmer should do\n\n"
            "3. Step: What farmer should do\n\n"
            "4. Step: What farmer should do\n\n"
            "5. Step: What farmer should do\n\n"
            "**Preventive Measures:**\n"
            "1. Step: Info\n\n"
            "2. Step: Info\n\n"
            "3. Step: Info\n\n"
            "4. Step: Info\n\n"
            "5. Step: Info\n\n"
            f"Now format the disease data for crop: {crop_name}"
            + (f", detected disease: {detected_disease}" if detected_disease else "")
        )

        content = [{"type": "text", "text": prompt_text}]
        if image_b64:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
            })

        messages = [
            {
                "role": "user",
                "content": content
            }
        ]

        # Use vision model for all analysis to get better results
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=1000,
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"AI analysis unavailable: {str(e)}\n\nPlease check your GROQ_API_KEY in config.json."

def validate_image_is_leaf(image_b64) -> bool:
    """
    Use Groq Vision to check if the uploaded image is actually a plant leaf.
    """
    try:
        config = load_config()
        groq_api_key = config.get("GROQ_API_KEY", "")
        client = Groq(api_key=groq_api_key)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Is this image a plant leaf? Respond with ONLY 'YES' or 'NO'."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        answer = response.choices[0].message.content.strip().upper()
        return "YES" in answer
    except Exception:
        # Fallback to True if API fails so we don't block the user
        return True


def disease_home(sarvam_client, language):

    def t(text):
        return translate_text(sarvam_client, text, language)

    # ── Welcome ───────────────────────────────────────────────────────────────
    st.title(f"🩺 {t('Welcome to Disease Detection System!')}")

    st.write(t("Your intelligent assistant for identifying and treating plant diseases."))
    st.write(t("Use the Disease Detection module to:"))

    st.markdown(f"""
- {t('Upload a plant leaf image for instant AI diagnosis.')}
- {t('Identify the exact disease affecting your crop.')}
- {t('Get expert treatment and pesticide recommendations.')}
- {t('Prevent disease spread and protect your harvest.')}
    """)

    st.markdown("---")

    # ── Crop Selection ────────────────────────────────────────────────────────
    st.header(f"🌾 {t('Select Your Crop')}")

    crops = [
        "Tomato", "Potato", "Cotton", "Wheat", "Rice", "Maize",
        "Sugarcane", "Chili", "Apple", "Banana", "Grape", "Soybean", "Other"
    ]

    selected_option = st.selectbox(
        t("Choose the crop you want to diagnose:"),
        [t(crop) for crop in crops]
    )

    # Always track the original English crop name for model branching
    try:
        original_crop_idx = [t(crop) for crop in crops].index(selected_option)
        original_crop = crops[original_crop_idx]
    except (ValueError, IndexError):
        original_crop = "Other"

    if original_crop == "Other":
        selected_crop = st.text_input(t("Enter the name of your crop:"))
        if not selected_crop:
            selected_crop = t("your plant")
    else:
        selected_crop = selected_option  # translated display name (for UI text)

    st.markdown("---")

    # ── Main Feature: Image Upload & Diagnosis ────────────────────────────────
    st.header(f"🔍 {t('Plant Leaf Disease Diagnosis')}")


    st.write(f"📤 **{t('Upload an image of the leaf for')} {selected_crop}**")

    uploaded_file = st.file_uploader(
        t("Upload Leaf Image"),
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.warning(f"{t('Please upload a valid image of a')} {selected_crop} {t('leaf for diagnosis.')}")
    else:
        file_bytes = uploaded_file.getvalue()
        image_b64 = base64.b64encode(file_bytes).decode('utf-8')

        st.image(uploaded_file, caption=t("Uploaded Leaf Image"), width=400)

        # ── Step 1: Validate if it's a leaf (All Crops) ───────────────────────
        with st.spinner(t("Checking image validity...")):
            is_valid_plant = validate_image_is_leaf(image_b64)

        if not is_valid_plant:
            st.error(
                f"❌ {t('This does not look like a plant leaf.')}\n\n"
                f"{t('Please upload a clear, close-up photo of the leaf for diagnosis.')}"
            )
        else:
            # ── Step 2: Diagnosis ─────────────────────────────────────────────

            # ── TOMATO: Use the H5 model ──────────────────────────────────────
            if original_crop == "Tomato":
                with st.spinner(t("Running Tomato AI Model... please wait")):
                    detected_disease, confidence = predict_tomato_disease(uploaded_file)

                if detected_disease is None:
                    # Confidence below threshold for specific disease classes
                    st.warning(
                        f"⚠️ {t('Tomato leaf detected, but specific disease is unclear.')}\n\n"
                        f"{t('Falling back to AI vision analysis...')}"
                    )
                    with st.spinner(t("Consulting AI Vision Expert...")):
                        ai_diagnosis = call_groq_disease_analysis(
                            "Tomato", language, image_b64=image_b64
                        )
                else:
                    # Show model result
                    st.success(f"✅ {t('Tomato model detected:')} **{detected_disease}** "
                               f"({t('Confidence')}: {confidence*100:.1f}%)")

                    with st.spinner(t("Generating detailed AI analysis... please wait")):
                        ai_diagnosis = call_groq_disease_analysis(
                            "Tomato", language, detected_disease=detected_disease, image_b64=image_b64
                        )

                st.subheader(f"🦠 {t('AI Diagnosis Report')}")
                st.write(ai_diagnosis)

                # Save Data
                plant_data = {
                    "crop_type": "Tomato",
                    "detected_disease": detected_disease or "Uncertain",
                    "confidence": round(confidence, 4),
                    "ai_analysis": ai_diagnosis,
                    "image_base64": image_b64
                }
                working_dir = os.path.dirname(os.path.abspath(__file__))
                try:
                    with open(os.path.join(working_dir, "plant.json"), "w") as f:
                        json.dump(plant_data, f, indent=4)
                except Exception:
                    pass

                pdf_bytes = pdf_generator.generate_pdf_bytes(
                    "TOMATO LEAF DISEASE DIAGNOSIS",
                    {"Crop Type": "Tomato", "Detected Disease": detected_disease or "AI Vision Diagnosis"},
                    ai_diagnosis
                )
                st.download_button(
                    label=f"📥 {t('Download Diagnosis Report')}",
                    data=pdf_bytes,
                    file_name="tomato_diagnosis_report.pdf",
                    mime="application/pdf"
                )

                # 📍 Find Nearby Pesticide Shops
                user_loc = st.session_state.get('user_location', '')
                search_query = f"pesticide and fertilizer shop near {user_loc}" if user_loc else "pesticide and fertilizer shop near me"
                maps_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
                
                st.link_button(
                    f"📍 {t('Find Nearby Pesticide & Fertilizer Shops')}",
                    maps_url,
                    use_container_width=True
                )

            # ── OTHER CROPS: Use Groq Vision ──────────────────────────────────
            else:
                st.success(t("Leaf image verified! Generating AI diagnosis..."))

                with st.spinner(t("Analyzing image with AI Vision... please wait")):
                    ai_diagnosis = call_groq_disease_analysis(original_crop, language, image_b64=image_b64)

                st.subheader(f"🦠 {t('AI Diagnosis Report')}")
                st.write(ai_diagnosis)

                plant_data = {
                    "crop_type": original_crop,
                    "ai_analysis": ai_diagnosis,
                    "image_base64": image_b64
                }
                working_dir = os.path.dirname(os.path.abspath(__file__))
                try:
                    with open(os.path.join(working_dir, "plant.json"), "w") as f:
                        json.dump(plant_data, f, indent=4)
                except Exception:
                    pass

                pdf_bytes = pdf_generator.generate_pdf_bytes(
                    "PLANT LEAF DISEASE DIAGNOSIS",
                    {"Crop Type": original_crop},
                    ai_diagnosis
                )
                st.download_button(
                    label=f"📥 {t('Download Diagnosis Report')}",
                    data=pdf_bytes,
                    file_name="plant_diagnosis_report.pdf",
                    mime="application/pdf"
                )

                # 📍 Find Nearby Pesticide Shops
                user_loc = st.session_state.get('user_location', '')
                search_query = f"pesticide and fertilizer shop near {user_loc}" if user_loc else "pesticide and fertilizer shop near me"
                maps_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
                
                st.link_button(
                    f"📍 {t('Find Nearby Pesticide & Fertilizer Shops')}",
                    maps_url,
                    use_container_width=True
                )

    st.markdown("---")

    # ── Special Offer ─────────────────────────────────────────────────────────
    st.subheader(t("🌟 Special Offer for Farmers!"))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"🌾 **{t('Buy premium, disease-resistant')} {selected_crop} {t('seeds with a 20% discount!')}**")
        st.write(t("Buy **Premium Quality Plant Seeds** for a wide variety of crops and vegetables."))
        st.write(t("Limited Time Offer: **Up to 20% discount on selected seeds!**"))

        st.markdown(f"""
        ### 🌟 {t('Why Choose Our Seeds?')}
        - {t('Tested and trusted by farmers')}
        - {t('High germination rate')}
        - {t('Disease-resistant varieties')}
        - {t('Suitable for different soil conditions')}
        """)
        if st.button(f"👉 {t('Visit Our Shop')}", key="disease_shop_btn"):
            st.session_state["nav_idx"] = 3
            st.rerun()

    with col2:
        st.image(
            "./image/plant.png",
            caption=t("Fresh produce – protect your crops with early disease detection"),
            use_column_width=True
        )
    st.markdown("---")

    # ── Thank You ─────────────────────────────────────────────────────────────
    st.header(f"🍃 {t('Thank You for Using Disease Detection!')}")

    st.write(f"""
{t('We are dedicated to helping farmers and gardeners maintain healthy crops.')}

{t('If you have any questions or need assistance, feel free to reach out.')}
    """)

    st.success(f"🌱 {t('Happy Farming!')}")
