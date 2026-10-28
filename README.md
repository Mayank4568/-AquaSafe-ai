# AquaSafe AI 🚰
### Intelligent Drinking Water Potability Classifier & Emergency Advisory Engine
**AICTE – IBM SkillsBuild Machine Learning & Applied AI Internship 2026**  
**Theme:** UN Sustainable Development Goal 6 (Clean Water & Sanitation) & Goal 3 (Good Health and Well-Being)

---

## 📌 Project Overview
AquaSafe AI is an end-to-end Machine Learning and Agentic AI solution that analyzes chemical laboratory water reports and classifies potability with high accuracy. When hazardous contamination is detected, it auto-generates a structured WHO-compliant remediation protocol for municipal water caretakers.

---

## 📁 Repository Structure
```
AquaSafe-AI/
├── Deliverables/
│   ├── AquaSafe_AI_Concept_Note.docx
│   ├── AquaSafe_AI_Concept_Note.pdf
│   ├── AquaSafe_AI_Lean_Canvas.docx
│   ├── AquaSafe_AI_Lean_Canvas.pdf
│   └── AquaSafe_AI_Pitch_Deck.pptx
├── dataset/
│   └── water_potability.csv
├── models/
│   └── aquasafe_pipeline.pkl
├── train_model.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack & Methodology
- **Language:** Python 3.9+
- **Machine Learning:** `scikit-learn` (`RandomForestClassifier`, `SimpleImputer`, `StandardScaler`)
- **Data Manipulation:** `pandas`, `numpy`
- **Dashboard / UI:** `streamlit`
- **Model Persistence:** `joblib`
- **Zero Paid APIs & Zero Hardware Sensors Required**

---

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
cd C:\Users\Mayank\AquaSafe-AI
pip install -r requirements.txt
```

### 2. Train the Machine Learning Model
```bash
python train_model.py
```
*Trains on 3,276 water quality records with median imputation, feature scaling, and evaluates accuracy, precision, recall, and F1-score.*

### 3. Launch the Interactive Streamlit Web Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`. 

#### 🌟 Key Dashboard Capabilities for Reviewers:
1. **Live Potability Classifier:** Instant 1-click test presets (*Safe Municipal Tap Water*, *Hard Borewell Water*, *Toxic Industrial Runoff*) with WHO chemical threshold compliance checking.
2. **Batch CSV Laboratory Inspection:** Upload bulk water quality CSV reports or test the pre-packaged 50-sample dataset, complete with exportable diagnostic reports.
3. **ML Model Diagnostics & Feature Importance:** Visual Gini impurity rankings explaining which chemical parameters most strongly influence potability decisions.
4. **Autonomous Emergency Remediation:** Auto-generates structured WHO 4th Edition treatment protocols (Alum coagulation, RO, GAC filtration) with downloadable text advisories.
5. **WHO Reference Guide:** Interactive chemical constituent guide detailing permissible limits and toxicological health hazards.

---

