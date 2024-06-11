# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """**Choose the fruits you want in your custom Smoothie!**
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Establecer la conexión y la sesión
try:
    cnx = st.experimental_connection("snowflake")
    session = cnx.session()
    st.write("Conexión a Snowflake establecida correctamente.")
except Exception as e:
    st.error(f"Error estableciendo la conexión a Snowflake: {e}")

# Ejecutar la consulta para obtener la tabla y columnas
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
    # Recolectar los datos en un DataFrame de Pandas
    pd_df = my_dataframe.collect()
    # Convertir a DataFrame de Pandas
    pd_df = pd.DataFrame(pd_df)
    st.write("Datos obtenidos correctamente de Snowflake.")
except Exception as e:
    st.error(f"Error al obtener datos de Snowflake: {e}")

# Mostrar el DataFrame de Pandas para depuración
st.dataframe(pd_df)
st.stop()

# Crear una lista de nombres de frutas para las opciones del multiselect
fruit_names = pd_df['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = pd.DataFrame(fruityvice_response.json())
        st.dataframe(data=fv_df, use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
        except Exception as e:
            st.error(f"Error al insertar la orden en Snowflake: {e}")

    



