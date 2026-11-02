"""
AquaSafe AI - Intelligent Drinking Water Potability Classifier & Emergency Advisory Engine
AICTE - IBM SkillsBuild Machine Learning & Applied AI Internship Capstone Project
Theme: UN Sustainable Development Goal 6 (Clean Water and Sanitation) & SDG 3 (Good Health)
Author: Mayank
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="AquaSafe AI | Drinking Water Safety Engine",
    page_icon="🚰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean CSS Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0284c7;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-safe {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load ML Pipeline & Resources
# ---------------------------------------------------------
@st.cache_resource
def load_pipeline():
    model_path = os.path.join(os.path.dirname(__file__), "models", "aquasafe_pipeline.pkl")
    if not os.path.exists(model_path):
        from train_model import train_aquasafe_model
        train_aquasafe_model()
    return joblib.load(model_path)

pipeline = load_pipeline()
model = pipeline['model']
imputer = pipeline['imputer']
scaler = pipeline['scaler']
feature_names = pipeline['feature_names']
accuracy = pipeline.get('accuracy', 0.892)

# Configured screening reference limits; not a complete drinking-water standard
WHO_STANDARDS = {
    'ph': {
        'name': 'pH Level',
        'min': 6.5,
        'max': 8.5,
        'unit': 'pH Units',
        'hazard': 'Corrosive or scale-forming water; acidic water leaches toxic heavy metals.',
        'remedy': 'Lime or sodium carbonate dosing for low pH; food-grade acid injection for alkaline water.'
    },
    'Hardness': {
        'name': 'Total Hardness (CaCO3)',
        'min': 0,
        'max': 300.0,
        'unit': 'mg/L',
        'hazard': 'Excessive mineral scaling in supply pipes; gastrointestinal irritation.',
        'remedy': 'Ion-exchange resin water softening or soda ash precipitation.'
    },
    'Solids': {
        'name': 'Total Dissolved Solids (TDS)',
        'min': 0,
        'max': 2000.0,
        'acceptable_max': 500.0,
        'unit': 'mg/L',
        'hazard': 'High salinity, unpalatable mineral taste, and potential toxic ion concentration.',
        'remedy': 'Multi-stage Reverse Osmosis (RO) filtration or electrodialysis.'
    },
    'Chloramines': {
        'name': 'Chloramines',
        'min': 0,
        'max': 8.0,
        'unit': 'ppm',
        'hazard': 'Skin/eye irritation, chloramine degradation into toxic byproducts.',
        'remedy': 'Granular activated carbon (GAC) filtration or ascorbic acid dechlorination.'
    },
    'Sulfate': {
        'name': 'Sulfate (SO4)',
        'min': 0,
        'max': 350.0,
        'unit': 'mg/L',
        'hazard': 'Cathartic laxative effects and dehydration in vulnerable populations.',
        'remedy': 'Reverse osmosis or anion exchange demineralization.'
    },
    'Conductivity': {
        'name': 'Electrical Conductivity',
        'min': 0,
        'max': 800.0,
        'unit': 'μS/cm',
        'hazard': 'Indicates dissolved ion influx from sewage or agricultural runoff.',
        'remedy': 'Electrodialysis or deionization filtration.'
    },
    'Organic_carbon': {
        'name': 'Total Organic Carbon (TOC)',
        'min': 0,
        'max': 20.0,
        'unit': 'ppm',
        'hazard': 'Promotes microbial biofilm growth and reacts with chlorine to form carcinogens.',
        'remedy': 'Ozonation, coagulation-flocculation, and biological activated carbon (BAC).'
    },
    'Trihalomethanes': {
        'name': 'Trihalomethanes (THMs)',
        'min': 0,
        'max': 80.0,
        'unit': 'μg/L',
        'hazard': 'Carcinogenic disinfection byproduct linked to bladder and colorectal cancers.',
        'remedy': 'Activated carbon adsorption and stripping aeration prior to distribution.'
    },
    'Turbidity': {
        'name': 'Turbidity',
        'min': 0,
        'max': 5.0,
        'unit': 'NTU',
        'hazard': 'Cloudiness shields pathogenic bacteria and viruses from chlorine disinfection.',
        'remedy': 'Alum/poly-aluminium chloride coagulation followed by rapid sand filtration.'
    }
}

# ---------------------------------------------------------
# Header & KPI Metrics Bar
# ---------------------------------------------------------
st.markdown('<div class="main-title">🚰 AquaSafe AI — Water Potability & Emergency Advisory Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title"><strong>AICTE – IBM SkillsBuild Machine Learning & Applied AI Internship Capstone</strong> | UN SDG 6: Clean Water & Sanitation & SDG 3: Good Health</div>', unsafe_allow_html=True)

st.info("AquaSafe AI is an educational screening prototype. It does not certify drinking water, perform physical or microbiological tests, or issue official municipal instructions. Confirm results with an accredited laboratory. The ML benchmark dataset may not represent local Indian water samples; validate it with genuine local labelled data before relying on predictions.")

# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="🎯 Dataset Holdout Score", value=f"{accuracy * 100:.1f}%", delta="Not real-world validation")
with kpi2:
    st.metric(label="🧪 Monitored Parameters", value="9 Parameters", delta="Chemical / physicochemical screening")
with kpi3:
    st.metric(label="📋 Reference Basis", value="Configured Limits", delta="Screening reference only")
with kpi4:
    st.metric(label="📝 Advisory", value="Suggested Actions", delta="Not an official directive")

st.markdown("---")

# ---------------------------------------------------------
# Multi-Tab Main Interface
# ---------------------------------------------------------
tab_single, tab_batch, tab_analytics, tab_guidelines = st.tabs([
    "🚰 Live Water Potability Test",
    "📁 Batch Laboratory CSV Inspection",
    "📊 ML Model & Feature Importance",
    "📋 Parameter Reference Guide"
])

# =========================================================
# TAB 1: Single Sample Testing & Remediation
# =========================================================
with tab_single:
    st.markdown("### 🔬 Live Water Quality Screening")
    st.caption("Enter laboratory readings or use demo presets. This prototype screens 9 chemical / physicochemical parameters; it does not test microorganisms.")

    # Slider values are initialized once, before any keyed widgets are created.
    defaults = {
        "ph": 7.4,
        "Hardness": 195.0,
        "Solids": 350.0,
        "Chloramines": 6.4,
        "Sulfate": 310.0,
        "Conductivity": 430.0,
        "Organic_carbon": 14.0,
        "Trihalomethanes": 66.0,
        "Turbidity": 3.8
    }

    presets = {
        "municipal": {
            "ph": 7.4, "Hardness": 195.0, "Solids": 350.0,
            "Chloramines": 6.4, "Sulfate": 310.0, "Conductivity": 430.0,
            "Organic_carbon": 14.0, "Trihalomethanes": 66.0, "Turbidity": 3.8
        },
        "well": {
            "ph": 8.3, "Hardness": 285.0, "Solids": 900.0,
            "Chloramines": 7.5, "Sulfate": 340.0, "Conductivity": 710.0,
            "Organic_carbon": 18.0, "Trihalomethanes": 75.0, "Turbidity": 4.6
        },
        "industrial": {
            "ph": 5.2, "Hardness": 380.0, "Solids": 4000.0,
            "Chloramines": 11.5, "Sulfate": 450.0, "Conductivity": 950.0,
            "Organic_carbon": 26.0, "Trihalomethanes": 115.0, "Turbidity": 7.8
        }
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
        number_key = f"{key}_number"
        if number_key not in st.session_state:
            st.session_state[number_key] = value

    # Widget callbacks run before rerendering, so both controls stay in sync.
    def sync_number_to_slider(key):
        st.session_state[key] = st.session_state[f"{key}_number"]

    def sync_slider_to_number(key):
        st.session_state[f"{key}_number"] = st.session_state[key]

    # Streamlit runs this callback before rerunning the script and rendering widgets.
    def apply_preset(preset_name):
        for key, value in presets[preset_name].items():
            st.session_state[key] = value
            st.session_state[f"{key}_number"] = value

    # Preset buttons
    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        st.button(
            "🟢 Load Safe Municipal Tap Water",
            on_click=apply_preset,
            args=("municipal",),
            key="preset_municipal",
            use_container_width=True
        )

    with col_p2:
        st.button(
            "🟡 Load Hard Mineral Well Water",
            on_click=apply_preset,
            args=("well",),
            key="preset_well",
            use_container_width=True
        )

    with col_p3:
        st.button(
            "🔴 Load Industrial Contaminated Water",
            on_click=apply_preset,
            args=("industrial",),
            key="preset_industrial",
            use_container_width=True
        )

    # One slider and one precise numeric input per parameter in the sidebar.
    st.sidebar.markdown("### ⚙️ Adjust Chemical Metrics")
    slider_specs = [
        ("ph", "1. pH Level (0 - 14)", 0.0, 14.0, 0.1),
        ("Hardness", "2. Hardness (mg/L)", 20.0, 450.0, 5.0),
        ("Solids", "3. Total Dissolved Solids - TDS (mg/L)", 0.0, 10000.0, 10.0),
        ("Chloramines", "4. Chloramines (ppm)", 0.0, 15.0, 0.1),
        ("Sulfate", "5. Sulfate (mg/L)", 20.0, 600.0, 5.0),
        ("Conductivity", "6. Conductivity (μS/cm)", 50.0, 1200.0, 10.0),
        ("Organic_carbon", "7. Organic Carbon (ppm)", 0.5, 30.0, 0.1),
        ("Trihalomethanes", "8. Trihalomethanes (μg/L)", 0.0, 160.0, 1.0),
        ("Turbidity", "9. Turbidity (NTU)", 0.1, 10.0, 0.1)
    ]

    curr_inputs = {}
    for key, label, min_value, max_value, slider_step in slider_specs:
        slider_col, number_col = st.sidebar.columns([3, 1])
        with slider_col:
            curr_inputs[key] = st.slider(
                label,
                min_value,
                max_value,
                step=slider_step,
                key=key,
                on_change=sync_slider_to_number,
                args=(key,)
            )
        with number_col:
            st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                step=0.01,
                format="%.2f",
                key=f"{key}_number",
                on_change=sync_number_to_slider,
                args=(key,),
                label_visibility="collapsed"
            )

    # Model Evaluation
    raw_vector = np.array([[curr_inputs[f] for f in feature_names]])
    scaled_vector = scaler.transform(raw_vector)
    prediction = model.predict(scaled_vector)[0]
    probabilities = model.predict_proba(scaled_vector)[0]
    potable_prob = probabilities[1]

    # Chemical / physicochemical screening against configured references
    violations = []
    compliance_rows = []
    for f in feature_names:
        val = curr_inputs[f]
        info = WHO_STANDARDS[f]
        min_v, max_v = info['min'], info['max']
        is_breach = (val < min_v or val > max_v)
        
        status_str = ("✅ Acceptable" if val <= info["acceptable_max"] else ("⚠️ Conditional permissible" if val <= max_v else "❌ Above permissible")) if f == "Solids" else ("⚠️ Outside reference" if is_breach else "Within reference")
        if is_breach:
            violations.append((f, val, min_v, max_v, info['hazard'], info['remedy']))

        compliance_rows.append({
            "Parameter": info['name'],
            "Observed Level": f"{val:.1f} {info['unit']}",
            "Configured Reference": (f"Acceptable ≤ {info['acceptable_max']} mg/L; conditional permissible ≤ {max_v} mg/L" if f == "Solids" else f"{min_v} - {max_v} {info['unit']}"),
            "Compliance Status": status_str
        })

    st.markdown("<br>", unsafe_allow_html=True)
    col_result, col_table = st.columns([1, 1.25])

    with col_result:
        st.subheader("🎯 Potability Classification")
        if prediction == 1 and len(violations) == 0:
            st.success(f"""
            ### ✅ WITHIN CONFIGURED LIMITS
            **AI Model Confidence: {potable_prob * 100:.1f}%**
            
            The entered chemical parameters are within the configured screening limits. Microbiological testing is recommended for a more complete assessment.
            """)
            st.progress(float(potable_prob))
        else:
            alert_lines = ["### ⚠️ WATER QUALITY ALERT — REVIEW REQUIRED"]
            if violations:
                affected_parameters = ", ".join(
                    f"{WHO_STANDARDS[v[0]]['name']} ({v[1]:.1f} {WHO_STANDARDS[v[0]]['unit']})"
                    for v in violations
                )
                alert_lines.append(
                    f"**Configured reference limits exceeded:** {affected_parameters}. "
                    "Review these readings with a qualified water-quality professional."
                )
            if prediction == 0:
                if violations:
                    alert_lines.append(
                        "**ML model prediction:** The model classified this sample as non-potable. "
                        "This is a model prediction, not a confirmed contamination finding."
                    )
                else:
                    alert_lines.append(
                        "**ML model prediction:** The model classified this sample as non-potable, "
                        "although none of the configured reference limits were exceeded. "
                        "This is a model prediction, not a confirmed contamination finding."
                    )
            st.error("\n\n".join(alert_lines))

        # Metric summary chips
        st.markdown(f"""
        - **Random Forest Vote:** `{'Safe (Class 1)' if prediction == 1 else 'Unsafe (Class 0)'}`
        - **Configured Reference Flags:** `{len(violations)} of 9 parameters exceed configured limits`
        - **Follow-up:** `{'Qualified review recommended' if len(violations) > 0 or prediction == 0 else 'Routine quality review'}`
        """)

    with col_table:
        st.subheader("📋 9-Parameter Screening Check")
        df_comp = pd.DataFrame(compliance_rows)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

    # Suggested treatment advisory
    st.markdown("---")
    st.subheader("📝 Suggested Treatment Advisory")
    
    if len(violations) > 0 or prediction == 0:
        st.warning("⚠️ **Suggested follow-up based on entered readings:**")
        
        advisory_body = f"""================================================================================
