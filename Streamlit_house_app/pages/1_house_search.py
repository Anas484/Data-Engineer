import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(layout="centered")
st.title("House :blue[Finder] :house:")

try:
    db_config = st.secrets["database"]

    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"]
    )
    if conn:
        st.badge("Connected", color="green")
except:
    st.badge("Disconnected", color="red")

# ---------------------- FILTERS ----------------------
area_options = ["Carpet Area", "Built-up Area", "Super Built-up Area"]
area_type = st.pills("Area Type", area_options, selection_mode="multi")

area_sqrft = st.select_slider("Select a range of area sqrft",options=[i for i in range(100,5100,100)],value=(100,500))
st.write(area_sqrft)


bhk_options = st.multiselect("No. of Bedrooms", ["1", "2", "3", "4", "5"])

col1 , col2 = st.columns(2)
with col1:
    price_min = st.number_input("Enter Min Price")
    st.write("The current number is ", price_min)
with col2:
    price_max = st.number_input("Enter Max Price")
    st.write("The current number is ", price_max)
local = ["Matunga West","Majiwada","Wadala","Parel","Abhyudaya Nagar","Ghatkopar East","Ashok Nagar","Dadar","Worli","Chembur East","Kandivali East","Kanjurmarg west","Lower Parel","Prabhadevi","Lokhandwala Kandivali East","Mulund East","Lokhandwala Andheri West","Goregaon West","Dadar West","Dadar East","Hanuman Nagar","Vikhroli East","Marol","Pali Hill","Pant Nagar","Upper Govd Nagar","BDD Chawls Worli","Bandra Kurla Complex","Mahim West","Lower Parel West","Dahisar East","Wadala East","Vile Parle East","Kanjurmarg East","Andheri West","Chembur","Kurla West","Goregaon East","Lalbaug","Powai","Andheri East","Anand Nagar","Tunga Village","Borivali East","Byculla","Hiranandani Gardens Powai","Bandra East","Amboli","Kanchpada","Thakur complex","Vaishali Nagar","Thakur Village","Old Prabhadevi","Lokhandwala Complex","Tilak nagar","Malad West","Yamuna Nagar","Santacruz East","Versova","Garodia Nagar","Napean Sea Road","Deonar","Matunga","Netaji Subhash Nagar","Upper Worli","Reclamation","Malad East","Paranjape Nagar","Nehru Nagar","Bandra West",'mg road',"Sakaka","JVLR","Mahalaxmi","Pirojshanagar","Gamdevi","Peddar Road"]

with conn.cursor() as cur:
        cur.execute("select distinct(locality) from houses")
        data = cur.fetchall()
local_list = [row[0] for row in data]

locality = st.multiselect("Locality", local_list if conn else local)

submit = st.button("Search")

# ---------------------- QUERY BUILDER ----------------------
query = "SELECT name, flattype_bhk, bathrooms, area_sqft, area_type, price, deposit, rentorsale, locality, link FROM houses"
conditions = []

if area_type:
    formatted = ",".join([f"'{a}'" for a in area_type])
    conditions.append(f"area_type IN ({formatted})")

if bhk_options:
    formatted = ",".join([f"'{b}'" for b in bhk_options])
    conditions.append(f"flattype_bhk IN ({formatted})")

if locality:
    formatted = ",".join([f"'{l}'" for l in locality])
    conditions.append(f"locality IN ({formatted})")

if area_sqrft:
    min,max = area_sqrft
    conditions.append(f"area_sqft BETWEEN {min} AND {max} ")

if price_min and not price_max:
    conditions.append(f"price >= {price_min}")
elif price_max and not price_min:
    conditions.append(f"price <= {price_max}")
elif price_min and price_max:
    conditions.append(f"price BETWEEN {price_min} AND {price_max} ")

if conditions:
    query += " WHERE " + " AND ".join(conditions)


st.write("Generated SQL:")
st.code(query, language="sql")

if submit:
    with conn.cursor() as cur:
        cur.execute(query=query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data,columns=columns)
        st.write("Returned : ", len(df))
        with st.container():
            st.dataframe(df)