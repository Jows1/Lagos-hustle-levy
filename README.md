# The Lagos Hustle Levy Index
**Quantifying the hidden economic cost of the Lagos commute.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link-here.streamlit.app)

## 📌 Overview
Lagosians don't just pay for transport with Naira; they pay with **time, health, and potential.** The **Lagos Hustle Levy** is a data-driven dashboard that calculates the "True Economic Value" of a worker's salary after accounting for the "Invisible Tax" of traffic. It exposes how a ₦400k salary can effectively function like a ₦150k salary when the cost of the "hustle" is factored in.

## 🚀 Features
* **Hustle Levy Calculator:** Real-time analysis of income loss based on commute routes (Ikorodu, Ajah, Alimosho, etc.).
* **The Human Cost (Impact Analysis):** A personalized look at how specific personas (like Abike or Emeka) lose up to 60% of their economic value.
* **Interactive Visualizations:** Comparative analysis of transport modes (Danfo, BRT, Private Car) vs. Time Theft.
* **Dark Mode Aesthetic:** Designed for high-impact storytelling and readability.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Data Processing:** Pandas
* **Visuals:** Plotly Express
* **Database:** SQLite3
* **Styling:** Custom CSS (GitHub-Dark inspired)

## 📂 Project Structure
```text
├── assets/             # Custom CSS and Branding
├── data/               # SQLite database (lagos_commute.db)
├── engine/             # Main application logic (app.py)
├── requirements.txt    # Python dependencies
└── README.md           # You are here!
```
## 🏃‍♂️ How to Run Locally
1. **Clone the repo:** git clone [https://github.com/your-username/lagos-hustle-levy.git](https://github.com/your-username/lagos-hustle-levy.git)

2. **Install Dependencies:** pip install -r requirements.txt

3. **Launch the app:** streamlit run engine/app.py

## 📊 The Data
The dataset used in this project is a synthesis of Lagos commuting patterns, factoring in:

* **Direct Costs:** Fuel prices and public transport fares.

* **Opportunity Costs:** The monetary value of time spent in traffic.

* **Physiological Cost:** A "Burnout Factor" based on hours spent in transit.