AQUASAFE AI — WATER QUALITY SCREENING FOLLOW-UP & SUGGESTED ACTIONS
AICTE - IBM SkillsBuild AI Capstone | Reference: UN SDG 6.1 (Universal Safe Water)
================================================================================

[1] EXECUTIVE ASSESSMENT:
    ML Model Prediction   : {"Non-potable (model prediction; not a confirmed contamination finding)" if prediction == 0 else "Potable (model prediction)"}
    Reference Limit Flags : {len(violations)} parameter(s) outside configured screening limits
    Follow-up             : Qualified review recommended

[2] CHEMICAL BREACH BREAKDOWN:
"""
        if not violations:
            advisory_body += "    No configured reference limits were exceeded.\n"
        for v in violations:
            advisory_body += f"    • {WHO_STANDARDS[v[0]]['name']}: {v[1]:.1f} {WHO_STANDARDS[v[0]]['unit']} (Configured reference: {v[2]} - {v[3]})\n"
            advisory_body += f"      - Toxicological Hazard: {v[4]}\n"
            advisory_body += f"      - Required Treatment  : {v[5]}\n\n"

        advisory_body += """[3] SUGGESTED WATER-TREATMENT ACTIONS:
    1. Review the laboratory report with a qualified water-quality professional.
    2. Possible treatment options (confirm suitability before use):
       - If Turbidity > 5 NTU: Initiate alum coagulation and rapid sand filtration.
       - If TDS exceeds 2000 mg/L: Seek qualified advice on suitable desalination / treatment options.
       - If Chloramines / THMs elevated: Deploy Granular Activated Carbon (GAC) filtration.
       - If pH outside 6.5 - 8.5: Apply soda ash dosing (low pH) or neutralizing aeration.
    3. Re-test the sample in an accredited laboratory after any treatment.

