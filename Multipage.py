import streamlit as st
import pandas as pd

def models():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.model_selection import train_test_split
    import streamlit as st
    import pandas as pd
    from joblib import dump, load
    import sklearn
    st.markdown(f'# {list(page_names_to_funcs.keys())[6]}')

    def results(model):
        st.markdown('## Accuracy')
        st.write(model.score(X_test, y_test))
        st.markdown('## Confusion Matrix')
        st.dataframe(confusion_matrix(y_test, model.predict(X_test)))
        st.markdown('## Classification Report')
        st.text(classification_report(y_test, model.predict(X_test)))

    def splitDataset(df):
       y_test =df['grav']
       X_test = df.drop(['grav','gravMerged'], axis = 1)
       return y_test,X_test



    st.markdown('# Machine learning models')
    st.write("""Generally speaking we can consider that accuracy scores:
                              - Over 90% - Very Good
                        - Between 70% and 90% - Good
                        - Between 60% and 70% - OK""")

    choices = ['XGBOOST','XGBOOST improved','Gradient Boosting','Gradient Boosting improved']
    #choices = ['Gradient Boosting']
    option = st.selectbox(
             'Which model do you want to try ?',
             choices)

    st.write('You selected :', option)

    @st.cache_data
    def load_data(url):
        df = pd.read_csv(url)
        return df



    df = load_data('test_sample_15_06_2023.csv')

    if df is not None:
        y_test =df['severity']
        X_test = df.drop(['severity','Unnamed: 0'], axis = 1)



    if option=='Gradient Boosting':
       st.write('Gradient Boosting score train 73.127 rmse train 0.518')
       GBC=joblib.load('GBC_model.joblib', mmap_mode=None)
       results(GBC)

    if option=='Gradient Boosting improved':
       st.write('Gradient Boosting score train 78.535 rmse train 0.463')
       GBCi=joblib.load('GBC_improved_model.joblib', mmap_mode=None)
       results(GBCi)


#     if option=='XGBOOST':
#        st.write('XGBOOST score train 78.733 rmse train 0.461')
#        xgb = joblib.load('xgb_model.joblib', mmap_mode=None)
#        results(xgb)


#     if option=='XGBOOST improved':
#        st.write('XGBOOST score train 78.733 rmse train 0.461')
#        xgbi = joblib.load('xgb_model.joblib', mmap_mode=None)
#        results(xgbi)


def intro():
    import streamlit as st
    import base64

    st.write("# Road Accidents in France #")
    st.sidebar.success("Select pages")   
       
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Multi_vehicle_accident_-_M4_Motorway%2C_Sydney%2C_NSW_%288076208846%29.jpg",
            width=700 # Manually Adjust the width of the image as per requirement
        )
    st.markdown("""
        **👈 Select the page from the dropdown on the left** to select : EDA, Dataviz, Modelling 
        or Shap Interpretation!
         ### Summary of our main tasks done to use Streamlit /GitHub
            - we prepared the data set to gain some memory
            - we select the road accident from 2012-2015
            - we kept road accident 2016 seperately to compare with our prediction
            - we did run the classification non-linear models: GBC - RFC - KNN - SVC - (XGBOOST?)
            - EDA and Dataviz are using road accidents from 2012 to 2016 
            
         ### Team

        - Deepa
        - Fan
        - Sidi
        
        Tutoring : Francesco
        
    """
    )

    st.markdown("![Alt Text](https://media.tenor.com/tuArNck3bKwAAAAC/car-crash.gif)")
    
def eda_advanced():
    import pandas as pd
    import pandas_profiling
    import streamlit as st

    from streamlit_pandas_profiling import st_profile_report
    
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    
    st.image('https://editor.analyticsvidhya.com/uploads/74223Pandas%20Profiling.png',width=700)
    
    @st.cache_data
    def load_data(url):
        df = pd.read_csv(url)
        return df
    
    
    
        
    df = load_data('EDA_advanced_sample_12062023.csv')
    
    #uploaded_file = st.file_uploader(label = '')
    
    
    #if uploaded_file is not None:
    #  df = pd.read_csv(uploaded_file)
    pr = df.profile_report()

    st_profile_report(pr)

