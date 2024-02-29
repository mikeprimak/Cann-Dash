import pandas as pd
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

import dash_ag_grid as dag
import math
from dash import html, dcc, State
import plotly.express as px
from dash.dependencies import Input, Output
from dash import Dash, dash_table
from itertools import islice
import itertools

import string
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


import pandas as pd
import re
import numpy as np
from PIL import Image
from wordcloud import STOPWORDS, WordCloud


# Initialize the app - incorporate a Dash Mantine theme
# external_stylesheets = [dmc.theme.DEFAULT_COLORS]
external_stylesheets = [dbc.themes.BOOTSTRAP]
# app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


# server = app.server



# colors for wordcloud
def create_colormap(rgb_color=(197, 189, 104)):
    N = 256
    color = np.ones((N, 4))
    color[:, 0] = np.linspace(rgb_color[0] / 256, 1, N)  # R = 45
    color[:, 1] = np.linspace(rgb_color[1] / 256, 1, N)  # G = 132
    color[:, 2] = np.linspace(rgb_color[2] / 256, 1, N)  # B = 200
    cmap = ListedColormap(color)
    return cmap


cmap = create_colormap()

# Incorporate data
df = pd.read_csv("ocs_product_details.csv")


getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.rowIndex % 2 === 0",
            "style": {"backgroundColor": "#4A7B4C", "color": "white"},
        },
    ]
}

df_for_display = df[["Brand", "Product", "Price Per Gram", "THC %", "CBD %"]]

df['dates_only'] = pd.to_datetime(df['scrape_date'])
df['dates_only'] = df['dates_only'].dt.date
most_recent_date = df['dates_only'].max()

all_list = ['All']

grow_methods_df = df['grow_method'].str.lower().value_counts().reset_index()

plant_type_df = df['plant_type'].str.lower().value_counts().reset_index()



min_price = math.floor(df['Price Per Gram'].min())
max_price = math.ceil(df['Price Per Gram'].max())

min_thc = math.floor(df['THC %'].min())
max_thc = math.ceil(df['THC %'].max())

min_cbd = math.floor(df['CBD %'].min())
max_cbd = math.ceil(df['CBD %'].max())


print("max is ", max_price)
print("min is ", min_price)


print(grow_methods_df)

brand_names = df['Brand'].unique()
brand_names.sort()
total_num_brands = len(brand_names)
print("total:", total_num_brands)

options=[{'label':x , 'value':x} for x in brand_names]
options.insert(0, {'label': 'All', 'value': "All"})






# table = dag.AgGrid(
#     id="my-table",
#     className="ag-theme-alpine",
#     style={'background-color':'red', 'color':'blue'},
#     rowData=df_for_display.to_dict("records"),                                                          # **need it
#     columnDefs=[{"field": i} for i in df.columns],                                          # **need it
#
# )


#  test responsive wordcloud
#  test responsive wordcloud
#  test responsive wordcloud


# convert dataframe of product descriptions to one long string
# df = pd.read_csv("ocs_product_details.csv")

# descriptions = df['long_product_description']
# df_descriptions = descriptions.drop_duplicates()
# list_descriptions = df_descriptions.tolist()
# string_descriptions = ' '.join(list_descriptions)
# # print(string_descriptions)
#
# string_descriptions = re.sub(r"[^ a-zA-Z0-9]+",'',string_descriptions)
# # print(string_descriptions)
#
# # Read text
# text = string_descriptions
# stopwords = STOPWORDS
# stopwords = ["preroll"] + list(STOPWORDS)
#
# # mask = np.array(Image.open('smoke-cloud.png'))
#
# # wc = WordCloud(background_color = '#385c39', contour_width = 1,
# #      contour_color = 'white', colormap = 'pink_r', mask = mask, width = 1600, height = 1000, stopwords=stopwords)
#
# wc = WordCloud(background_color = '#385c39', colormap = 'pink_r', width = 1600, height = 1000, stopwords=stopwords)
#
# wc.generate(text)
# wc.to_file("assets/test-responsive.png")




