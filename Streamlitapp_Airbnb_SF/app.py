#---------------------------- LIBRERÍAS ----------------------------#
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import folium
import geopandas as gpd





#---------------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------------#
st.set_page_config(
    page_title="AirBnb San Francisco",
    #page_icon=
    layout="wide",    # centered o wire
    #initial_sidebar_state="expanded"   # Menú despliegue inicial, con 'expanded estará siempre abierto por defecto. Con "collapsed" cerrado
)

logo = "img/logo.png"




#---------------------------- COSAS QUE SE VAN A USAR EN TODA LA APP ----------------------------#
df = pd.read_csv("data/listings_preprocessed.csv")
# df = df.drop(columns=[''])






#---------------------------- HEADER ----------------------------#
st.image(logo, width=250)    # width=tamaño
st.title("Informe de datos de Airbnb en San Francisco")





#---------------------------- SIDEBAR ----------------------------#
# Todo lo que hagamos en la pantalla principal, se puede hacer también en el sidebar
st.sidebar.image(logo, width=120)    # width=tamaño
st.sidebar.title("Filtros")
st.sidebar.write("----------------")




#---------------------------- FILTRO PRECIO ----------------------------#
filtro_precio = st.sidebar.multiselect('price_range', df['price_range'].unique())
if filtro_precio:
    df = df[df['price_range'].isin(filtro_precio)]




#---------------------------- FILTRO TIPO HABITACIÓN ----------------------------#
filtro_room_type = st.sidebar.multiselect('room_type', df['room_type'].unique())
if filtro_room_type:
    df = df[df['room_type'].isin(filtro_room_type)]




#---------------------------- FILTRO TIPO PROPIEDAD ----------------------------#
filtro_property_type = st.sidebar.multiselect('property_type', df['property_type'].unique())
if filtro_property_type:
    df = df[df['property_type'].isin(filtro_property_type)]




#---------------------------- FILTRO BARRIO ----------------------------#
filtro_neighbourhood = st.sidebar.multiselect('neighbourhood_cleansed', df['neighbourhood_cleansed'].unique())
if filtro_neighbourhood:
    df = df[df['neighbourhood_cleansed'].isin(filtro_neighbourhood)]




#---------------------------- RESET FILTERS ----------------------------#
#if st.sidebar.button('Reset filters'):
#    df = pd.read_csv("data/listings_copy.csv")




#---------------------------- BODY ----------------------------#

st.dataframe(df)
st.markdown("Muestra de los datos")




#---------------------------- TABS ----------------------------#
tab1, tab2, tab3 = st.tabs(
    ['Mapas', 'Gráficos', 'Predicciones']
)




#---------------------------- Mapas (tab1) ----------------------------#
with tab1:       
    st.subheader("Distribución propiedades por barrio")
    fig = px.density_mapbox(df, 
                lat='latitude', 
                lon='longitude', 
                z='price',  # Variable para la intensidad del color
                radius=10,  # Radio de la dispersión de puntos
                center=dict(lat=37.7749, lon=-122.4194),  # Centro del mapa
                zoom=10,  # Nivel de zoom inicial
                mapbox_style="carto-positron",  # Estilo del mapa
                title="Mapa densidad de precios de propiedades en San Francisco")  # Título del mapa
    st.plotly_chart(fig)




#---------------------------- Gráficos (tab2) ----------------------------#
with tab2:
    st.header("Gráficos")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Distribución de precios")
        fig = px.box(df, x='price', color_discrete_sequence=['#16385b'])                   
        st.plotly_chart(fig)
    with col2:
        st.subheader("Precios según tipo de habitación")
        fig = px.bar(df.groupby('room_type')['price'].mean())
        st.plotly_chart(fig)
    
    




#---------------------------- Predicciones (tab3) ----------------------------#
with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Correlación")
        st.write(df.describe())
    with col2:
        st.write("")
    with col3:
        if st.checkbox('Mostrar correlación'):
            fig, ax = plt.subplots()
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
            st.pyplot(fig)