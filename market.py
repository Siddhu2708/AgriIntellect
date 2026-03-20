import streamlit as st
import pandas as pd
import os

from utils import translate_text

def market_home(sarvam_client, language):
    def t(text):
        return translate_text(sarvam_client, text, language)

    st.title(f"🛒 {t('Agricultural Market')}")
    st.write(t("Connect with buyers and sellers in your region."))

    working_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load all dataframes to get unique values for global filters
    df_buyer = pd.read_csv(os.path.join(working_dir, "buyer.csv")) if os.path.exists(os.path.join(working_dir, "buyer.csv")) else pd.DataFrame()
    df_seller = pd.read_csv(os.path.join(working_dir, "seller.csv")) if os.path.exists(os.path.join(working_dir, "seller.csv")) else pd.DataFrame()
    df_shop = pd.read_csv(os.path.join(working_dir, "shop.csv")) if os.path.exists(os.path.join(working_dir, "shop.csv")) else pd.DataFrame()
    df_subsidy = pd.read_csv(os.path.join(working_dir, "subsidy.csv")) if os.path.exists(os.path.join(working_dir, "subsidy.csv")) else pd.DataFrame()

    # Global Filters at the top
    st.markdown("---")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    all_states = sorted(list(set(
        (df_buyer['state'].dropna().unique().tolist() if not df_buyer.empty else []) +
        (df_seller['state'].dropna().unique().tolist() if not df_seller.empty else []) +
        (df_shop['state'].dropna().unique().tolist() if not df_shop.empty else []) +
        (df_subsidy['state'].dropna().unique().tolist() if not df_subsidy.empty else [])
    )))
    
    all_districts = sorted(list(set(
        (df_buyer['district'].dropna().unique().tolist() if not df_buyer.empty else []) +
        (df_seller['district'].dropna().unique().tolist() if not df_seller.empty else []) +
        (df_shop['district'].dropna().unique().tolist() if not df_shop.empty else []) +
        (df_subsidy['district'].dropna().unique().tolist() if not df_subsidy.empty else [])
    )))

    all_crops = sorted(list(set(
        (df_buyer['residue_required'].dropna().unique().tolist() if not df_buyer.empty else []) +
        (df_seller['crop'].dropna().unique().tolist() if not df_seller.empty else []) +
        (df_subsidy['crop_type'].dropna().unique().tolist() if not df_subsidy.empty else [])
    )))

    # Get default filters from session state string (e.g. "Pune, Maharashtra")
    user_loc_str = st.session_state.get('user_location', '').lower()
    user_loc_parts = [p.strip() for p in user_loc_str.split(',')]
    
    default_state = "All"
    default_dist = "All"
    
    for part in user_loc_parts:
        # Check if part matches any state
        for s in all_states:
            if part == s.lower():
                default_state = s
        # Check if part matches any district
        for d in all_districts:
            if part == d.lower():
                default_dist = d

    with f_col1:
        state_filter = st.selectbox(t("Select State"), ["All"] + all_states, index=(["All"] + all_states).index(default_state), key="global_state")
    with f_col2:
        dist_filter = st.selectbox(t("Select District"), ["All"] + all_districts, index=(["All"] + all_districts).index(default_dist), key="global_dist")
    with f_col3:
        crop_filter = st.selectbox(t("Select Crop"), ["All"] + all_crops, key="global_crop")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([f"🏢 {t('Buyers')}", f"🚜 {t('Sellers')}", f"💰 {t('Subsidies')}"])

    with tab1:
        st.header(t("Find Buyers for Your Crop Residue"))
        if not df_buyer.empty:
            filtered_df = df_buyer.copy()
            if state_filter != "All":
                filtered_df = filtered_df[filtered_df['state'] == state_filter]
            if dist_filter != "All":
                filtered_df = filtered_df[filtered_df['district'] == dist_filter]
            if crop_filter != "All":
                filtered_df = filtered_df[filtered_df['residue_required'].str.contains(crop_filter, case=False, na=False)]
            
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.error(t("Buyer data not found."))

    with tab2:
        st.header(t("Find Sellers of Crop and Residue"))
        if not df_seller.empty:
            s_filtered_df = df_seller.copy()
            if state_filter != "All":
                s_filtered_df = s_filtered_df[s_filtered_df['state'] == state_filter]
            if dist_filter != "All":
                s_filtered_df = s_filtered_df[s_filtered_df['district'] == dist_filter]
            if crop_filter != "All":
                s_filtered_df = s_filtered_df[s_filtered_df['crop'].str.contains(crop_filter, case=False, na=False)]

            st.dataframe(s_filtered_df, use_container_width=True)
        else:
            st.error(t("Seller data not found."))

    with tab3:
        st.header(t("Available Government Subsidies"))
        if not df_subsidy.empty:
            sub_filtered_df = df_subsidy.copy()
            if state_filter != "All":
                sub_filtered_df = sub_filtered_df[sub_filtered_df['state'] == state_filter]
            if dist_filter != "All":
                sub_filtered_df = sub_filtered_df[sub_filtered_df['district'] == dist_filter]
            if crop_filter != "All":
                sub_filtered_df = sub_filtered_df[sub_filtered_df['crop_type'].str.contains(crop_filter, case=False, na=False) | (sub_filtered_df['crop_type'] == "All Crops")]

            st.dataframe(sub_filtered_df, use_container_width=True)
        else:
            st.error(t("Subsidy data not found."))
