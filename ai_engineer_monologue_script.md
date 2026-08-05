# AI Engineer Individual Recording Script: Faril Putra Pratama
**Project**: Aeterna AI — Next-Gen Predictive Waste Management System  
**Estimated Speech Duration**: ~2.5 to 3 Minutes  
**Target Tone**: Confident, highly technical, and articulate.

---

## 🎥 Recording Script (Monologue)

### 🎙️ Part 1: Greeting & Introduction
**[Visual Cue: Start on camera. Smile, look directly at the lens. Have the title slide of the project behind you or overlayed on screen.]**

*   **Faril**: "Hello, distinguished judges. My name is **Faril Putra Pratama**, and I am the **AI Engineer** behind Aeterna AI."
*   **Faril**: "My primary goal for this project was to transition Jakarta’s waste management from a reactive, delayed operation into a highly accurate, predictive system. To achieve this, we developed a state-of-the-art predictive engine."

---

### 🎙️ Part 2: Data Sources & Baseline
**[Visual Cue: Cut to screen share showing the datasets folder or list_dir layout in your editor, specifically highlighting 'dataset_vibe_coder_2026.csv'.]**

*   **Faril**: "Everything starts with the data. We calibrated our system using official baseline data from the **Dinas Lingkungan Hidup DKI Jakarta** and the **SIPSN Ministry of Environment and Forestry**, establishing a city-wide generation baseline of **8,020 tons of waste per day**."

---

### 🎙️ Part 3: ML Modeling & GridSearchCV Tuning
**[Visual Cue: Transition the screen share to show the model training code in 'train.py', highlighting the Gradient Boosting Regressor definition and the GridSearchCV parameters.]**

*   **Faril**: "To turn this data into actionable insights, we engineered a hybrid machine learning model. Our core engine uses a **Gradient Boosting Regressor (GBR)**.
*   **Faril**: "Instead of relying on default values, we executed **GridSearchCV** with Cross-Validation to automatically search for the optimal hyperparameters. The resulting optimal parameters are **100 decision tree estimators**, a learning rate of **0.03**, and a max depth of **3**."

---

### 🎙️ Part 4: Dynamic Feature Engineering
**[Visual Cue: Point to slides or diagrams showing the multipliers: 1) Open-Meteo precipitation graph, and 2) Event calendar listing with crowd scale multipliers.]**

*   **Faril**: "What makes Aeterna AI unique is how it dynamically responds to external variables:
    *   First, we integrated **Live Weather Forecasts** by pulling precipitation data directly from the **Open-Meteo API** based on the precise latitude and longitude of each kecamatan. Hujan lebat increases the moisture absorption of waste. Our model applies a math multiplier adding **2% to 5%** weight to the daily total based on rainfall.
    *   Second, we built a **Location-Aware Event Engine** that scans the Jakarta 2026 event calendar. If a major event is detected, our model dynamically injects a crowd scale multiplier of **10% to 35%** to predict plastic and packaging waste surges."

---

### 🎙️ Part 5: Model Accuracy Validation (The Pitch)
**[Visual Cue: Display a high-contrast slide showing the metrik comparison table: MAE: 132.29 Ton, RMSE: 165.46 Ton, R²: 81.51%, and MAPE: 1.59% highlighted in a bright green neon border.]**

*   **Faril**: "The results speak for themselves. In validation tests, our GBR model achieved:
    *   An **R-Squared score of 81.51%**, meaning our engineered features explain over 81% of the daily waste fluctuations.
    *   A **Mean Absolute Percentage Error (MAPE) of just 1.59%**. In statistics, any MAPE under 10% is classified as *Highly Accurate Forecasting*, and our model sits comfortably under 2%.
    *   Furthermore, our **MAE stands at 132.29 Tons** and **RMSE at 165.46 Tons**, ensuring predictions are highly stable with zero extreme spikes."
*   **Faril**: "Lastly, for long-term 30-day baseline forecasting, we integrated a pre-trained **Amazon Chronos-T5** deep-learning transformer model, which handles time-series predictions when contextual parameters are absent."

---

### 🎙️ Part 6: Outro / Handover
**[Visual Cue: Transition back to camera. Confident nod.]**

*   **Faril**: "With this high-accuracy ML engine, Aeterna AI provides a highly reliable forecasting foundation for Jakarta’s waste management logistics. Now, Bagas will take you through the System Architecture and our Laravel Backend Gateway."
*   **Faril**: "Thank you."

