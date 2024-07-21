import streamlit as st
import pandas as pd
from  datetime import datetime,timedelta
import matplotlib.pyplot as plt
import requests
def get_data():
    url = "http://127.0.0.1:8000"
    try:
        response = requests.get(url)
        df=pd.DataFrame(response.json())
        df['DATE']=df['DATE'].apply(lambda x:datetime.fromtimestamp(x/1000))
        return df
    except Exception as e:
        print("Failed to get response from server")
        raise NotImplementedError('Check if server is open at the url')

def filter_df(df,time_interval : int):
    '''
    Takes a dataframte and filters the DATE column for time_interval from starting date
    '''
    first_date=datetime.now()-timedelta(days=time_interval)
    return df[df['DATE']>=first_date]
def draw_gross_expenditure():
    fig, ax = plt.subplots(figsize=(10,8))
    filtered_df=data_df.groupby('TYPE')['VALUE'].sum().reset_index()
    ax.pie(filtered_df['VALUE'], labels=filtered_df['TYPE'], autopct='%1.1f%%')
    ax.axis('equal')
    ax.legend( labels=[f'{label}:{value}' for label, value in zip(filtered_df['TYPE'], filtered_df['VALUE'])],fontsize='small',loc='best')
    plt.tight_layout()
    st.pyplot(fig)
def statistical_data():
    total_expenditure=data_df['VALUE'].sum()
    st.markdown(f"""
    <h1 style='text-align: center;'>
    Total expenditure is :<span style='color:red;'>{total_expenditure}</span>
    </h1>
    """, unsafe_allow_html=True)    
    st.markdown('#')    
    st.markdown('#')    
    col1,col2=st.columns(2)
    with col1:
        filtered_df_week=filter_df(data_df,7).groupby('TYPE')['VALUE'].sum().reset_index()
        weekly_expenditure=filtered_df_week['VALUE'].sum()
        st.markdown(f'#### Weekly expenditure is :red[{weekly_expenditure}]')
        st.markdown('#')
        st.write('Weekly expenditure distribution')
        fig, ax = plt.subplots(figsize=(3,5))
        ax.pie(filtered_df_week['VALUE'], labels=filtered_df_week['TYPE'], autopct='%1.1f%%')
        ax.axis('equal')
        ax.legend( labels=[f'{label}:{value}' for label, value in zip(filtered_df_week['TYPE'], filtered_df_week['VALUE'])],fontsize='xx-small',loc='lower right')
        st.pyplot(fig)
    with col2:
        filtered_df_month=filter_df(data_df,30).groupby('TYPE')['VALUE'].sum().reset_index()
        monthly_expenditure=filtered_df_month['VALUE'].sum()
        st.markdown(f'#### Monthly expenditure is :red[{monthly_expenditure}]')
        st.markdown('#')
        st.write('Monthly expenditure distribution')
        fig, ax = plt.subplots(figsize=(3,5))
        ax.pie(filtered_df_month['VALUE'], labels=filtered_df_month['TYPE'], autopct='%1.1f%%')
        ax.axis('equal')
        ax.legend( labels=[f'{label}:{value}' for label, value in zip(filtered_df_month['TYPE'], filtered_df_month['VALUE'])],fontsize='xx-small',loc='lower right')
        st.pyplot(fig)
    st.write('<p style="font-size: 40px; color: green; text-align:center">Gross expenditure distribution</p>',unsafe_allow_html=True)
    draw_gross_expenditure()
def modify_data():
    st.markdown(
    '<h2 style="text-align: center;">Modify your data here</h2>', 
    unsafe_allow_html=True)
    
    

st.markdown("""
    <h1 style='text-align: center; color:aqua;'>Basic Finance app</h1>
""", unsafe_allow_html=True)
page_names=['View Raw data','View Statistical Data','Modify data']
selected_page = st.sidebar.radio("Select Page", page_names)
data_df = get_data()
if(selected_page == 'View Raw data'):
    st.write('Showing Raw data', unsafe_allow_html=True)
    data_df.drop('ID',axis=1,inplace=True)
    st.dataframe((data_df.sort_values(by='DATE',ascending=False)),width=800,height=400)
    
if(selected_page == 'View Statistical Data'):
    statistical_data()

if(selected_page == 'Modify data'):
    modify_data()