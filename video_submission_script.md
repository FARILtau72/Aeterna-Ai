# AI Open Innovation Challenge 2026: Video Submission Script
**Project Name**: Aeterna AI — Next-Gen Predictive Waste Management System  
**Video Length**: ~8–9 Minutes (Within the 10-minute limit)  
**Roles**:
*   **Faril** (AI Engineer)
*   **Bagas** (System Architecture — Laravel Backend)
*   **Arga** (Front-End Developer — Next.js Frontend)

---

## 🎬 Act 1: Introduction & The Bantargebang Crisis (0:00 - 1:30)

**[Visual: A clean title slide with the Kemenko Perekonomian and FabLab Jababeka logos, team name, and the Aeterna AI logo. Transition to all three members on camera or screen sharing.]**

*   **Bagas**: "Hello, distinguished judges. We are Team Aeterna, and today we are thrilled to present our solution for Case 2 of the AI Open Innovation Challenge 2026: **Aeterna AI — Next-Gen Predictive Waste Management Platform for DKI Jakarta**."
*   **Arga**: "Every single day, DKI Jakarta generates more than **8,000 tons of waste**. Historically, waste management has been **reactive**—trucks are dispatched only after trash piles up or citizens complain. This leads to massive budget waste, delayed collections, and worst of all, trash clogging waterways, which directly triggers urban flooding."
*   **Bagas**: "Furthermore, the TPST Bantargebang landfill in Bekasi is reaching its absolute capacity. To solve this, we must transition from reactive collection to **predictive analytics**. That is why we built Aeterna AI—a platform that forecasts waste surges *before* they occur, allowing the city to allocate logistics dynamically and keep Jakarta clean."

---

## 🧠 Act 2: Core AI Engine, Data Sources & ML Metrics (1:30 - 3:45)

**[Visual: Transition to Faril sharing his screen, showing the Jupyter Notebook or train.py code, followed by GBR metrics slides.]**

*   **Faril**: "Thanks, Bagas. As the AI Engineer, my goal was to build a highly accurate, feature-rich forecasting engine. We gathered our baseline dataset from official sources: the **Dinas Lingkungan Hidup (DLH) DKI Jakarta** and the **SIPSN Ministry of Environment and Forestry**, establishing a baseline city-wide generation of 8,020 tons per day."
*   **Arga**: "But we didn't stop at historical averages. Faril, how does the model handle external factors?"
*   **Faril**: "Excellent question. We engineered a hybrid ML architecture. We integrated a **Gradient Boosting Regressor (GBR)** as our primary regressor and used **GridSearchCV** to automatically fine-tune its hyperparameters. The GBR model is calibrated with two dynamic real-time features:
    1.  **Live Weather Data**: We fetch precipitation forecast (in millimeters) from the **Open-Meteo API**. Rainwater increases the weight of open-air waste. Our model applies a math formula adding a weight multiplier of 2% to 5% based on rainfall.
    2.  **Location-Aware Event Calendar**: We track major events in Jakarta, like the PRJ JIExpo, marathons, or national holidays. The model applies a crowd multiplier ranging from 10% for local events up to 35% for massive crowds, predicting plastic packaging surges."
*   **Bagas**: "What about the accuracy metrics? The judges will want to see the validation."
*   **Faril**: "Our model achieved outstanding results. After GridSearchCV tuning, we achieved:
    *   A **Mean Absolute Percentage Error (MAPE) of just 1.59%**, which classifies our system as *Highly Accurate Forecasting*—well below the 10% industry gold standard.
    *   An **R-Squared ($R^2$) Score of 81.51%**, meaning our model explains over 81% of the daily waste variation.
    *   Our **Mean Absolute Error (MAE)** dropped to **132.29 Tons**, and **RMSE** stands stable at **165.46 Tons**, proving the model is highly stable and free from wild prediction spikes."
*   **Faril**: "For long-term trend forecasting, we also integrated **Amazon Chronos-T5**, a deep-learning transformer model, which handles 30-day baseline forecasting as a fallback."

---

## 🏗️ Act 3: System Architecture, API, & Laravel Gateway (3:45 - 5:45)

**[Visual: Transition to Bagas sharing his screen, showing Laravel routes, controllers, and system architecture diagrams, followed by Hugging Face Spaces.]**

