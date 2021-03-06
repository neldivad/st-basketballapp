import streamlit as st
import pandas as pd
import base64
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import app_functions as app

st.title('NBA Player Stats')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
# https://www.basketball-reference.com/leagues/NBA_2011_per_game.html
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) 
        # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
        # Remove the original index column because pandas will have their own index
    return playerstats

playerstats = load_data(selected_year)
    # Returned dataframe will be dependent on the selected argument 
    # based on the sidebar dropdown. Everytime you change the value
    # from dropdown, you change the returned dataframe. 

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats['Tm'].unique())
    # clickable option will be from this list of values
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team[:5])
    # Name = 'Team',
    # 2nd argument: Possible display option is all values discovered in list
    # 3rd argument: Default displayed values in list. 

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats['Tm'].isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
test = df_selected_team.astype(str)
st.dataframe(test)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
    # doesn't work

download= st.button('Download CSV File')
if download:
  'Download Started!'
  csv = df_selected_team.to_csv(index=False).encode()
  b64 = base64.b64encode(csv).decode()  # some strings
  linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csveee file</a>'
  href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csvee file</a>'
  st.markdown(href,
              #linko,
              unsafe_allow_html=True)
    # doesn't work either

###################################
# Working download button
###############################
@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(df_selected_team)
st.download_button(
    label='clicc', 
    data= csv, 
    file_name='xd.csv',
    mime='text/csv')
   
####################################
# Heatmap
if st.checkbox('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    fig = app.make_corr_map(df, 'Title')
    
    st.plotly_chart(fig)
