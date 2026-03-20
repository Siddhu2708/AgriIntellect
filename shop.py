import streamlit as st
import pandas as pd
import os
from utils import translate_text



def Shop(sarvam_client, language):
    def t_func(text):
        return translate_text(sarvam_client, text, language)

    # Language code mapping for user format
    lang_code = "en"
    if language == "Hindi": lang_code = "hi"
    elif language == "Marathi": lang_code = "mr"

    st.title(f"🏪 {t_func('Planty AI Shop')}")
    st.write(t_func("Expert-curated products for your Multiple Plants system, strictly following Planty AI's specialized recommendations."))

    tab1, tab2 = st.tabs([f"🛒 {t_func('Premium Products')}", f"🏪 {t_func('Nearby Shops')}"])

    with tab1:
        st.header(t_func("Planty Recommended Solutions"))
        st.info(t_func("These products are scientifically selected for maximum compatibility with the Multiple Plants varieties and soil conditions analyzed by Planty AI."))
        
        # Translation dictionary for the user format
        t = {
            'price': t_func('Price'),
            'usage': t_func('Usage')
        }

        # Local image directory
        img_dir = "image"

        general_solutions = [
            {
                'name': {'en': 'Planty Pro Tomato Micronutrient Mix', 'hi': 'प्लांटी प्रो टमाटर सूक्ष्म पोषक मिश्रण', 'mr': 'प्लँटी प्रो टोमॅटो सूक्ष्म पोषक मिश्रण'},
                'price': '₹920.00',
                'image': f'{img_dir}/Organic Fertilizer.jpg',
                'usage': {'en': 'Complete micronutrient complex for correcting tomato specific soil deficiencies.', 'hi': 'टमाटर विशिष्ट मिट्टी की कमियों को दूर करने के लिए पूर्ण सूक्ष्म पोषक तत्व।', 'mr': 'टोमॅटो विशिष्ट जमिनीतील कमतरता दूर करण्यासाठी पूर्ण सूक्ष्म पोषक तत्वे.'}
            },
            {
                'name': {'en': 'Planty Shield Bacterial Treatment', 'hi': 'प्लांटी शील्ड बैक्टीरियल उपचार', 'mr': 'प्लँटी शील्ड बॅक्टेरियल उपचार'},
                'price': '₹1588.17',
                'image': f'{img_dir}/Agri_mycin.jpg',
                'usage': {'en': 'Specialized formula for Planty AI-detected bacterial speck and spot.', 'hi': 'प्लांटी एआई द्वारा पता लगाए गए बैक्टीरियल स्पेक और स्पॉट के लिए विशेष फॉर्मूला।', 'mr': 'प्लँटी एआय द्वारे शोधलेल्या बॅक्टेरियल स्पेक आणि स्पॉटसाठी विशेष फॉर्म्युला.'}
            },
            {
                'name': {'en': 'Planty Ranman Late Blight Shield', 'hi': 'प्लांटी रैनमैन लेट ब्लाइट शील्ड', 'mr': 'प्लँटी रॅनमॅन लेट ब्लाइट शील्ड'},
                'price': '₹1743.00',
                'image': f'{img_dir}/Ranman.jpg',
                'usage': {'en': 'Preventative and curative fungicide for late blight detected by AI.', 'hi': 'एआई द्वारा पता लगाए गए लेट ब्लाइट के लिए निवारक और उपचारात्मक कवकनाशी।', 'mr': 'एआय द्वारे शोधलेल्या लेट ब्लाइटसाठी प्रतिबंधात्मक आणि उपचारात्मक बुरशीनाशक.'}
            },
            {
                'name': {'en': 'Planty Eco-Pest Neem Extract', 'hi': 'प्लांटी ईको-पेस्ट नीम एक्सट्रैक्ट', 'mr': 'प्लँटी इको-पेस्ट कडूिंबाचा अर्क'},
                'price': '₹1334.17',
                'image': f'{img_dir}/Neem Oil.jpg',
                'usage': {'en': 'Organic, high-concentration neem extract for sustainable pest management.', 'hi': 'स्थायी कीट प्रबंधन के लिए जैविक, उच्च सांद्रता वाला नीम का अर्क।', 'mr': 'शाश्वत कीड व्यवस्थापनासाठी सेंद्रिय, उच्च सांद्रता असलेला कडूिंबाचा अर्क.'}
            },
            {
                'name': {'en': 'Tomato Blossom-End Rot Corrector', 'hi': 'टमाटर ब्लॉसम-एंड रोट सुधारक', 'mr': 'टोमॅटो ब्लॉसम-एंड रोट सुधारक'},
                'price': '₹550.00',
                'image': f'{img_dir}/Organic Fertilizer.jpg',
                'usage': {'en': 'Calcium-rich supplement to prevent physiological disorders in tomatoes.', 'hi': 'टमाटर में शारीरिक विकारों को रोकने के लिए कैल्शियम युक्त पूरक।', 'mr': 'टोमॅटोमधील शारीरिक विकार टाळण्यासाठी कॅल्शियमयुक्त पूरक आहार.'}
            },
            {
                'name': {'en': 'Planty Mite Buster (Acaricide)', 'hi': 'प्लांटी माइट बस्टर (एकारीसाइट)', 'mr': 'प्लँटी माइट बस्टर (एकारीसाइड)'},
                'price': '₹1200.00',
                'image': f'{img_dir}/Acaricide.jpg',
                'usage': {'en': 'Targeted treatment for spider mites on tomato leaves.', 'hi': 'टमाटर के पत्तों पर मकड़ी के जाले के कीड़ों के लिए लक्षित उपचार।', 'mr': 'टोमॅटोच्या पानांवरील स्पायडर माइट्सवर लक्ष्यित उपचार.'}
            },
            {
                'name': {'en': 'Botrytis Grey Mold Shield', 'hi': 'बोट्राइटिस ग्रे मोल्ड शील्ड', 'mr': 'बोट्रिटिस ग्रे मोल्ड शिल्ड'},
                'price': '₹900.00',
                'image': f'{img_dir}/Botrytis.jpg',
                'usage': {'en': 'Effective control for tomato fruit and stem rot.', 'hi': 'टमाटर के फल और तना सड़न के लिए प्रभावी नियंत्रण।', 'mr': 'टोमॅटो फळ आणि देठ कुजण्यावर प्रभावी नियंत्रण.'}
            },
            {
                'name': {'en': 'Tomato Early Blight Protectant', 'hi': 'टमाटर अगेती झुलसा रक्षक', 'mr': 'टोमॅटो अर्ली ब्लाइट रक्षक'},
                'price': '₹750.00',
                'image': f'{img_dir}/Chlorothalonil.jpg',
                'usage': {'en': 'Preventative spray for early blight common in tomatoes.', 'hi': 'टमाटर में आम अगेती झुलसा के लिए निवारक स्प्रे।', 'mr': 'टोमॅटोमध्ये आढळणाऱ्या अर्ली ब्लाइटसाठी प्रतिबंधात्मक फवारणी.'}
            },
            {
                'name': {'en': 'Planty Bio-Bacterial Mix', 'hi': 'प्लांटी बायो-बैक्टीरियल मिश्रण', 'mr': 'प्लँटी बायो-बॅक्टेरियल मिश्रण'},
                'price': '₹400.00',
                'image': f'{img_dir}/Copper Fungicides.jpg',
                'usage': {'en': 'Organic copper-based solution for tomato bacterial diseases.', 'hi': 'टमाटर के जीवाणु रोगों के लिए जैविक तांबा आधारित समाधान।', 'mr': 'टोमॅटोच्या जिवाणू रोगांसाठी सेंद्रिय तांबे आधारित उपाय.'}
            },
            {
                'name': {'en': 'Organic Cow Dung Booster', 'hi': 'जैविक गाय का गोबर बूस्टर', 'mr': 'सेंद्रिय गाईचे शेण बूस्टर'},
                'price': '₹650.00',
                'image': f'{img_dir}/Cow Dung.jpg',
                'usage': {'en': 'Pure organic enrichment for tomato field soil structure.', 'hi': 'टमाटर के खेत की मिट्टी की संरचना के लिए शुद्ध जैविक संवर्धन।', 'mr': 'टोमॅटोच्या शेतातील मातीच्या रचनेसाठी शुद्ध सेंद्रिय समृद्धी.'}
            },
            {
                 'name': {'en': 'Planty Professional Ovicidal Agent', 'hi': 'प्लांटी प्रोफेशनल ओविसाइडल एजेंट', 'mr': 'प्लँटी प्रोफेशनल ओविसाइडल एजंट'},
                'price': '₹1250.00',
                'image': f'{img_dir}/Onager.jpg',
                'usage': {'en': 'Effective long-term mite egg control for tomato plants.', 'hi': 'टमाटर के पौधों के लिए प्रभावी दीर्घकालिक कीट अंडे नियंत्रण।', 'mr': 'टोमॅटोच्या रोपांसाठी प्रभावी दीर्घकालीन माइट अंडी नियंत्रण.'}
            },
            {
                'name': {'en': 'Planty Previcur Flex Root Guard', 'hi': 'प्लांटी प्रीविकुर फ्लेक्स रूट गार्ड', 'mr': 'प्लँटी प्रीविकुर फ्लेक्स रूट गार्ड'},
                'price': '₹820.00',
                'image': f'{img_dir}/Previcur Flex.jpg',
                'usage': {'en': 'Protection against tomato Pythium and Phytophthora root rots.', 'hi': 'टमाटर पीथियम और फाइटोफ्थोरा जड़ सड़न के खिलाफ सुरक्षा।', 'mr': 'टोमॅटो पीथियम आणि फायटोफथोरा मूळ कुजण्यापासून संरक्षण.'}
            }
        ]

        # Explicit layout as requested by user
        row1_col1, row1_col2, row1_col3 = st.columns ( 3 )
        row2_col1, row2_col2, row2_col3 = st.columns ( 3 )
        row3_col1, row3_col2, row3_col3 = st.columns ( 3 )
        row4_col1, row4_col2, row4_col3 = st.columns ( 3 )

        with row1_col1 :
            st.image ( general_solutions[0]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[0]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[0]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[0]['usage'][lang_code]}" )

        with row1_col2 :
            st.image ( general_solutions[1]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[1]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[1]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[1]['usage'][lang_code]}" )

        with row1_col3 :
            st.image ( general_solutions[2]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[2]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[2]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[2]['usage'][lang_code]}" )

        with row2_col1 :
            st.image ( general_solutions[3]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[3]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[3]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[3]['usage'][lang_code]}" )

        with row2_col2 :
            st.image ( general_solutions[4]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[4]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[4]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[4]['usage'][lang_code]}" )

        with row2_col3 :
            st.image ( general_solutions[5]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[5]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[5]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[5]['usage'][lang_code]}" )

        with row3_col1 :
            st.image ( general_solutions[6]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[6]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[6]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[6]['usage'][lang_code]}" )

        with row3_col2 :
            st.image ( general_solutions[7]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[7]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[7]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[7]['usage'][lang_code]}" )

        with row3_col3 :
            st.image ( general_solutions[8]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[8]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[8]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[8]['usage'][lang_code]}" )

        with row4_col1 :
            st.image ( general_solutions[9]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[9]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[9]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[9]['usage'][lang_code]}" )

        with row4_col2 :
            st.image ( general_solutions[10]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[10]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[10]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[10]['usage'][lang_code]}" )

        with row4_col3 :
            st.image ( general_solutions[11]['image'], use_column_width=True )
            st.write ( f"**{general_solutions[11]['name'][lang_code]}**" )
            st.write ( f"**{t['price']}:** {general_solutions[11]['price']}" )
            st.write ( f"**{t['usage']}:** {general_solutions[11]['usage'][lang_code]}" )


    with tab2:
        st.header(t_func("Find Agricultural Shops Near You"))
        working_dir = os.path.dirname(os.path.abspath(__file__))
        shop_path = os.path.join(working_dir, "shop.csv")
        
        if os.path.exists(shop_path):
            df_shop = pd.read_csv(shop_path)
            
            # Extract unique values for filters
            all_states = sorted(df_shop['state'].dropna().unique().tolist())
            all_districts = sorted(df_shop['district'].dropna().unique().tolist())
            all_products = sorted(list(set(
                p for sublist in df_shop['products_available'].dropna().str.split().tolist() for p in sublist
            )))

            # Get default state and district from sidebar location
            user_loc_str = st.session_state.get('user_location', '').lower()
            default_state = "All"
            default_dist = "All"
            for part in [p.strip() for p in user_loc_str.split(',')]:
                for s in all_states:
                    if part == s.lower():
                        default_state = s
                for d in all_districts:
                    if part == d.lower():
                        default_dist = d

            # Filter UI
            f1, f2, f3 = st.columns(3)
            with f1:
                s_state = st.selectbox(t_func("Select State"), ["All"] + all_states, index=(["All"] + all_states).index(default_state), key="shop_state_filter")
            with f2:
                s_dist = st.selectbox(t_func("Select District"), ["All"] + all_districts, index=(["All"] + all_districts).index(default_dist), key="shop_dist_filter")
            with f3:
                s_prod = st.selectbox(t_func("Select Product/Crop"), ["All"] + all_products, key="shop_prod_filter")

            # Apply Filtering
            filtered_df = df_shop.copy()
            if s_state != "All":
                filtered_df = filtered_df[filtered_df['state'] == s_state]
            if s_dist != "All":
                filtered_df = filtered_df[filtered_df['district'] == s_dist]
            if s_prod != "All":
                filtered_df = filtered_df[filtered_df['products_available'].str.contains(s_prod, case=False, na=False)]

            if filtered_df.empty:
                st.warning(t_func("No shops found matching these criteria."))
            else:
                st.success(t_func(f"Found {len(filtered_df)} shops matching your filters."))

            for _, shop in filtered_df.iterrows():
                with st.container(border=True):
                    sc1, sc2 = st.columns([1, 4])
                    with sc1:
                        stype = str(shop['shop_type']).lower()
                        if "pesticide" in stype: st.write("🧪")
                        elif "fertilizer" in stype: st.write("🌱")
                        elif "seed" in stype: st.write("🍅")
                        else: st.write("🏪")
                    with sc2:
                        st.markdown(f"### {shop['shop_name']}")
                        st.write(f"📍 **{t_func('Location')}:** {shop['district']}, {shop['state']}")
                        st.write(f"🛠️ **{t_func('Products')}:** {shop['products_available']}")
                        st.write(f"📞 **{t_func('Contact')}:** {shop['contact_number']}")
                        st.write(f"⭐ **{t_func('Rating')}:** {shop['rating']}/5")
        else:
            st.error(t_func("Shop database not found."))
