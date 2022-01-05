import geopandas as gpd
import pandas as pd
import json
import os
from bokeh.io import output_notebook, show, output_file
# May not need save
from bokeh.plotting import figure, save
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
# May not need export_png
from bokeh.io import curdoc, output_notebook, export_png
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.io.export import get_screenshot_as_png
#shapefile = '/home/lexichuxuanl/chicagos-response-to-the-pandemic/map/Neighborhoods/geo_export_a131bb4a-42f9-4af9-bd33-aedec365203f.shp'
shapefile = '/home/jwnicoll/chicagos-response-to-the-pandemic/ui/Neighborhoods/geo_export_a131bb4a-42f9-4af9-bd33-aedec365203f.shp'
datafile = '//home/lexichuxuanl/chicagos-response-to-the-pandemic/data_files/COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv'


def create_map(directory, shapefile):
    
    datafiles = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            datafiles.append(pd.read_csv(filename))
    
    gdf = gpd.read_file(shapefile)[["zip","geometry"]]
    
    maps = []
    
    for datafile in datafiles:
        df = pd.read_csv(datafile)[:3]
        data_title = df.columns[2]
        #need to make sure that all datafiles are organized in this order
        df.columns = ['zip_code', 'week', 'data_of_interest']
        start_wk = df['week'].min()
        end_wk = df['week'].max()

        json_data = get_json_data(1)    
        geosource = GeoJSONDataSource(geojson = json_data)
        #choose the number of colors depending on number of unique values
        distinct_val = len(pd.unique(df['data_of_interest']))
        palette = brewer['YlOrRd'][distinct_val]
        #reverse the palette so that deepest color represents larger value
        palette = palette[::-1]
        #set the color mapper values corresponding to the min and max of dataset
        min_val = df['data_of_interest'].min()
        max_val = df['data_of_interest'].max()
        color_mapper = LinearColorMapper(palette = palette, 
                                        low = min_val, 
                                        high = max_val,
                                        nan_color = '#d9d9d9')
        #Define custom tick labels for color bar.
        num_labels = (max_val - min_val)/distinct_val
        tick_labels = {}
        for i in range(num_labels):
            tick_labels[str(i)] = str(i) + '%'
        
        #Add hover tool
        hover = HoverTool(tooltips = [ ('Zip code','@zip'),
                                       (data_title, '@data_of_interest')])
        #Create color bar. 
        color_bar = ColorBar(color_mapper=color_mapper, 
                            label_standoff=8,
                            width = 500, 
                            height = 20,
                            border_line_color=None,
                            location = (0,0), 
                            orientation = 'horizontal', 
                            major_label_overrides = tick_labels)
        #Create figure object.
        plot_title = data_title + 'by neighborhood, week 1'
        p = figure(title = plot_title, 
                   plot_height = 600, 
                   plot_width = 950, 
                   toolbar_location = None,
                   tools = [hover])
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        #Add patch renderer to figure. 
        p.patches('xs','ys', 
                 source = geosource,
                 fill_color = {'field' :'data_of_interest', 
                               'transform' : color_mapper},
                 line_color = 'black', 
                 line_width = 0.25, 
                 fill_alpha = 1)
        
        #Specify figure layout.
        p.add_layout(color_bar, 'below')

        # Make a slider object: slider 
        slider = Slider(title = 'Week',
                        start = start_wk, 
                        end = end_wk, 
                        step = 1, 
                        value = start_wk)
        slider.on_change('value', update_plot)
        # Make a column layout of widgetbox(slider) and plot, and add it to the current document
        layout = column(p,widgetbox(slider))
        curdoc().add_root(layout)

        maps.apped(p)


def get_json_data(selected_week):
    
    wk = selected_week
    df_wk = df[df['week'] == wk]
    merged = gdf.merge(df_wk, left_on = 'zip', right_on = 'zip_code', how = 'left')
    merged.fillna('No data', inplace = True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    
    return json_data

def update_plot(attr, old, new, data_title):
    wk = slider.value
    new_data = json_data(wk)
    geosource.geojson = new_data
    p.title.text = data_title + 'by neighborhood, week' + str(wk)
    
# shapefile is a global variable, so I don't think it has to get passed in as an argument
def create_map_from_series(series, filename):
    '''
    Attempt to recreate function above, but just from series
    '''
    gdf = gpd.read_file(shapefile)[["zip","geometry"]]

    maps = []

    series_json = json.loads(series.to_json())
    json_data = json.dumps(series_json)
    geosource = GeoJSONDataSource(geojson = json_data)
    #choose the number of colors depending on number of unique values
    distinct_val = len(pd.unique(series))
    if distinct_val < 3:
        palette_val = 3
    elif distinct_val > 9:
        palette_val = 9
    else:
        palette_val = distinct_val
    palette = brewer['YlOrRd'][palette_val]
    #reverse the palette so that deepest color represents larger value
    palette = palette[::-1]
    #set the color mapper values corresponding to the min and max of dataset
    min_val = series.min()
    max_val = series.max()
    color_mapper = LinearColorMapper(palette = palette, 
                                    low = min_val, 
                                    high = max_val,
                                    nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    num_labels = int((max_val - min_val)/distinct_val)
    tick_labels = {}
    for i in range(num_labels):
        tick_labels[str(i)] = str(i) + '%'
    # I suspect this will require debugging
    #Add hover tool
    hover = HoverTool(tooltips = [ ('Zip code','@zip'),
                                   (series.name, '@series.name')])#(data_title, '@data_of_interest')])
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, 
                        label_standoff=8,
                        width = 500, 
                        height = 20,
                        border_line_color=None,
                        location = (0,0), 
                        orientation = 'horizontal', 
                        major_label_overrides = tick_labels)
    #Create figure object.
    plot_title = series.name + 'by zip code'
    p = figure(title = plot_title, 
               plot_height = 600, 
               plot_width = 950, 
               toolbar_location = None,
               tools = [hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure. 
    p.patches('xs','ys', 
             source = geosource,
             fill_color = {'field' :'data_of_interest', 
                           'transform' : color_mapper},
             line_color = 'black', 
             line_width = 0.25, 
             fill_alpha = 1)
        
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    #show(p)
    #save(p,filename='try.html', resources=inline)
    image = get_screenshot_as_png(p)
    image.save('/home/jwnicoll/chicagos-response-to-the-pandemic/ui/static/'+filename)
    #export_png(p, filename="/home/jwnicoll/chicagos-response-to-the-pandemic/ui/static/" +filename)
    #save(p)