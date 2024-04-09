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
st.title("")
st.title("Properties & Prices - San Francisco")
st.title("")
st.title("")
st.subheader("Data exploration")
st.write("Explore the preprocessed data in the following table to view details. You can filter table data with filters in left menu. Click on the columns' header to show in ascending or descending order.")
st.header("")






#---------------------------- SIDEBAR ----------------------------#
# Todo lo que hagamos en la pantalla principal, se puede hacer también en el sidebar
st.sidebar.image(logo, width=100)    # width=tamaño
st.sidebar.title("Filters")
st.sidebar.write("----------------")




#---------------------------- FILTRO PRECIO ----------------------------#
filtro_precio = st.sidebar.multiselect('price_range', df_filtrado['price_range'].unique())
if filtro_precio:
    df_filtrado = df_filtrado[df_filtrado['price_range'].isin(filtro_precio)]




#---------------------------- FILTRO TIPO HABITACIÓN ----------------------------#
filtro_room_type = st.sidebar.multiselect('room_type', df_filtrado['room_type'].unique())
if filtro_room_type:
    df_filtrado = df_filtrado[df_filtrado['room_type'].isin(filtro_room_type)]




#---------------------------- FILTRO BARRIO ----------------------------#
filtro_neighbourhood = st.sidebar.multiselect('neighbourhood', df_filtrado['neighbourhood'].unique())
if filtro_neighbourhood:
    df_filtrado = df_filtrado[df_filtrado['neighbourhood'].isin(filtro_neighbourhood)]




#---------------------------- BODY 1 - Type of listings ----------------------------#

st.dataframe(df_filtrado)
st.header("")
st.header("")
st.header("")
st.header("")
st.title("PROPERTIES")



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
        fig = px.bar(neighbourhood_counts, 
                     x=neighbourhood_counts.values, 
                     y=neighbourhood_counts.index)

        fig.update_layout(                                                                  # Actualizar el layout para ajustar a las necesidades de visualización
            xaxis_title='Total of properties',
            yaxis_title='',
            height=700,  
        )

        fig.update_xaxes(tickfont=dict(size=14))                                            # Ajusta este valor según sea necesario para tu gráfico
        fig.update_layout(showlegend=False, yaxis_tickfont_size=12, xaxis_tickfont_size=14)
        fig.update_traces(marker_color='#fac8b5',                                           # Establecer el color de las barras
                          hovertemplate='%{y}<br>Total of properties: %{x}',
                          hoverlabel=dict(font=dict(size=16)))                  
        st.plotly_chart(fig, use_container_width=True)                                      # Asegurar que Streamlit use el ancho completo de la columna para el gráfico
                
        
    with col2:
        st.header("")
        st.header("")
        st.header("")
        st.header("")
        st.header("")
        try:
            with open('Streamlitapp_Airbnb_SF/html/listings_by_neighbourhood.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                components.html(html_content, height=430)
        except Exception as e:
            st.error(f"An error occurred: {e}")  
    
    


#---------------------------- Rental Property Attributes (tab2) ----------------------------#
with tab2:
    col1_2, col3 = st.columns([2, 1])                                                                           # Fusionar las dos primeras columnas en una sola


    with col1_2:
        # GRÁFICO 1:
        st.subheader("Total of properties by types") 
        propiedades_por_tipo = df['property_type'].value_counts().reset_index()                                 # Con 'reset_index()' convierto el resultado en un DataFrame y se restablece el índice.
        propiedades_por_tipo.columns = ['property_type', 'total_propiedades']                                   # Renombrar las columnas
        propiedades_por_tipo = propiedades_por_tipo.sort_values(by='total_propiedades', ascending=False)
        top_10_propiedades = propiedades_por_tipo.head(10)                                                      # TOP 10 DE TIPOS DE PROPIEDADES (según cantidad)

        # Crear el gráfico de dispersión con Plotly Express
        fig = px.scatter(top_10_propiedades, 
                         x='total_propiedades', 
                         y='property_type', 
                         color_discrete_sequence=['#737373'],  
                         labels={'total_propiedades': 'Count', 'property_type': ''})
        
        fig.update_yaxes(autorange="reversed")                                                # Invertir el eje y para que los tipos de propiedad aparezcan en orden descendente
        fig.update_layout(width=800, height=500, margin=dict(t=20, b=20),                     # Ajustar el tamaño de la figura, la posición del título y los márgenes superior e inferior
                          xaxis_title='',
                          yaxis_title='')
        fig.update_layout(showlegend=False, yaxis_tickfont_size=14, xaxis_tickfont_size=14)
        fig.update_traces(marker=dict(size=20), 
                          mode='markers',                                                      # Aumentar tamaño de los puntos
                          hovertemplate='<br>Total of properties: %{x}',
                          hoverlabel=dict(font=dict(size=16)))
          
        st.plotly_chart(fig, use_container_width=True)                                        # Asegurar que Streamlit use el ancho completo de la columna para el gráfico


        # GRÁFICO 2:
        st.subheader("")
        st.subheader("Number of accommodates in type of rent 'Entire home/apt'") 
        
        entire_rental = df[df['room_type'] == 'Entire home/apt']                                                    # Filtrar datos para la gráfica con los que son 'Entire home/apt'
        accommodates_entire_rental = entire_rental['accommodates'].value_counts().sort_index()                      # Contar los valores distintos de 'accommodates'
        
        fig = px.bar(x=accommodates_entire_rental.index, 
             y=accommodates_entire_rental.values, 
             color_discrete_sequence=['#737373'],  # Usar el mismo color para todas las barras
             labels={'x': 'Number of accommodates', 'y': 'Total of properties'},  # Etiquetas de los ejes
             title='')  # Título de la gráfica
             

        # Ajustar el tamaño de la figura y los márgenes
        fig.update_layout(showlegend=False, width=1500, height=750, margin=dict(l=100, r=100, t=50, b=50), yaxis_tickfont_size=14, xaxis_tickfont_size=14)
        fig.update_traces(hovertemplate='<br>Total of properties: %{y}',
                          hoverlabel=dict(font=dict(size=16)))
        
        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig)                                                                                             # Mostrar la gráfica en Streamlit

    with col3:
        st.subheader("Renting Types")
        st.subheader("")
        st.subheader("")
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
        st.write("Data describe: ")
        st.write(df_filtrado_2.describe())
    with col2:
        if st.checkbox('Display correlation'):
            fig, ax = plt.subplots(figsize=(4, 2))
            sns.heatmap(df_filtrado_2.corr(), annot=True, cmap='coolwarm', annot_kws={"size": 4}, ax=ax, cbar=False)
            ax.tick_params(axis='x', labelsize=4)       # Ajustar tamaño del texto en ejes x e y
            ax.tick_params(axis='y', labelsize=4)
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
st.write("")
st.write("")
st.write("")
st.title("PRICES (average nightly price)")
st.title("")


#---------------------------- Price summary (Power bi)(tab1) ----------------------------#
st.write("Explore the interactive data about price summary in the city. You can filter by 'neigbourhood' to see details of data. The filter is in dropdown menu in the top left corner.")
st.title("")
st.markdown('<iframe title="price_summary_SF" width="600" height="373.5" src="https://app.fabric.microsoft.com/view?r=eyJrIjoiNWM0YTkwZTktYjYyNS00ZmMwLTk4Y2EtMzIwYzgxMTU5YmZjIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)