================================================================================
Generated by AquaSafe AI from user-entered readings and configured screening references. Not a water-safety certificate.
================================================================================
"""
        st.code(advisory_body, language="text")
        st.download_button(
            label="📥 Download AI-Generated Advisory Report (.txt)",
            data=advisory_body,
            file_name="AquaSafe_Emergency_Remediation_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.success("✅ **Within Configured Limits:** The monitored chemical parameters are within this prototype’s screening references. Microbiological testing and complete laboratory assessment are still required.")


# =========================================================
# TAB 2: Batch CSV Laboratory Inspection
# =========================================================
with tab_batch:
    st.markdown("### 📁 Batch Laboratory CSV Upload & High-Throughput Screening")
    st.caption("Municipal water testing labs analyze hundreds of water samples simultaneously. Upload a CSV of chemical lab records to perform automated bulk potability classification.")

    demo_csv_path = os.path.join(os.path.dirname(__file__), "dataset", "demo_water_samples.csv")

    col_u1, col_u2 = st.columns([2, 1])
    with col_u1:
        uploaded_file = st.file_uploader("Upload Water Quality CSV Report", type=["csv"])
    with col_u2:
        st.write("")
        st.write("")
        use_demo_data = st.button("📥 Load Pre-Packaged Demo Batch (50 Water Samples)", use_container_width=True)

    df_batch = None
    if uploaded_file is not None:
        try:
            df_batch = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded `{uploaded_file.name}` with {df_batch.shape[0]} samples.")
        except Exception as e:
            st.error(f"Error reading uploaded CSV: {e}")
    elif use_demo_data or os.path.exists(demo_csv_path):
        df_batch = pd.read_csv(demo_csv_path)

    if df_batch is not None:
        # Check required columns
        missing_cols = [c for c in feature_names if c not in df_batch.columns]
        if missing_cols:
            st.error(f"CSV is missing required chemical columns: {missing_cols}")
        else:
            # Run bulk inference
            X_batch = df_batch[feature_names].values
            X_batch_imp = imputer.transform(X_batch)
            X_batch_scaled = scaler.transform(X_batch_imp)
            
            batch_preds = model.predict(X_batch_scaled)
            batch_probs = model.predict_proba(X_batch_scaled)[:, 1]

            # Results DataFrame
            results_df = df_batch.copy()
            results_df['AI_Potability_Verdict'] = np.where(batch_preds == 1, 'Safe (Potable)', 'Hazardous (Non-Potable)')
            results_df['Safety_Confidence_%'] = np.round(batch_probs * 100, 1)

            # Count violations per row
            def count_violations(row):
                cnt = 0
                for f in feature_names:
                    val = row[f]
                    if pd.notna(val):
                        if val < WHO_STANDARDS[f]['min'] or val > WHO_STANDARDS[f]['max']:
                            cnt += 1
                return cnt

            results_df['Reference_Limit_Flags'] = results_df.apply(count_violations, axis=1)

            # Display Bulk Metrics
            total_samples = len(results_df)
            potable_count = int(np.sum(batch_preds == 1))
            unsafe_count = total_samples - potable_count
            potable_pct = (potable_count / total_samples) * 100

            st.markdown("#### 📈 Batch Screening Summary")
            bm1, bm2, bm3, bm4 = st.columns(4)
            with bm1:
                st.metric("Total Samples Tested", total_samples)
            with bm2:
                st.metric("Safe / Potable Samples", f"{potable_count} ({potable_pct:.1f}%)")
            with bm3:
                st.metric("Unsafe / Contaminated", f"{unsafe_count} ({100 - potable_pct:.1f}%)")
            with bm4:
                st.metric("Samples with Reference Flags", int((results_df['Reference_Limit_Flags'] > 0).sum()))

            # Visual Distribution Chart
            summary_chart_df = pd.DataFrame({
                'Water Quality Verdict': ['Safe (Potable)', 'Contaminated (Non-Potable)'],
                'Sample Count': [potable_count, unsafe_count]
            }).set_index('Water Quality Verdict')
            
            st.bar_chart(summary_chart_df, color="#0284c7")

            # Table View
            st.markdown("#### 🔬 Detailed Lab Records & AI Diagnostics")
            st.dataframe(results_df, use_container_width=True, hide_index=True)

            # Download Processed Results
            csv_export = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Classified Batch Report (CSV)",
                data=csv_export,
                file_name="AquaSafe_Classified_Lab_Batch.csv",
                mime="text/csv",
                use_container_width=True
            )


# =========================================================
# TAB 3: Model Explainability & Feature Importance
# =========================================================
with tab_analytics:
    st.markdown("### 📊 Machine Learning Model Diagnostics & Explainability")
    st.caption("Inspect the algorithmic architecture, feature importance hierarchy, and validation metrics powering the AquaSafe AI engine.")

    col_m1, col_m2 = st.columns([1.2, 1])
    
    with col_m1:
        st.subheader("🌲 Feature Importance (Gini Impurity Contribution)")
        st.write("Identifies which chemical indicators contribute the most to potability classification decisions:")
        
        # Calculate feature importances
        importances = model.feature_importances_
        fi_df = pd.DataFrame({
            'Importance': importances
        }, index=[WHO_STANDARDS[f]['name'] for f in feature_names]).sort_values('Importance', ascending=False)

        st.bar_chart(fi_df, color="#0ea5e9")

    with col_m2:
        st.subheader("⚙️ ML Pipeline Specifications")
        st.markdown(f"""
        - **Classifier:** `RandomForestClassifier`
        - **Ensemble Depth:** `150 Decision Trees` (max_depth=12)
        - **Class Balancing:** `class_weight='balanced'` (prevents minority class bias)
        - **Missing Value Handling:** Median SimpleImputer
        - **Feature Normalization:** Standard Gaussian Scaling (`StandardScaler`)
        - **Train / Test Division:** 80% Training, 20% Stratified Validation
        - **Dataset Holdout Accuracy:** **{accuracy * 100:.2f}%** (not real-world validation)
        """)
        
        st.markdown("#### 🛡️ AICTE & IBM Capstone Alignment")
        st.info("""
        - **Class 3 Standard:** Strict `iloc` feature/label separation & stratified 80/20 train-test split.
        - **Advisory Layer:** Generates suggested follow-up actions from configured screening flags; it does not issue official instructions.
        - **Zero Hardware & Zero Paid API Dependency:** Self-contained, reproducible, and verifiable offline.
        """)


# =========================================================
# TAB 4: Parameter Reference Guide
# =========================================================
with tab_guidelines:
    st.markdown("### 📋 Parameter Reference Guide")
    st.caption("Configured screening references for this prototype. They are not a substitute for the complete BIS / WHO drinking-water standard.")

    for k, v in WHO_STANDARDS.items():
        with st.expander(f"🔹 {v['name']} (Reference: {v['min']} - {v['max']} {v['unit']})"):
            st.markdown(f"**Health & Toxicological Hazard:** {v['hazard']}")
            st.markdown(f"**Standard Municipal Remediation:** {v['remedy']}")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    AquaSafe AI | AICTE - IBM SkillsBuild Machine Learning & Applied AI Internship Capstone 2026<br>
    Built for UN SDG 6: Clean Water and Sanitation & UN SDG 3: Good Health and Well-Being
</div>
""", unsafe_allow_html=True)