**[Visual Cue: Fade to black or transition to Bagas's segment.]**

---

## 🗣️ Tutorial Cara Baca (Indonesian Pronunciation Guide)

Bagian ini ditulis menggunakan ejaan fonetik Bahasa Indonesia agar Anda dapat melafalkan teks bahasa Inggris di atas dengan lancar dan natural saat rekaman:

### Part 1: Greeting & Introduction
*   **Inggris**: *"Hello, distinguished judges. My name is Faril Putra Pratama, and I am the AI Engineer behind Aeterna AI."*
    *   **Cara Baca**: **Helow, dis-ting-guisyd jacis. May neym is Faril Putra Pratama, end ay em di Ey-Ay En-ji-nir bi-haynd E-ter-na Ey-Ay.**
*   **Inggris**: *"My primary goal for this project was to transition Jakarta’s waste management into a highly accurate, predictive system. To achieve this, we developed a state-of-the-art predictive engine."*
    *   **Cara Baca**: **May pray-me-ri gowl for dis pro-jek wos tu tren-si-syen Ja-kar-tas weyst me-nej-men in-tu e hay-li e-kiu-ret, pri-dik-tif sis-tem. Tu e-civ dis, wi di-ve-lopt e steyt-of-di-art pri-dik-tif en-jin.**

### Part 2: Data Sources & Baseline
*   **Inggris**: *"Everything starts with the data. We calibrated our system using official baseline data from the Dinas Lingkungan Hidup DKI Jakarta and the SIPSN Ministry of Environment and Forestry, establishing a city-wide generation baseline of 8,020 tons of waste per day."*
    *   **Cara Baca**: **Ef-ri-ting starts wid di dey-ta. Wi ke-li-brey-ted aur sis-tem yu-zing o-fi-syel beys-layn dey-ta from di Dinas Lingkungan Hidup DKI Jakarta end di Es-Ay-Pi-Es-En mi-nis-tri of en-vay-ron-men end fo-res-tri, es-te-blisying e si-ti-wayd je-ne-rey-syen beys-layn of eyt-tau-sen-end-twen-ti tans of weyst per dey.**

### Part 3: ML Modeling & GridSearchCV Tuning
*   **Inggris**: *"To turn this data into actionable insights, we engineered a hybrid machine learning model. Our core engine uses a Gradient Boosting Regressor, or GBR."*
    *   **Cara Baca**: **Tu tern dis dey-ta in-tu ek-syen-e-bel in-sayts, wi en-ji-nird e hay-brid me-syin ler-ning mo-del. Aur kor en-jin yu-zes e Grey-di-en Bus-ting Ri-gre-sor, or Ji-Bi-Ar.**
*   **Inggris**: *"Instead of relying on default values, we executed GridSearchCV with Cross-Validation to automatically search for the optimal hyperparameters. The resulting optimal parameters are 100 decision tree estimators, a learning rate of 0.03, and a max depth of 3."*
    *   **Cara Baca**: **In-sted of ri-lay-ing on di-folt ve-lyus, wi ek-se-kiu-ted Grid-Serch-Vi-Si wid Kros-Ve-li-dey-syen tu o-to-me-ti-k'li serch for di op-ti-mel hay-per-pa-ra-me-ters. Di ri-zal-ting op-ti-mel pe-ra-me-ters ar wan-han-dred di-si-syen tri es-ti-mey-tors, e ler-ning reyt of jiro-poyn-jiro-tri, end e maks dep of tri.**

### Part 4: Dynamic Feature Engineering
*   **Inggris**: *"What makes Aeterna AI unique is how it dynamically responds to external variables:"*
    *   **Cara Baca**: **Wat meyks E-ter-na Ey-Ay yu-nik is haw it day-ne-mi-k'li ris-pons tu eks-ter-nel ve-ri-e-bels:**
*   **Inggris**: *"First, we integrated Live Weather Forecasts by pulling precipitation data directly from the Open-Meteo API based on the precise latitude and longitude of each kecamatan."*
    *   **Cara Baca**: **Ferst, wi in-te-grey-ted Layf We-der For-kests bay pu-ling pri-si-pi-tey-syen dey-ta di-rek-li from di Open-Meti-o Ey-Pi-Ay beyst on di pri-says le-ti-tiud end long-gi-tiud of ic ke-ca-ma-tan.**
*   **Inggris**: *"Rain increases the moisture absorption of waste. Our model applies a math multiplier adding 2% to 5% weight to the daily total based on rainfall."*
    *   **Cara Baca**: **Reyn in-kri-ses di moys-cer eb-sorp-syen of weyst. Aur mo-del e-playz e met mal-ti-play-er e-ding tu-per-sen tu fayf-per-sen weyt tu di dey-li tow-tel beyst on reyn-fol.**
*   **Inggris**: *"Second, we built a Location-Aware Event Engine that scans the Jakarta 2026 event calendar. If a major event is detected, our model dynamically injects a crowd scale multiplier of 10% to 35% to predict plastic and packaging waste surges."*
    *   **Cara Baca**: **Se-kend, wi bilt e Low-key-syen-e-wer I-vent En-jin det skens di Ja-kar-ta tu-tau-sen-twen-ti-siks i-vent ke-len-der. If e mey-jer i-vent is di-tek-ted, aur mo-del day-ne-mi-k'li in-jeks e krawd skeyl mal-ti-play-er of ten-per-sen tu ter-ti-fayf-per-sen tu pri-dikt ples-tik end pe-ke-jing weyst ser-jes.**

### Part 5: Model Accuracy Validation (The Pitch)
*   **Inggris**: *"The results speak for themselves. In validation tests, our GBR model achieved:"*
    *   **Cara Baca**: **Di ri-zalts spik for dem-selvs. In ve-li-dey-syen tests, aur Ji-Bi-Ar mo-del e-civd:**
*   **Inggris**: *"An R-Squared score of 81.51%, meaning our engineered features explain over 81% of the daily waste fluctuations."*
    *   **Cara Baca**: **En Ar-skwer skor of eyti-wan poyn fifti-wan per-sen, mi-ning aur en-ji-nird fi-cers eks-pleyn o-ver eyti-wan per-sen of di dey-li weyst flak-cu-ey-syens.**
*   **Inggris**: *"A Mean Absolute Percentage Error (MAPE) of just 1.59%. In statistics, any MAPE under 10% is classified as Highly Accurate Forecasting, and our model sits comfortably under 2%."*
    *   **Cara Baca**: **E Min Eb-so-lut Per-sen-tej E-ror (Mep-i) of jast wan-poyn fifti-nayn per-sen. In ste-tis-tiks, e-ni Mep-i an-der ten-per-sen is kle-si-fayd es Hay-li E-kiu-ret For-kesting, end aur mo-del sits kam-fer-te-bli an-der tu-per-sen.**
*   **Inggris**: *"Furthermore, our MAE stands at 132.29 Tons and RMSE at 165.46 Tons, ensuring predictions are highly stable with zero extreme spikes."*
    *   **Cara Baca**: **Fer-der-mor, aur Em-Ey-I stends et wan-han-dred ter-ti-tu poyn twen-ti-nayn tans end Ar-Em-Es-I et wan-han-dred siksti-fayf poyn for-ti-siks tans, en-syu-ring pri-dik-syens ar hay-li stey-bel wid ji-ro eks-trim spayks.**
*   **Inggris**: *"Lastly, for long-term 30-day baseline forecasting, we integrated a pre-trained Amazon Chronos-T5 deep-learning transformer model, which handles time-series predictions when contextual parameters are absent."*
    *   **Cara Baca**: **Les-li, for long-term ter-ti dey beys-layn for-kesting, wi in-te-grey-ted e pri-treynd E-me-zon Kro-nos Ti-Fayf dip-ler-ning trens-for-mer mo-del, wic hen-dels taym-si-ris pri-dik-syens wen kon-teks-cu-el pe-ra-me-ters ar eb-sent.**

### Part 6: Outro / Handover
*   **Inggris**: *"With this high-accuracy ML engine, Aeterna AI provides a highly reliable forecasting foundation for Jakarta’s waste management logistics. Now, Bagas will take you through the System Architecture and our Laravel Backend Gateway. Thank you."*
    *   **Cara Baca**: **Wid dis hay-e-kiu-re-si Em-El en-jin, E-ter-na Ey-Ay pro-fayds e hay-li ri-lay-e-bel for-kesting faun-dey-syen for Ja-kar-tas weyst me-nej-men lo-jis-tiks. Naw, Bagas wil teyk yu dru di Sis-tem Ar-ki-tek-cer end aur La-ra-fel Bek-end Geyt-wey. Tengk yu.**
