#---------------------------- LIBRERÍAS ----------------------------#
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import folium
import geopandas as gpd
import streamlit.components.v1 as components





#---------------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------------#

st.set_page_config(
    page_title="AirBnb San Francisco",
    #page_icon=
    layout="wide"    # centered o wire
)
    #initial_sidebar_state="expanded"   # Menú despliegue inicial, con 'expanded estará siempre abierto por defecto. Con "collapsed" cerrado

logo = "Streamlitapp_Airbnb_SF/img/logo.png"




#---------------------------- COSAS QUE SE VAN A USAR EN TODA LA APP ----------------------------#
df = pd.read_csv("Streamlitapp_Airbnb_SF/data/listings_preprocessed.csv")
# df = df.drop(columns=[''])
df = df.rename(columns={'neighbourhood_cleansed': 'neighbourhood'})                                                                                         # Cambiar nombre a columna 'neighbourhood_cleansed'

columnas_a_mostrar = ['price', 'neighbourhood', 'property_type', 'room_type', 'bedrooms', 'bathrooms', 'accommodates', 'availability_365', 'price_range']   # Columnas que quiero mostrar
df_filtrado = df[columnas_a_mostrar]                                                                                                                        # Filtrar el DataFrame para mostrar solo las columnas seleccionadas




#---------------------------- HEADER ----------------------------#
st.image(logo, width=250)    # width=tamaño
st.title("Type of listings and price summary in San Francisco")
st.header("")
st.header("")






#---------------------------- SIDEBAR ----------------------------#
# Todo lo que hagamos en la pantalla principal, se puede hacer también en el sidebar
st.sidebar.image(logo, width=120)    # width=tamaño
st.sidebar.title("Filtros")
st.sidebar.write("----------------")




#---------------------------- FILTRO PRECIO ----------------------------#
filtro_precio = st.sidebar.multiselect('price_range', df_filtrado['price_range'].unique())
if filtro_precio:
    df_filtrado = df_filtrado[df_filtrado['price_range'].isin(filtro_precio)]




#---------------------------- FILTRO TIPO HABITACIÓN ----------------------------#
filtro_room_type = st.sidebar.multiselect('room_type', df_filtrado['room_type'].unique())
if filtro_room_type:
    df_filtrado = df_filtrado[df_filtrado['room_type'].isin(filtro_room_type)]




#---------------------------- FILTRO TIPO PROPIEDAD ----------------------------#
filtro_property_type = st.sidebar.multiselect('property_type', df_filtrado['property_type'].unique())
if filtro_property_type:
    df_filtrado = df_filtrado[df_filtrado['property_type'].isin(filtro_property_type)]




#---------------------------- FILTRO BARRIO ----------------------------#
filtro_neighbourhood = st.sidebar.multiselect('neighbourhood', df_filtrado['neighbourhood'].unique())
if filtro_neighbourhood:
    df_filtrado = df_filtrado[df_filtrado['neighbourhood'].isin(filtro_neighbourhood)]




#---------------------------- RESET FILTERS ----------------------------#
#if st.sidebar.button('Reset filters'):
#    df = pd.read_csv("data/listings_copy.csv")




#---------------------------- BODY 1 - Type of listings ----------------------------#

st.dataframe(df_filtrado)
st.header("")
st.header("")




#---------------------------- TABS ----------------------------#
tab1, tab2, tab3 = st.tabs(
    ['Listings', 'Rental Property Attributes', 'Data summary & correlation']
)




#---------------------------- Listings (tab1) ----------------------------#
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Listings count by neighbourhood")
        neighbourhood_counts = df['neighbourhood'].value_counts().sort_values(ascending=True)
        # Crear el gráfico de barras con Plotly
        fig = px.bar(neighbourhood_counts, x=neighbourhood_counts.values, y=neighbourhood_counts.index)

        fig.update_layout(                                                                  # Actualizar el layout para ajustar a las necesidades de visualización
            xaxis_title='Number of listings',
            yaxis_title='',
            height=700,  
        )

        fig.update_xaxes(
            tickfont=dict(size=14),                                                         # Ajusta este valor según sea necesario para tu gráfico
        )

        fig.update_traces(marker_color='#fac8b5',                                           # Establecer el color de las barras
                          hovertemplate='Neighbourhood: %{y}<br>Number of listings: %{x}')                  
        st.plotly_chart(fig, use_container_width=True)                                      # Asegurar que Streamlit use el ancho completo de la columna para el gráfico
                
        
    with col2:
        st.header("")
        st.header("")
        st.header("")
        st.header("")
        st.header("")
        try:
            with open('streamlitapp_Airbnb_SF/html/listings_by_neighbourhood.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                components.html(html_content, height=430)
        except Exception as e:
            st.error(f"An error occurred: {e}")  
    
    


#---------------------------- Rental Property Attributes (tab2) ----------------------------#
with tab2:
    col1_2, col3 = st.columns([2, 1])  # Fusionar las dos primeras columnas en una sola

    with col1_2:
        st.subheader("Types of property (TOP 10)")
        try:
            with open('streamlitapp_Airbnb_SF/html/types_property_top10.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                components.html(html_content, height=420, width=800)
        except Exception as e:
            st.error(f"An error occurred: {e}")

        st.subheader("Number of accomodates in entire rental")
        st.image('Streamlitapp_Airbnb_SF/img/accommodates_entire_rental.png', width=800)

    with col3:
        st.subheader("Renting Types")
        rooms_type = df['room_type'].value_counts().reset_index()                          
        rooms_type.columns = ['room_type', 'listings_count']                               
        rooms_type = rooms_type.sort_values(by='listings_count', ascending=False)          
        st.write(rooms_type)

        



#---------------------------- Data summary & correlation (tab3) ----------------------------#
columnas_a_mostrar_2 = ['price', 'bedrooms', 'bathrooms', 'accommodates', 'availability_365']   # Columnas que quiero mostrar
df_filtrado_2 = df[columnas_a_mostrar_2] 

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Correlation")
        st.write(df_filtrado_2.describe())
    with col2:
        if st.checkbox('Display correlation'):
            fig, ax = plt.subplots()
            sns.heatmap(df_filtrado_2.corr(), annot=True, cmap='coolwarm')
            st.pyplot(fig)
            
            
            
            
            
#---------------------------- BODY 2 - Prices ----------------------------#         

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.markdown("Muestra de los datos")
st.markdown('<iframe title="price" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiMTc2YjNlZTMtNzI1MC00YWMwLTkwNjktYjM1MzkwNGMwM2MxIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)



    
    
    
    
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
