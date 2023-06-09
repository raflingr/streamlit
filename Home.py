import streamlit as st
import pandas as pd 
import streamlit.components.v1 as stc
import plotly.express as px
import time
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import * 

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
#pip install -U scikit-learn

st.set_page_config(page_title="rafli085 ", page_icon="📈", layout="wide")  
st.subheader("⏱ Prediksi Peminjaman")
st.write("Pilih jenis bisnis yang kamu inginkan, pilih lokasi dan daerah tempat kamu tinggal, kemudian cek probabilitas untuk mendapat pinjaman")
st.markdown("##")
 
 
#for database use these two commented lines
#result = view_all_data()
#df = pd.DataFrame(result,columns=["Peraturan","Kadaluarsa","Lokasi","Negara","Provinsi","Investasi","Konstruksi","Tipe Bisnis","Ketidakseimbangan","Flood","Rating","id"])

#for excel use this line
df=pd.read_excel('data.xlsx', sheet_name='Sheet1')

#st.sidebar.image("data/logo1.png",caption="Online Analytical")

#2. switcher
st.sidebar.header("Filter di Sini:")
state= st.sidebar.selectbox(
    "Pilih Negara:",
    options=df["State"].unique(),
    help="Tempat Bisnis Teralokasikan",   
)
region = st.sidebar.selectbox(
    "Pilih Zona:",
    options=df["Region"].unique(),
    help="segment within a Region"  
)
location = st.sidebar.radio(
    "Pilih Lokasi:",
    options=df["Location"].unique(),
    help="Area Kota atau Desa"
     
)
construction = st.sidebar.radio(
    "Pilih Fasilitas:",
    options=df["Construction"].unique(),
    help="Barang atau Jasa"
)


df_selection = df.query(
    "State == @state & Location ==@location & Region==@region & Construction==@construction"
 )

   

 
 
    #simple bar graph
investment_by_business_type=(
        df_selection.groupby(by=["BusinessType"]).count()[["State"]].sort_values(by="State")
    )
fig_investment=px.bar(
       investment_by_business_type,
       x="State",
       y=investment_by_business_type.index,
       orientation="h",
       title=" Investasi Berdasarkan Tipe Bisnis",
       color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
       template="plotly_white",
    )


fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
     )
 



try:
 with st.expander("Tabular"):
  #st.dataframe(df_selection,use_container_width=True)
  shwdata = st.multiselect('Filter :', df_selection.columns, default=["Location","State","Region","Investment","Construction","BusinessType"])
  st.dataframe(df_selection[shwdata],use_container_width=True
  )
 
 df_selection['Negara'].replace(['Dodoma','Kigoma','Iringa','Mwanza','Dar es Salaam','Kilimanjaro','Arusha'],[1,2,3,4,5,6,7],inplace=True)
 df_selection['Lokasi'].replace(['Kota','Desa'],[1,2],inplace=True)
 df_selection['Provinsi'].replace(['Timur','Barat Tengah','Timur Laut','Tengah'],[1,2,3,4],inplace=True)
 df_selection['Konstruksi'].replace(['Frame','Fire Resist','Masonry','Metal Clad'],[1,2,3,4],inplace=True)

 X=df_selection.drop(columns=['BusinessType'])
 y=df_selection.drop(columns=['Location',  'State',  'Region',  'Investment',  'Construction'])
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
 clf = DecisionTreeClassifier()
 clf.fit(X_train, y_train)
 DecisionTreeClassifier()
 test = clf.predict(X_test)
 from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
 accuracy = accuracy_score(y_test, test)

 
 col1,col2=st.columns(2)

 with col1:
  st.dataframe(df_selection["BusinessType"].unique(),use_container_width=True)

 with col2:
  st.write("Loan Probability:", round(accuracy,2))
  st.title(f"{round(accuracy*100,1)} %")
  st.markdown("""---""")
  new_user=clf.predict([[df_selection["State"].unique(),df_selection["Location"].unique(),df_selection["Region"].unique(),0,df_selection["Construction"].unique()]]) 
  st.write("Recommended Facility")
  st.info(",".join(new_user))
 st.plotly_chart(fig_investment,use_container_width=False,theme="streamlit") 

except:
     st.info("One of selection is Required")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
 

    


