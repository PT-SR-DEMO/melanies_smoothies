# Import python packages
import streamlit as st
#Import the snowpark col function
from snowflake.snowpark.functions import col
import requests
import pandas

#set width of app
st.set_page_config(layout="wide")


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()

# ---------------------------------------------------------------------------------
# Adding a select box
#option = st.selectbox(
    #"What is your favorite fruit?",
    #("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)'''
# ---------------------------------------------------------------------------------


#Here we can collect the name of the customer before they order
#we don't need the active session just yet
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)
#we edit our insert statement later below to include this name




#Starting a session to connect to our table and get required column to add to dataframe
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#This line displays our dataframe - we can use it later to check on things
#st.dataframe(data=my_dataframe, use_container_width=True)

#For testing
#st.stop()


#Converting the Snowpark Dataframe to a Pandas Dataframe
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


#Adding a select box for our ingredients
ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        my_dataframe,
        max_selections = 5
)


#These two can be used to display our ingredients list
#we add them into an if loop, it will only display if the list is populated
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    #this line below is added to make an ingredients string
    ingredients_string = ''

    #this for loop is to populate our string list with the chosen fruits
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        #Subheader for nutrition info
        st.subheader(fruit_chosen + ' Nutrition Information')
        #New Section to display smoothiefroot nutrition information
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        #st.text(smoothiefroot_response.json())
        #Now storing the JSON response as a dataframe
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)


    #outputting the ingredients STRING
    #st.write(ingredients_string)

    #Building a SQL Insert Statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #Show the insert statement
    #st.write(my_insert_stmt)

    #GREAT FOR TESTING BEFORE WE INSERT
    #st.stop()

    #Adding a submit button, if true, the next if statement will run
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        #this code gives the sql insert statement to the sql session
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")











































