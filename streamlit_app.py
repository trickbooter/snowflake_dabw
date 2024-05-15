# This Streamlit application is part of the Snowflake DABW training course
# It's a basic Streamlit app for gathering smoothie orders

# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write the app title & header text
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!\n")

# Who is the order for
name_on_order = st.text_input('Name for order?')

# Read fruit options from Snowflake
cnx = st.connection("snowflake")
session = cnx.session()
f_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Offer the user a multiselect box for their fruit choices
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,f_df
    ,max_selections=5
)

# Verify we've got ingredients to proceed with
if ingredients_list:
    # Render a submit button, and if pressed & we have ingredients, submit to the DB
    submit = st.button('Submit Order!')
    
    if submit:
        # Build a space delim string of fruits
        ingredients_string = ''
        for fruit in ingredients_list:
            ingredients_string += fruit + ' '

        if ingredients_string:
            # Create an insert statement for the Smoothie order. 
            # In reality this unchecked and unparameterised input is unsafe and open to injection
            insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

            session.sql(insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")