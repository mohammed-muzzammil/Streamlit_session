import streamlit as st
import pandas as pd
import os
import cx_Oracle
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression


temp='\\temp.csv'

path=os.getcwd()
path=path+temp

st.title("Data Pre Processing  Application")


def to_excel(df):
        
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer)
    writer.save()
    processed_data = output.getvalue()
    return processed_data





# All Functions
def mvt_mean(df):
    
    clean_df=(df.fillna(df.mean()))
    clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
    st.dataframe(clean_df)
    return df



def upload_csv(uploaded_file):
    
    try:
        
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            df.to_csv(path, index=False)
            return df

    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df
    

    
def upload_xlsx(uploaded_file):
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        df.to_csv(path, index=False)
        return df    





# File Upload 
def file_upload():

        st.sidebar.header("Data Import")                               
        f_option=('.Xlsx','.Csv','Oracle', 'jpg')
        f_select=st.sidebar.radio('Choose a file type',f_option)

        if f_select == '.Xlsx':
            uploaded_file = st.sidebar.file_uploader("Choose a file", type="xlsx")
            if uploaded_file:
                if st.sidebar.button('Upload File'):
                    df=upload_xlsx(uploaded_file)

        elif f_select == ".Csv":
            uploaded_file = st.sidebar.file_uploader("Choose a file ", type="csv")
            if uploaded_file:
                if st.sidebar.button("Upload csv file"):
                    df = upload_csv(uploaded_file)
                    
        elif f_select == "jpg":
             
            file = st.file_uploader("Please Select", type = "jpg")
            if file:
                if st.button('Upload'):
                    img = file.read()
                    st.image(img)


        elif f_select == "Oracle":

            st.info("Enter Oracle Database information")

            user=st.text_input("Enter User name ")
            passwd=st.text_input("Enter Password ", type="password")
            host=st.text_input("Enter Host Address")
            port=st.text_input("Enter Port number")
            query =st.text_input("Enter the query for the desired data")


            if st.button("Connect"):

               # muzzammil/123@46:99/ORCL


                con_query="{}/{}@{}:{}/ORCL".format(user,passwd,host,port)

                con=cx_Oracle.connect(con_query)

                if con!=None:
                    st.info("Connection Established Successfully")
                    df = pd.read_sql(query,con)
                    st.dataframe(df)
                    df.to_csv(path, index=False)
                    
                    


            
# Processing Data
def missing_value_treatment():

        st.sidebar.header("Missing value Treatment")
        missing_value_option = ["mean","median","mode"]
        missing_value = st.sidebar.radio("Choose a method", missing_value_option)

        if missing_value == "mean":
            if st.sidebar.button("Process mean"):
                df = pd.read_csv("temp.csv")
                df = mvt_mean(df)
                df.to_csv(path)
                
                
# Options for Outlier Treatment
def options_outlier_treatment():
    st.sidebar.header("Outlier Treatment")
    ot_options = ["IQR", "Z-Score"]
    ot_value = st.sidebar.radio("Choose a Outlier Method", ot_options)
    if ot_value == "IQR":
        st.write("IQR")
    elif ot_value == "Z-Score":
        st.write("Z-Score")
    return
        
        
# Options for Feature Scaling

def options_feature_scaling():
    st.sidebar.header("Feature Scaling")
    fs_options = ["Standard Scaler", "Min Max Scaler", "Robust Scaler"]
    fs_value = st.sidebar.radio("Choose a feature scaling Method", fs_options)
    
    if fs_value == "Standard Scaler":
        st.write("Standard Scaler")
        
    elif fs_value == "Min Max Scaler":
        st.write("Min Max Scaler")
        
    elif fs_value == "Robust Scaler":
        st.write("Robust Scaler")
        
    return
        
        
    

        
        
    
    
                
                
                

# Pre Processing Options

def pre_processing_options():
    st.sidebar.header("Data Pre Processing")
    options = ["Missing value Treatment", "Outlier Treatment", "Feature Scaling"]
    value  = st.sidebar.radio("Choose a Pre Procssing Method", options
                             )
    if value == "Missing value Treatment":
        missing_value_treatment()
        
    elif value == "Outlier Treatment":
        options_outlier_treatment()
    
    elif value == "Feature Scaling":
        options_feature_scaling()
        
        
        

        
        

    
def main():
    file_upload()
    pre_processing_options()
    

main()
        
        








    