*   **Bagas**: "Thank you, Faril. To make this AI model accessible and secure, I structured the system using **Laravel** as our primary Backend API Gateway, connecting it to Faril's Python ML service on Hugging Face."
*   **Arga**: "Why did you choose Laravel for this architecture, Bagas?"
*   **Bagas**: "Laravel gives us enterprise-grade routing, robust CORS middlewares, and request validation out of the box. The Laravel backend handles:
    1.  **Event Calendar & News Logging**: It manages the event database and parses our daily waste news feed.
    2.  **Timezone-Aware Engine**: I locked the backend queries strictly to **Asia/Jakarta (WIB: UTC+7)** to prevent calendar penanggalan offsets, since cloud servers operate on UTC.
    3.  **ML Microservice Proxying**: When a user requests a prediction, Laravel validates the request, proxies it to our FastAPI-based Python container on Hugging Face Spaces, and formats the output for the client."
*   **Bagas**: "We containerized the Python ML microservice using **Docker** and deployed it on Hugging Face Spaces, exposing REST endpoints like `/api/v1/predict` and `/api/v1/autopilot` which Laravel queries asynchronously to keep response times under 200 milliseconds."

---

## 💻 Act 4: Next.js Frontend Live Demo & Interactive Cyber HUD (5:45 - 8:15)

**[Visual: Transition to Arga sharing his screen, showcasing the live dashboard running on Vercel. Moving the mouse to show the HUD cursor, clicking markers on the Leaflet map, switching tabs, and clicking alert rows.]**

*   **Arga**: "On the client side, I built our dashboard using **Next.js** for optimized rendering, visual performance, and structured React components. Our theme is an interactive **Cyber HUD Dashboard** with glassmorphic layouts, neon grids, and micro-animations."
*   **Faril**: "Since Leaflet.js relies on the browser's window object, how did you handle Next.js Server-Side Rendering (SSR)?"
*   **Arga**: "Great catch. Since Next.js uses SSR by default, I resolved Leaflet's window dependency by using **Next.js Dynamic Imports with SSR disabled**. This ensures the map renders seamlessly on the client side without throwing node-server errors."
*   **Arga**: "The map displays all 44 kecamatan with penanda badges. Green represents SAFE, yellow is WARNING, and red is CRITICAL. When I click a kecamatan, say **Menteng**, Next.js dynamically draws a glowing route directly to **TPST Bantargebang** using the **Haversine Formula**."
*   **Bagas**: "I see the details panel changed immediately. What metrics are shown there?"
*   **Arga**: "It displays the total estimated volume and deconstructs it into **6 Categories** based on official SIPSN ratios: Organic (~50%), Plastic (~22%), Paper (~11%), and others. It also outputs our **Logistics Dispatch Plan**: recommending the exact number of 5-ton trucks, the required crew size, and the estimated travel time to Bekasi at 28 km/h."
*   **Arga**: "We also implemented seamless SPA navigation. If we head to the **AI AUTOPILOT** or **REGIONAL ALERTS** page, we see active alerts triggered by the demo events Faril added. If I click on any of these alert rows, like **Tanah Abang (CRITICAL)**, Next.js smoothly transitions the viewport to the Predictor tab, pans the map, and immediately triggers GBR inference to show the dispatch details. It is fully connected and reactive!"

---

## 🚀 Act 5: Conclusion & Future Vision (8:15 - 9:00)

**[Visual: Transition back to all three team members on camera.]**

*   **Faril**: "By combining Gradient Boosting models, live weather forecasts, and event calendars, Aeterna AI achieves an unprecedented **98.41% prediction accuracy**."
*   **Bagas**: "Our Laravel backend is designed to be easily integrated into the Pemprov DKI super-app, **JAKI (Jakarta Kini)**. Warga can report trash, and our system will automatically dispatch the nearest DLH truck routing."
*   **Arga**: "Aeterna AI shifts waste management from a reactive headache to a predictive science, saving city budgets, preventing flooded canals, and ensuring a cleaner, smarter Jakarta."
*   **Bagas**: "Thank you, judges. We are ready to answer your questions and help Jakarta step into the future of waste intelligence!"

**[Visual: Fade out with contact info, GitHub repo link (https://github.com/FARILtau72/Aeterna-Ai), and Hugging Face link.]**