def eda_basic():
    
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from functions import df_info, df_isnull, number_of_outliers, space, sidebar_space, sidebar_multiselect_container
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')

                                    #st.set_page_config(layout = "wide", page_icon = 'logo.png', page_title='Multipage')

    #st.header("Exploratory Data Analysis")
    st.image("https://datos.gob.es/sites/default/files/u322/grafico.jpg",width=600)
    st.write('<p style="font-size:160%">You will be able to✅:</p>', unsafe_allow_html=True)

    st.write('<p style="font-size:100%">&nbsp 1. See the whole dataset</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 2. See the description of the data</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 3. See the count and percentage of empty values</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 4. See the statistical analysis </p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:100%">&nbsp 5. Check inbalance or distribution of target variable:</p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:100%">&nbsp 6. See distribution of numerical columns</p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:100%">&nbsp 7. See count plot of categorical columns</p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:100%">&nbsp 8. Get outlier analysis with box plots</p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:100%">&nbsp 9. Obtain info of target value variance with categorical columns</p>', unsafe_allow_html=True)
    #st.image('header2.png', use_column_width = True)

    space()
    
    st.write('<p style="font-size:130%">Import Dataset</p>', unsafe_allow_html=True)

    file_format = st.radio('Select file format:', ('csv', 'excel'), key='file_format')
    dataset = st.file_uploader(label = '')


    #st.sidebar.header('Import Dataset to Use Available Features: 👉')

    if dataset:
        if file_format == 'csv':
            df = pd.read_csv(dataset).sample(n=1000)
        else:
            df = pd.read_excel(dataset).sample(n=1000)
    #@st.cache_data
    #def load_data(url):
    #   df = pd.read_csv(url)
    #   return df

    #   df = load_data('https://bol.mondial-assistance.gr/Files/Eda_basic/Eda_basic_Dataviz_07_06_2023.csv')
            #
            st.subheader('Dataframe:')
            n, m = df.shape
            st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
            st.dataframe(df)
            #repère former codes
        #repère former codes
        all_vizuals = ['Info', 'NA Info', 'Descriptive Analysis', 'Target Analysis', 
                       'Distribution of Numerical Columns', 'Count Plots of Categorical Columns', 
                       'Box Plots', 'Outlier Analysis', 'Variance of Target with Categorical Columns']
        sidebar_space(3)         
        vizuals = st.sidebar.multiselect("Choose which visualizations you want to see 👇", all_vizuals)

        if 'Info' in vizuals:
            st.subheader('Info:')
            c1, c2, c3 = st.columns([1, 2, 1])
            c2.dataframe(df_info(df))

        if 'NA Info' in vizuals:
            st.subheader('NA Value Information:')
            if df.isnull().sum().sum() == 0:
                st.write('There is not any NA value in your dataset.')
            else:
                c1, c2, c3 = st.columns([0.5, 2, 0.5])
                c2.dataframe(df_isnull(df), width=1500)
                space(2)


        if 'Descriptive Analysis' in vizuals:
            st.subheader('Descriptive Analysis:')
            st.dataframe(df.describe())

        if 'Target Analysis' in vizuals:
            st.subheader("Select target column:")    
            target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)

            st.subheader("Histogram of target column")
            fig = px.histogram(df, x = target_column)
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.plotly_chart(fig)


        num_columns = df.select_dtypes(exclude = 'object').columns
        cat_columns = df.select_dtypes(include = 'object').columns

        if 'Distribution of Numerical Columns' in vizuals:

            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = sidebar_multiselect_container('Choose columns for Distribution plots:', num_columns, 'Distribution')
                st.subheader('Distribution of numerical columns')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.histogram(df, x = selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width = True)
                        i += 1

        if 'Count Plots of Categorical Columns' in vizuals:

            if len(cat_columns) == 0:
                st.write('There is no categorical columns in the data.')
            else:
                selected_cat_cols = sidebar_multiselect_container('Choose columns for Count plots:', cat_columns, 'Count')
                st.subheader('Count plots of categorical columns')
                i = 0
                while (i < len(selected_cat_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_cat_cols)):
                            break

                        fig = px.histogram(df, x = selected_cat_cols[i], color_discrete_sequence=['indianred'])
                        j.plotly_chart(fig)
                        i += 1

        if 'Box Plots' in vizuals:
            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = sidebar_multiselect_container('Choose columns for Box plots:', num_columns, 'Box')
                st.subheader('Box plots')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.box(df, y = selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width = True)
                        i += 1

        if 'Outlier Analysis' in vizuals:
            st.subheader('Outlier Analysis')
            c1, c2, c3 = st.columns([1, 2, 1])
            c2.dataframe(number_of_outliers(df))

        if 'Variance of Target with Categorical Columns' in vizuals:


            df_1 = df.dropna()

            high_cardi_columns = []
            normal_cardi_columns = []

            for i in cat_columns:
                if (df[i].nunique() > df.shape[0] / 10):
                    high_cardi_columns.append(i)
                else:
                    normal_cardi_columns.append(i)


            if len(normal_cardi_columns) == 0:
                st.write('There is no categorical columns with normal cardinality in the data.')
            else:

                st.subheader('Variance of target variable with categorical columns')
                model_type = st.radio('Select Problem Type:', ('Regression', 'Classification'), key = 'model_type')
                selected_cat_cols = sidebar_multiselect_container('Choose columns for Category Colored plots:', normal_cardi_columns, 'Category')

                if 'Target Analysis' not in vizuals:   
                    target_column = st.selectbox("Select target column:", df.columns, index = len(df.columns) - 1)

                i = 0
                while (i < len(selected_cat_cols)):



                    if model_type == 'Regression':
                        fig = px.box(df_1, y = target_column, color = selected_cat_cols[i])
                    else:
                        fig = px.histogram(df_1, color = selected_cat_cols[i], x = target_column)

                    st.plotly_chart(fig, use_container_width = True)
                    i += 1

                if high_cardi_columns:
                    if len(high_cardi_columns) == 1:
                        st.subheader('The following column has high cardinality, that is why its boxplot was not plotted:')
                    else:
                        st.subheader('The following columns have high cardinality, that is why its boxplot was not plotted:')
                    for i in high_cardi_columns:
                        st.write(i)

                    st.write('<p style="font-size:140%">Do you want to plot anyway?</p>', unsafe_allow_html=True)    
                    answer = st.selectbox("", ('No', 'Yes'))

                    if answer == 'Yes':
                        for i in high_cardi_columns:
                            fig = px.box(df_1, y = target_column, color = i)
                            st.plotly_chart(fig, use_container_width = True)
 
    
    
    
    
