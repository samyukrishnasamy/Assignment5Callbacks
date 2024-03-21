# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   Graph DOES NOT need to interact with dropdown or slider
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# import dependencies
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px


# %%
### DATA SET ### 
# read the csv file
gdp = pd.read_csv("gdp_pcap.csv")

#convert the dataset so that the years are combines to make a column
gdp_long = gdp.melt(id_vars=['country'], var_name='Year', value_name='gdpPercap')
gdp_long['Year'] = pd.to_numeric(gdp_long['Year'])  # convert the 'Year' column to numeric

# %%
### APP LAYOUT ###
# stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# initialize Dash app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# create the app
app.layout = html.Div([
   html.H1(children="GDP Per Capita"), # app title
   html.Div(children=''' 
            Explore the GDP per capita across different countries and years using this interactive app.
            Gapminder's dataset provides the estimates of Gross Domestic Product (GDP) per capita for all countries from 1800 to 2100.
            Select one or more countries and a range of years to visualize the GDP per capita over the years.
    '''), # app description
    # display the dropdown and slider
    html.Div([
        # dropdown menu for countries
        dcc.Dropdown(
            id='country',
            options=[{'label': country, 'value': country} for country in gdp_long['country'].unique()], # show all the unique country values
            value =["USA"], # initialize the country so that dropdown automatically has USA selected
            multi=True,  # allow multiple selections
            className = 'six columns'
        ),
        # range slider for years
        dcc.RangeSlider(min = gdp_long["Year"].min(), 
                        max = gdp_long["Year"].max(), 
                        step = 1,
                        marks = {year: str(year) for year in range(gdp_long['Year'].min(), gdp_long['Year'].max() + 1, 100)}, # have every 100 years marked in the slider
                        value = [gdp_long['Year'].min(), gdp_long['Year'].max()], # initilaize so the slider automatically has 1800 to 2100 
                        id = 'years',
                        tooltip={"placement": "bottom", "always_visible": True},
                        className = 'six columns'
                        )
    ], className = 'row'),
    
    #display the graph
    dcc.Graph(id = 'graph')
])


# %%
## GRAPH ## 
# get the inputs from dropdown and slider
@app.callback(
    Output('graph', 'figure'),
    [Input('country', 'value'), # country input
     Input('years', 'value')]   # year input
)

# make the graph
def update_figure(selected_countries, selected_year):
   # filter the dataset so that it only includes selected years and countries
   filtered_gdp = gdp_long[
       (gdp_long['Year'] >= selected_year[0]) & 
       (gdp_long['Year'] <= selected_year[1]) &
       (gdp_long['country'].isin(selected_countries))
    ]

   # aggregate gdp by year
   total_gdp_by_year = filtered_gdp.groupby(['Year', 'country'])['gdpPercap'].sum().reset_index()

# make the line graph
   fig = px.line(
       total_gdp_by_year,
       x="Year", 
       y="gdpPercap",
       color="country",
       title= f'GDP for {selected_countries} from {selected_year[0]} to {selected_year[1]}',
       height = 550
    )

   fig.update_layout(
       yaxis_title = "Total GDP",
       xaxis_title = "Year"
)
   
   return fig


# run the app on a tab
if __name__ == '__main__':
    app.run_server(debug=True)
