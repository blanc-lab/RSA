import streamlit as st
import pandas as pd
from datetime import datetime, date

###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

###################################

from functionforDownloadButtons import download_button
import footer as footer
###################################

def _max_width_():
    max_width_str = f"max-width: 2400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="📊", page_title="Forecast",layout="wide")








###################################

with st.sidebar:
    st.image(
    "https://www.duytan.com/Data/Sites/1/media/home/logo_duytan_scgp-endorsement_full-color-01.png",
    width=300,
    )    
    st.title("TIME SERIES FORECAST")
    st.title("1. Select Data")
    uploaded_file = st.file_uploader("Choose a Excel file")
    
    
    #####
    footer.footer()
    
    #####

     
    if uploaded_file is not None:
        shows = pd.read_excel(uploaded_file, sheet_name = "Sheet1")
        shows = shows.fillna(0)
        #uploaded_file.seek(0)
        #st.write(shows)
        #unpivot & pivot to WIDE-FORMAT
        shows = pd.melt(shows, id_vars=shows.columns[0])
        #shows.sort_values(by=['Date'],inplace=True)
        shows["Date"] = shows["Date"].apply(lambda x: x.date())
        shows2 = shows.copy(deep=True)
        shows2["Date"] = shows2["Date"].apply(lambda x: x.strftime("%m-%Y"))
        #shows.set_index(['Date', 'variable'],inplace=True)
        #shows = shows.unstack('Date').reset_index()
        shows = pd.pivot_table(shows, values="value",index="variable",columns="Date").reset_index()
        shows.rename({'variable': 'Material'}, axis=1, inplace=True)
        shows2 = pd.pivot_table(shows2, values="value",index="variable",columns="Date").reset_index()
        shows2.rename({'variable': 'Material'}, axis=1, inplace=True)
        
        
        
    else:
        st.info(
            f"""
                👆 Upload your .xlsx file to make forecast. Here's a sample file: [Actual Sales](https://duytan-my.sharepoint.com/:x:/g/personal/phamgiaphu_duytan_com1/EYe1ArKWaulDhLa1G9mPrnMB7C3G_F_mkvJ-7c93u6c9kw?e=j3HVCj)
                """)
        st.stop()

###################################

top = st.columns(1)


with top[0]:
    st.subheader('1. Data loading 📋')
    st.write("Your raw data will show here.")
    st.write(shows)



from st_aggrid import GridUpdateMode, DataReturnMode

col1, col2 = st.columns(2)
with col1:
    gb = GridOptionsBuilder.from_dataframe(shows2)
    #enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
    gb.configure_default_column(enablePivot=False, enableValue=False, enableRowGroup=False)
    gb.configure_selection(selection_mode="multiple",use_checkbox=True)
    gb.configure_column(shows2.columns[0],headerCheckboxSelection=True)
    gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
    gridOptions = gb.build()

with col2:
    st.checkbox("UCM")
    st.checkbox("SARIMA")
    st.checkbox("Prophet")

  
response = AgGrid(
    shows2,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

df = pd.DataFrame(response["selected_rows"])

st.subheader("Filtered data will appear below 👇 ")
st.text("")

st.table(df)

st.text("")

c29, c30 = st.columns([1, 1])

with c29:

    CSVButton = download_button(
        df,
        "File.csv",
        "Download to CSV",
    )

with c30:
    CSVButton = download_button(
        df,
        "File.csv",
        "Download to TXT",
    )
