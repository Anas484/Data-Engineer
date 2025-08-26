import streamlit as st
import psycopg2 
import pandas as pd
import re
import os
import datetime
# Database connection
def get_connection():
    return psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 5432))
)

options = ["India","China","Russia","Japan","UAE","Indonesia","United Kingdom","United States","South Africa"]

conn = get_connection()

st.title("User Data Form")

fname = st.text_input("First Name")
lname = st.text_input("Last Name")
dob = st.date_input("Enter DOB",min_value=datetime.date(1900, 1, 1),max_value=datetime.date.today())
email = st.text_input("Email")
country = st.selectbox("Countrys", options)
phone = st.text_input("Mobile Number")

if st.button("Submit"):
    try:
        if (len(phone) < 10) :
            st.error("Please Enter 10 Digit Phone Number")
        else:
            with conn.cursor() as cursor:
                cursor.execute("select email from customer where email = %s",(email,))
                email_exists = cursor.fetchone()

                cursor.execute("select phone from customer where phone = %s",(phone,))
                phone_exists = cursor.fetchone()

                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

                if not re.match(email_pattern,email):
                    st.error("Please enter correct email.")
                elif email_exists and phone_exists:
                    st.error(f"{email} and {phone} already exist. Please enter different values.")
                elif email_exists:
                    st.error(f"{email} already exists. Please enter another email.")
                elif phone_exists:
                    st.error(f"{phone} already exists. Please enter another phone number.")
                else :
                    with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO customer (f_name, l_name, dob, email, country, phone ) VALUES (%s, %s, %s, %s, %s, %s)",
                                        (fname, lname, dob, email, country, phone))
                        conn.commit()
                    st.success("Data submitted!")
    except Exception as e:
        print("Error : ",e)


if st.button("Show All Rows"):
    try:
        with conn.cursor() as cursor:
            cursor.execute("Select * from customer")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            
            if rows:
                df = pd.DataFrame(rows,columns=columns)
                st.dataframe(df)
                st.success("All the customers displayed.")
            else:
                st.info("No customer records found.")
    except Exception as e:
        print("Error : ",e)

    
    









    