# Import python packages
import streamlit as st
# import pandas as pd
from snowflake.snowpark.functions import col  # Import col function
import requests    
# st.text(fruityvice_response)
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw: ")

st.write(
    """Choose the fruits you want in your custom Smoothiel!  
    """
)
# import streamlit as st

name_on_order= st.text_input("Name On Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)


# st.write("You selected:", option)
cnx=st.connection("snowflake")  

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))    
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

#st.dataframe (data-my_dataframe, use_contai
ingredients_list =st.multiselect(
'Choose up to 5 ingredients:'
, my_dataframe
)
# if ingredients_list:
#  st.write(ingredients_list)   
#  st.text(ingredients_list)
# time_to_insert =st.button('Submit Order')
# ingredients_string = ""  # Initialize ingredients_string
ingredients_string = "" 
if ingredients_list :
    # ingredients_string = "" 
 
 
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '
        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        # st.dataframe(pd_df)
        # st.stop()
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df =st.dataframe(data=fruityvice_response.json(), use_container_width=True)
     
 # st.write(ingredients_string)
    
 
#  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#                       values ('""" + ingredients_string + """','"""+name_on_order+""")"""
        

#  st.write(my_insert_stmt)
#  st.stop()

 
# # time_to_insert =st.button('Submit Order')


my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients,name_on_order)
                        VALUES ('{}', '{}') """.format(ingredients_string, name_on_order)
time_to_insert =st.button('Submit Order')
session.sql(my_insert_stmt).collect()
st.success('Your Smoothie is ordered!', icon="✅")

    
    



