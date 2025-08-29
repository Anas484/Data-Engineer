# 🏠 NestFinder

Welcome to **NestFinder** – a Streamlit web app to explore rental and sale listings in Mumbai.  
Built with **Streamlit**, **PostgreSQL (RDS)**, and **Python**.  

🌐 **Live Demo:**  
👉 [Visit the App](https://anas-house.streamlit.app/)  

---

## ✨ Features
- 🔍 Search by **BHK, location, and area size**
- 📊 Interactive **dashboard and visualizations**
- ⚡ Fast queries powered by **PostgreSQL on AWS RDS**
- 🎨 Simple and modern UI with Streamlit

---

## 🚀 Run Locally
Clone the repo and install requirements:

```bash
git clone https://github.com/Anas484/Data-Engineer/Streamlit_house_app.git
cd Streamlit_house_app
pip install -r requirements.txt
streamlit run main.py

Database Structure for the APP

```sql
CREATE TABLE IF NOT EXISTS houses (
row_hash_id   VARCHAR(64) PRIMARY KEY,
name          TEXT,
flatType_bhk  INT,
bathrooms     INT,
area_sqft     INT,
area_type     TEXT,
price         NUMERIC,
deposit       NUMERIC,
rentOrsale    TEXT,
locality      TEXT,
link          TEXT,
processed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