#  end of responsive wordcloud
#  end of responsive wordcloud
#  end of responsive wordcloud







app.title = 'Cannabis Dashboard'

# App layout
app.layout = html.Div([

    # dbc.Row([
    #     dbc.Col([
    #         html.Br(),
    #         dcc.Graph(id="grow-method-graph", config={'displayModeBar': False}),
    #     ], lg=4),
    #     dbc.Col([
    #         html.Br(),
    #         dcc.Graph(id="plant-type-graph", config={'displayModeBar': False}),
    #     ], lg=4),
    #     dbc.Col([
    #         html.Br(),
    #         html.Img(src=r'assets/smoke-cloud-cannabis-descriptions.png', style={'height':'300px'}, alt='image'),
    #     ], lg=4),
    # ]),
    #

    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading-1",
                type="circle",
                children=html.Div(id="loading-output-1"),
                fullscreen=True,
                style={"background-color": "rgba(255, 255, 255, .7)"},
                color="#4A7B4C"),
            dmc.Title('Ontario Cannabis Products Market', size="h3"),
            html.Br(),
            html.Div(children="Selected Brands:", style={'height':'40px'}),
            dcc.Dropdown(
                        options,
                        ['All'],
                        multi=True,
                        maxHeight=200,
                        id="brand_dropdown",
                        className="brand_dropdown"
                    ),
            html.Br(),
            html.Div(id="selected_price_range", children="Price Range (per gram): $ ", style={'height':'40px'}),
            dcc.RangeSlider(
                min=df['Price Per Gram'].min(),
                max=df['Price Per Gram'].max(),
                value=[df['Price Per Gram'].min(), df['Price Per Gram'].max()],
                marks=None,
                id="mean",
            ),
            html.Br(),
            html.Div(id="selected_thc_range", children="THC Range: % ", style={'height':'40px'}),
            dcc.RangeSlider(
                min=df['THC %'].min(),
                max=df['THC %'].max(),
                value=[df['THC %'].min(), df['THC %'].max()],
                id="thc_range",
                marks=None,
            ),
            html.Br(),
            html.Div(id="selected_cbd_range", children="CBD Range: % ", style={'height':'40px'}),
            dcc.RangeSlider(
                min=df['CBD %'].min(),
                max=df['CBD %'].max(),
                value=[df['CBD %'].min(), df['CBD %'].max()],
                id="cbd_range",
                marks=None,
            ),

            html.Br(),
            html.Div(children="Product Types:", style={'height':'40px'}),
            dcc.RadioItems(['All', 'Dried Flower','Pre-Roll'], 'All', id="selected_product_types"),
            html.Button(id='submit-button-state', n_clicks=0, children='Apply Filters', className='apply-filters-button'),
        ], xs=12, lg=2, style={'background-color': '#385C39', "padding": "15px", "padding-left": "25px"}),

            dbc.Col([

                html.Br(),
                dbc.Row([
                    dbc.Col([

                        # html.Div(id="num_brands", children="No. Brands: "),
                        # html.Div(id="num_products", children="No. Products: "),
                        html.Div(children="Average Price Per Gram", style={'height': '30px', 'marginTop':'5px','font-family' : 'arial'}),
                        html.Div(style={'height': '180px', 'padding-top':'30px', 'text-align': 'center', 'background': '#4A7B4C', 'font-family' : 'arial'},
                                 children=[
                                    html.Div(id='avg_price_per_gram', style={'font-size': '50px', 'display': 'inline-block'}, children=''),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(id='num-brands-num-products', style={'font-size': '13px', 'display': 'inline-block'})
                                 ])


                    ], xs=12, lg=6, xl=3),
                    dbc.Col([

                        dcc.Graph(id="grow-method-graph", config={'displayModeBar': False}),
                    ], xs=12, lg=6, xl=3),
                    dbc.Col([

                        dcc.Graph(id="plant-type-graph", config={'displayModeBar': False}),
                    ], xs=12, lg=6, xl=3),

                    dbc.Col([

                        dcc.Graph(id="terpenes-graph", config={'displayModeBar': False}),
                    ], xs=12, lg=6, xl=3),

                ]),


                dbc.Row([
                    dbc.Col([

                        dcc.Graph(id="graph", config={'displayModeBar': False}),
                    ], xs=12, lg=4),
                    dbc.Col([

                        dcc.Graph(id="thc-graph", config={'displayModeBar': False}),
                    ], xs=12, lg=4),
                    dbc.Col([

                        dcc.Graph(id="cbd-graph", config={'displayModeBar': False}),
                    ], xs=12, lg=4),
                ]),


                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div(children="How Is This Cannabis Described By Producers?",
                                 style={'height': '40px', 'font-family': 'arial'}),
                        # html.Img(id="word_cloud_id", src=r'assets/test-responsive.png', style={'height': '300px'}, alt='image'),
                        dcc.Graph(id="word_cloud_id", config={'displayModeBar': False}),
                    ], xs=12, lg=6),
                    dbc.Col([
                        html.Div(children="Where Is Ontario Cannabis Grown?", style={'height': '40px', 'font-family' : 'arial'}),
                        dcc.Graph(id="map", config={'displayModeBar': False}),
                    ], xs=12, lg=6),
                ], style={'marginTop':'30px'}),


                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div(children="Filtered Product Table", style={'height': '40px', 'font-family' : 'arial'}),
                        html.Div(id="dash_table"),

                    ], lg=12),
                ], style={'marginTop':'30px'}),




            ], style={'padding-left':'20px', 'padding-right':'20px', 'background-color':'#4A7B4C'}, xs=12, lg=10),









    ]),





], style={'backgroundColor':'#4A7B4C'},  className="container-class")


