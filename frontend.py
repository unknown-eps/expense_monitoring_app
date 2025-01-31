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
        df['DATE']=df['DATE'].apply(lambda x:datetime.fromtimestamp(x/1000)-timedelta(hours=5, minutes=30))
        return df
    except Exception as e:
        print(f"Failed to get response from server {e}")
        st.error("Error : No fastapi server found")
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
    '<h2 style="text-align: center;">Add new data here</h2>', 
    unsafe_allow_html=True)
    with st.form("my_form"):
        type_options = ["transport", "food", "rent","essential","fun","education"]
        type_input = st.selectbox("Type", type_options)
        value_input = st.text_input("VALUE")
        submitted = st.form_submit_button("Submit")
        if(submitted):
            url = "http://127.0.0.1:8000"
            try:
                data = {"type": type_input, "value": int(value_input)}
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    st.success("Data successfully made!")
                else:
                    st.error(f"Request failed with status code {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
def check_credentials(username,password):
    st.session_state.login_attempted=True
    url='http://127.0.0.1:8000/validate'
    data={"username":username,"password":password}
    try:
        response = requests.post(url,json=data)
        if response.json():
            st.session_state.authenticated=True
    except Exception:
        st.error("Check if the backend server is up")
        st.session_state.backend = False
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated=False
        st.session_state.login_attempted=False
        st.session_state.backend=True
    if not st.session_state.authenticated:
        username=st.text_input("username")
        password=st.text_input("password")
        st.button(label="login",on_click=lambda :check_credentials(username,password))
    if st.session_state.login_attempted and not st.session_state.authenticated and st.session_state.backend:
        st.error("Invalid Credentials")

st.markdown("""
    <h1 style='text-align: center; color:aqua;'>Basic Finance app</h1>
""", unsafe_allow_html=True)
authenticate()
if st.session_state.authenticated:
    page_names=['View Raw data','View Statistical Data','Modify data']
    selected_page = st.sidebar.radio("Select Page", page_names)
    data_df = get_data()
    if(selected_page == 'View Raw data'):
        st.write('Showing Raw data', unsafe_allow_html=True)
        if(data_df is not None):
            data_df.drop('ID',axis=1,inplace=True)
            st.dataframe((data_df.sort_values(by='DATE',ascending=False)).set_index('DATE'),width=800,height=400)
    if(selected_page == 'View Statistical Data'):
        statistical_data()

    if(selected_page == 'Modify data'):
        modify_data()