def data_viz():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import pydeck as pdk
    import plotly.express as px
    import datetime as dt

    st.header('Data Visualization')

    st.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/Data_Visualization_Tools.jpg", width=700)
    #@st.cache_data

    #uploaded_file = st.file_uploader("Choose a file")
    #if uploaded_file is not None:
    # df = pd.read_csv(uploaded_file).sample(n=100000)

            
    @st.cache_data
    def load_data(url):
        df = pd.read_csv(url)
        return df

  
    df = load_data('Dataviz_12_06_2023.csv')
    
    #dropna
    df.dropna(subset=['LATITUDE', 'LONGITUDE','CRASH_DATE','CRASH_TIME'], inplace=True)


    df['date/time'] = pd.to_datetime(df['CRASH_DATE'] + ' ' + df['CRASH_TIME'])
    data = df

    #1. Visualization
    st.header("Where are the most people injured in France?")
    injured_people = st.slider("Number of person injured in road accident",0, 100)
    st.map(data.query("INJURED_PERSONS >= @injured_people")[['LATITUDE', 'LONGITUDE']].dropna(how="any"))

    #2. Visualization ######################
    st.header("How many road accident during a given time of the day?")
    hour = st.slider("Hour to look at", 0, 23)
    severity = st.radio("Severity",('Not Severe', 'Severe', 'All'))
    if severity=='Not Severe':
         severity=0
    if severity=='Severe':
         severity=1

    st.markdown("road accident between %i:00 and %i:00" % (hour, (hour + 1) % 24))

    chart_data = df[['LATITUDE','LONGITUDE','date/time','severity']].dropna(how="any")
    chart_data=chart_data.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"})
    if severity!='All':
         severity=chart_data=chart_data[chart_data['severity'] == severity]
    vis_data=chart_data[chart_data['date/time'].dt.hour == hour]

    def pychart(dataframe):
         st.pydeck_chart(pdk.Deck(
              map_style=None,
              initial_view_state=pdk.ViewState(
                   latitude=48.85,
                   longitude=2.35,
                   zoom=6,
                   pitch=50,
              ),
              layers=[pdk.Layer(
                   'HexagonLayer',
                   data=dataframe,
                   get_position='[lon, lat]',
                   radius=50,
                   elevation_scale=10,
                   elevation_range=[20, 500],
                   pickable=True,
                   extruded=True,),],
         ))

    pychart(vis_data)
    #######################

    #4. Visualization
    st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
    # filtered = data[
    #  (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
    # ]
    hist = np.histogram(data['date/time'].dt.minute, bins=60, range=(0,60))[0]
    chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
    fig = px.bar(chart_data, x='minute',y='crashes', hover_data=['minute','crashes'], height=400)
    st.write(fig)

    #5. Visualization
    st.header("Top 8 dangerous area by zone")
    #select = st.selectbox('Injured people', ['Pedestrian','Cyclists','Motorists'])
    select = st.selectbox('Injured people', ['Department','Commune','Street'])

    if select == 'Department':
         st.write(data.query("INJURED_PERSONS >= 1")[["dep","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])
    elif select == 'Commune':
         st.write(data.query("INJURED_PERSONS >= 1")[["com","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])
    else:
         st.write(data.query("INJURED_PERSONS >= 1")[["ON_STREET_NAME","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])


    if st.checkbox("Show Raw Data", False):
       st.subheader('Raw Data')
       st.write(data)

def modelling():
    import streamlit as st
    import pandas as pd
    st.markdown(f'# {list(page_names_to_funcs.keys())[4]}')
    from model import prediction, scores
    

    

    st.write("""Generally speaking we can consider that accuracy scores:
    
                          - Over 90% - Very Good
                          - Between 70% and 90% - Good
                          - Between 60% and 70% - OK""")

    choices = ['Random Forest','SVC','KNN','XGBOOST','Gradient Boosting']

    prediction = st.cache(prediction,suppress_st_warning=True)

    option = st.selectbox(
         'Which model do you want to try ?',
         choices)

    st.write('You selected :', option)

    clf = prediction(option)

    display = st.selectbox(
         "What do you want to display ?",
         ('Accuracy', 'Confusion matrix','Classification report'))

    if display == 'Accuracy':
        st.write(scores(clf, display))
    elif display == 'Confusion matrix':
        st.dataframe(scores(clf, display))
    elif display == 'Classification report':
        #st.table(classification_report(y_test, clf.predict(X_test)))
        st.text(scores(clf, display))
        
        
        
def shap(): 
    import shap
    import streamlit as st
    import streamlit.components.v1 as components
    import xgboost
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    st.markdown(f'# {list(page_names_to_funcs.keys())[5]}')
    
    #uploaded_file = st.file_uploader("Choose a file")
    #if uploaded_file is not None:
    #  df = pd.read_csv(uploaded_file)

    @st.cache_data
    def load_data(url):
        df = pd.read_csv(url)
        return df

    df = load_data('modelling_shap_2012_2015.csv')
    df = df.sample(n=1000)
    def st_shap(plot, height=None):
        shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
        components.html(shap_html, height=height)

             
    y =df['grav']
    X = df.drop(['grav','gravMerged'], axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    st.write('XGBoost model')
    model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)

    st.markdown('''explain the model's predictions using SHAP''')
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    st.write('<p style="font-size:130%"> #Visualize the first prediction explanation </p>', unsafe_allow_html=True)
    st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:]))

    st.write('<p style="font-size:130%"> #Visualize the training set predictions </p>', unsafe_allow_html=True)
    st_shap(shap.force_plot(explainer.expected_value, shap_values, X), 400)

        
page_names_to_funcs = {
    "Home Page": intro,
    "Exploratory Data Analysis advanced": eda_advanced,
    "Exploratory Data Analysis basic": eda_basic,
    "Data Visualization": data_viz,
    "Machine Learning Models": modelling,
    "Shapley Interpretation": shap,
    "Models": models
    
}

page_name = st.sidebar.selectbox("Choose your page", page_names_to_funcs.keys())

page_names_to_funcs[page_name]()