@app.callback(
    Output("graph", "figure"),
    Output("num-brands-num-products", "children"),
    # Output("num_brands", "children"),
    # Output("num_products", "children"),
    Output("avg_price_per_gram", "children"),
    # Output("table", "data"),
    Output("dash_table", "children"),


    Output("thc-graph", "figure"),
    Output("cbd-graph", "figure"),
    Output("brand_dropdown", "value"),
    Output("grow-method-graph", "figure"),
    Output("plant-type-graph", "figure"),
    Output("map", "figure"),
    Output("selected_price_range", "children"),
    Output("selected_thc_range", "children"),
    Output("selected_cbd_range", "children"),
    Output("word_cloud_id", "figure"),
    Output("loading-output-1", "children"),
    Output("terpenes-graph", "figure"),
    Input('submit-button-state', 'n_clicks'),
    State("thc_range", "value"),
    State("cbd_range", "value"),
    State("mean", "value"),
    State("brand_dropdown", "value"),
    State("selected_product_types", "value"))
def display_color(n_clicks, thc_range, cbd_range, mean, brand_dropdown_list, selected_product_types):
    data = df[(df['Price Per Gram']>=mean[0]) & (df['Price Per Gram']<=mean[1])]
    data = data[(data['THC %'] >= thc_range[0]) & (data['THC %'] <= thc_range[1])]
    data = data[(data['CBD %'] >= cbd_range[0]) & (data['CBD %'] <= cbd_range[1])]

    print(selected_product_types)
    if selected_product_types == "All":
        print("IT IS ALL")
        data = data
    else:
        data = data[(data['actual_product_type'] == selected_product_types)]
        print("NOT ALL AT ALL")
        print("IT IS ", selected_product_types )


    if brand_dropdown_list == all_list:

        data = data
        # num_brands = total_num_brands
    else:
        if "All" in brand_dropdown_list:
            if brand_dropdown_list[-1] == "All":
                brand_dropdown_list = ['All']
                # num_brands = total_num_brands

            else:
                brand_dropdown_list.remove("All")
                print("removing all")
                data = data[data['Brand'].isin(brand_dropdown_list)]
                # num_brands = len(brand_dropdown_list)

            # check if 'all' is last item, in which case remove all the other values instead of 'all'. maybe do this above.
        else:
            data = data[data['Brand'].isin(brand_dropdown_list)]
            # num_brands = len(brand_dropdown_list)


    filtered_brand_names = data['Brand'].unique()
    filtered_brand_names.sort()
    filtered_num_brands = len(filtered_brand_names)
    num_brands = filtered_num_brands
    print("NUM BRANDS IS:", num_brands)



    loading_spinner = ""

    # linked_product = []
    # thc_range_strings = []
    # cbd_range_strings = []
    two_decimal_price_per_gram = []

    # for i in data.index:
    #     # print (data['Product'][i], data['Product_URL'][i])
    #     prod_name = data['Product'][i]
    #     prod_url = data['Product_URL'][i]
    #
    #     # data['Price Per Gram'][i] = float(format(data['Price Per Gram'][i], '.2f'))
    #
    #     thc_max = round(data['thc_percent_high_end_of_range'][i])
    #     thc_min = round(data['thc_percent_low_end_of_range'][i])
    #     thc_range_string = str(thc_min) + " - " + str(thc_max) + "%"
    #
    #     cbd_max = round(data['cbd_high_end_of_range'][i])
    #     cbd_min = round(data['cbd_low_end_of_range'][i])
    #     cbd_range_string = str(cbd_min) + " - " + str(cbd_max) + "%"
    #
    #     thc_range_strings.append(thc_range_string)
    #
    #     cbd_range_strings.append(cbd_range_string)
    #
    #
    #     linked_product.append('[' + prod_name + '](' + prod_url + ')')

    # print(linked_product)

    # data.Product = linked_product
    #
    # data = data.assign(thc_range=thc_range_strings)
    # data = data.assign(cbd_range=cbd_range_strings)
    # print(data)
    #

    columnDefs = [
        {'field': 'Brand', 'color':'blue'},
        # {'field': 'Product', 'headerName': 'Product Name', 'cellRenderer':'markdown'},
        {'field': 'product_name_link_markdown', 'headerName': 'Product', 'cellRenderer': 'markdown'},
        {'field': 'Price Per Gram', 'headerName': 'Price Per Gram ($)', 'filter': False},
        {'field': 'actual_product_type', 'headerName': 'Product Type'},
        {'field': 'plant_type', 'headerName': 'Plant Type'},
        {'field': 'THC %', 'headerName': 'THC %', 'filter': False},
        {'field': 'CBD %', 'headerName': 'CBD %', 'filter': False},
    ]

    grid = dag.AgGrid(

        className="ag-theme-alpine custom-grid-class",
        rowData=data.to_dict("records"),
        rowStyle={"backgroundColor": "#839D58", "color": "white"},
        style={"height": 550},
        getRowStyle=getRowStyle,
        # columnDefs=[{"field": i} for i in df.columns],
        columnDefs=columnDefs,
        columnSize="sizeToFit",
        defaultColDef={"resizable": True, "sortable": True, "filter": True},

    )


    # df_for_display = data[["Brand", "Product", "Price Per Gram", "THC %", "CBD %"]].to_dict('records')

    selected_price_range = "Price Range (/g): $ " + str(format(mean[0], '.2f')) + " - $ " + str(format(mean[1], '.2f'))

    selected_thc_range = "THC Range: % " + str(format(thc_range[0], '.0f')) + " - % " + str(
        format(thc_range[1], '.0f'))

    selected_cbd_range = "CBD Range: % " + str(format(cbd_range[0], '.0f')) + " - % " + str(
        format(cbd_range[1], '.0f'))

    fig = px.histogram(data, range_x=[min_price,max_price], x="Price Per Gram", height=200, labels={
                     "Price Per Gram": "Price Per Gram ($)"})

    # maintains bin width as 1.
    fig.update_traces(xbins=dict(size=1),
                      marker_color='#C5BD68'
                      )
    fig.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="No. Products",
        font_family="Arial",
        font_color="white",
        title={'text': 'How Many Products At Each Price Point?', 'font': {'size': 14}},
        title_font_family="Arial",
        bargap=0.2)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    thc_fig = px.histogram(data, range_x=[min_thc, max_thc], x="THC %", height=200)

    thc_fig.update_traces(xbins=dict(size=1),
                      marker_color='#C5BD68'
                      )
    thc_fig.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="No. Products",
        font_family="Arial",
        font_color="white",

        title={'text': 'What THC % Is Most Common?', 'font': {'size': 14}},
        title_font_family="Arial",
        bargap=0.2)
    thc_fig.update_xaxes(showgrid=False)
    thc_fig.update_yaxes(showgrid=False)

    cbd_fig = px.histogram(data, range_x=[min_cbd, max_cbd], x="CBD %", height=200)
    cbd_fig.update_traces(xbins=dict(size=1),
                          marker_color='#C5BD68'
                          )
    cbd_fig.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="No. Products",
        font_family="Arial",
        font_color="white",
        title_font_family="Arial",

        title={'text': 'What CBD % Is Most Common?', 'font': {'size': 14}},
        bargap=0.2)
    cbd_fig.update_xaxes(showgrid=False)
    cbd_fig.update_yaxes(showgrid=False)

    grow_methods_df = data['grow_method'].str.lower().value_counts().reset_index()


    grow_method_fig = px.pie(grow_methods_df, height=200, values="count", names="grow_method", hole=.3,
                             color_discrete_sequence=["#839D58", "#C5BD68", '#FFDB83', '#D1A44F', '#97711B'])

    grow_method_fig.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Arial",
        font_color="white",
        title={'text': 'Grown Indoor or Outdoor?', 'font': {'size': 14}},
        title_font_family="Arial")

    plant_type_df = data['plant_type'].str.lower().value_counts().reset_index()


    plant_type_fig = px.pie(plant_type_df, height=200, hole=.3,
                             color_discrete_sequence=["#839D58", "#C5BD68", '#FFDB83', '#D1A44F', '#97711B'],
                             values="count", names="plant_type")
    plant_type_fig.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Arial",
        font_color="white",
        title={'text': 'Indica or Sativa?', 'font': {'size': 14}},
        title_font_family="Arial")




    # MAP

    token = "pk.eyJ1IjoibWljaGFlbHByaW1hayIsImEiOiJjbHF4NXRnbTcwYmN6MmtwZ3BpZ2w5MjM5In0.H2fkGMFOGRos_9vnLPBgPA"

    map_fig = px.scatter_mapbox(data, title="Where Is The Cannabis Grown?", lat="latitude", lon="longitude",
                        color_discrete_sequence=["#C5BD68"], zoom=2, height=300, hover_data= {
                            "Brand": True,
                            "growing_region": True,
                            "latitude": False,
                            "longitude": False
                        },)


    map_fig.update_layout(mapbox = dict(
        accesstoken="pk.eyJ1IjoibWljaGFlbHByaW1hayIsImEiOiJjbHF4NXRnbTcwYmN6MmtwZ3BpZ2w5MjM5In0.H2fkGMFOGRos_9vnLPBgPA",
        style='mapbox://styles/michaelprimak/clqx47i9d00ob01qr6zdb241o'
    ),)

    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    num_brands_and_products_value = "Average price across " + str(data.count()['Product_URL']) + " products ("+ str(num_brands) + " Brands)."

    # num_brands_value = "No. Brands: " + str(brand_dropdown_list)
    #
    # # num_brands_value = "No. Brands: " + str(data['Brand'].nunique())
    # num_products_value = "No. Products: " + str(data.count()['Product_URL'])

    avg_price_per_gram = "$" + str(round(data.mean(axis='index', numeric_only=True)['Price Per Gram'], 2))

    #  start of wordcloud callback
    #  start of wordcloud callback
    #  start of wordcloud callback


    #
    descriptions = data['long_product_description']
    df_descriptions = descriptions.drop_duplicates()
    list_descriptions = df_descriptions.tolist()
    string_descriptions = ' '.join(list_descriptions)
    # print(string_descriptions)

    # letters = string.ascii_lowercase
    # print("the random string is ")
    # rand_string = ''.join(random.choice(letters) for i in range(10))
    #
    # rand_filename = "assets/wordcloud_" + rand_string + ".png"
    # print(rand_filename)


    string_descriptions = re.sub(r"[^ a-zA-Z0-9]+", '', string_descriptions)
    # print(string_descriptions)

    # stopwords = STOPWORDS
    stopwords = ["preroll"] + list(STOPWORDS)





    wc = WordCloud(background_color='#4A7B4C', colormap=cmap, width=2000, height=1000, stopwords=stopwords)

    wc.generate(string_descriptions)

    new_wordcloud_file = px.imshow(wc, height=300)
    new_wordcloud_file.update_layout(hovermode=False)

    new_wordcloud_file.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    new_wordcloud_file.update_xaxes(showticklabels=False, zerolinecolor = 'rgba(0,0,0,0)')
    new_wordcloud_file.update_yaxes(showticklabels=False, zerolinecolor = 'rgba(0,0,0,0)')



    #
    # wc.to_file(rand_filename) # running this line reloads the page over and over. how to not.
    #
    # new_wordcloud_file = rand_filename



    #  end of wordcloud callback
    #  end of wordcloud callback
    #  end of wordcloud callback


    ############### terpene counter #################
    #  get dataframe of all terpenes values
    terpenes = data['terpenes']

    # convert to list
    list_terpenes = terpenes.tolist()

    # convert to string
    string_terpenes = ' '.join(str(x) for x in list_terpenes)
    string_terpenes = re.sub(r"[^ a-zA-Z0-9]+", '', string_terpenes)

    # remove words that are not terpene names
    remove_list = ["May", "Vary", "Terpenes"]
    for sub in remove_list:
        string_terpenes = string_terpenes.replace(' ' + sub + ' ', ' ')

    # remove nan values
    new_string_terpenes = string_terpenes.replace("nan", " ")

    # count how many times each word occurs in the string, and format resut as list.
    def word_count(str):
        # Create an empty dictionary named 'counts' to store word frequencies.
        counts = dict()

        # Split the input string 'str' into a list of words using spaces as separators and store it in the 'words' list.
        words = str.split()

        # Iterate through each word in the 'words' list.
        for word in words:
            # Check if the word is already in the 'counts' dictionary.
            if word in counts:
                # If the word is already in the dictionary, increment its frequency by 1.
                counts[word] += 1
            else:
                # If the word is not in the dictionary, add it to the dictionary with a frequency of 1.
                counts[word] = 1

        # Return the 'counts' dictionary, which contains word frequencies.
        return counts

    # Call the word_count function with an input sentence and print the results.
    dict_of_terpenes = (word_count(new_string_terpenes))

    # sort list by value (number of times word occurs)
    sorted_dict_of_terpenes = sorted(dict_of_terpenes.items(), key=lambda x: x[1], reverse=True)
    converted_dict = dict(sorted_dict_of_terpenes)

    terpene_dict = dict(itertools.islice(converted_dict.items(), 5))
    # remove words that occur fewer than 50 times
    # terpene_dict = {key: val for key, val in converted_dict.items() if val >= 25}

    print(terpene_dict)

    terpene_df = pd.DataFrame(terpene_dict.items(), columns=['Terpene', 'Occurrences'])

    print(terpene_df)


    terpenes_graph = px.pie(terpene_df, height=200, hole=.3,
                             color_discrete_sequence=["#839D58", "#C5BD68", '#FFDB83', '#D1A44F', '#97711B'],
                             values="Occurrences", names="Terpene")
    terpenes_graph.update_layout(
        margin=dict(l=45, r=45, t=55, b=45),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Arial",
        font_color="white",
        title={'text': 'Most Common Terpenes?', 'font': {'size': 14}},
        title_font_family="Arial")



    return (fig, num_brands_and_products_value, avg_price_per_gram,
            grid, thc_fig, cbd_fig, brand_dropdown_list, grow_method_fig,
            plant_type_fig, map_fig, selected_price_range, selected_thc_range, selected_cbd_range,
            new_wordcloud_file, loading_spinner, terpenes_graph

            )




# Run the App
if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=False)


