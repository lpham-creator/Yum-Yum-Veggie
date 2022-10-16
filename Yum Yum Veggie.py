#!/usr/bin/env python
# coding: utf-8

# In[475]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import Bokeh packages for interactive plots
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper
from bokeh.tile_providers import OSM
from bokeh.palettes import Category20b, Category20c, Spectral, Magma, Inferno, Plasma, Viridis, Cividis, Purples
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show 
from bokeh.tile_providers import get_provider, Vendors 
tile_provider = get_provider(Vendors.OSM)
from bokeh.layouts import column
from bokeh.models import Slider
output_notebook()


# In[476]:


vege = pd.read_csv("/Users/phamlethuylinh/Desktop/vege.csv")
vege.info()


# In[477]:


print(vege.priceRangeMin)


# In[478]:


features = ["priceRangeMin", "priceRangeMax"]
vege[features].boxplot(figsize=(10, 4));


# In[479]:


vege = vege.copy()[['id', "address","city", "cuisines", "postalCode", "priceRangeMin", "priceRangeMax",
                         'latitude', 'longitude', "categories", "province"]]
vege.info()


# In[480]:


vege = vege.drop_duplicates(subset=['id'])


# In[481]:


vege.head()


# In[482]:


cuisines = vege['cuisines'].value_counts()


# In[483]:


zipcode = pd.read_csv('/Users/phamlethuylinh/Desktop/14zpallagi.csv',
                      usecols=['STATE', 'zipcode'], dtype={'zipcode': 'str'})

zipcode.head()


# In[484]:


zipcode = zipcode.drop_duplicates(['zipcode'])
zipcode.head()


# In[485]:


vege_merge = pd.merge(vege, zipcode, left_on='province', right_on='STATE', how='left')
vege_merge.info()


# In[486]:


# count the restaurants by State
counts = vege_merge.province.value_counts()


# merge
vege_clean = pd.merge(vege_merge, counts.to_frame(), 
                       left_on='province', right_index=True, how='left')
vege_clean.head()

#drop unused columns and NAs
vege_clean = vege_clean.drop(['id', 'province_y', "province_x"], axis=1).dropna()
vege_clean.priceRangeMax = vege_clean.priceRangeMax.dropna(axis = 0, how = "any", inplace=False)

vege_clean['dot_size'] = vege_clean.priceRangeMax**.85


# In[487]:


#Because latitude, longitude and elevation is a 3D coordinate system, plus that a map we are about to use is 2D, we need to project 3D coordinates system (latitude and longitude) on 2D coordinate system (x and y) for drawing data on a map.


# In[488]:


import math

def lgn2x(a):
    return a * (math.pi/180.0) * 6378137

def lat2y(a):
    return math.log(math.tan(a * (math.pi/180.0)/2 + math.pi/4)) * 6378137


# In[489]:


vege_clean.head()


# In[490]:


vege_clean['x'] = vege_clean.longitude.apply(lambda row: lgn2x(row))
vege_clean['y'] = vege_clean.latitude.apply(lambda row: lat2y(row))

# drop unused columns
vege_clean = vege_clean.drop(['latitude', 'longitude'], axis=1)
vege_clean.info()


# In[491]:


vege_map = (vege_clean.sort_values(['priceRangeMax'], ascending=[0])).drop_duplicates(subset = ["address"])


# In[492]:


vege_map.info()


# In[493]:


cds = ColumnDataSource(vege_map)


# In[494]:


hover = HoverTool(tooltips=[('City', '@city'),
                            ('Address', '@address'),
                            ('Cuisine', '@cuisines'),
                           ("Max_Price", '@priceRangeMax')],
                  mode='mouse')


# In[495]:


# UPPER FIGURE
# initialize a figure
up = figure(title='Location of Vegetarian Restaurants in US',
           plot_width=1000, plot_height=600,
           x_axis_location=None, y_axis_location=None, 
           tools=['pan', 'wheel_zoom', 'tap', 'reset', 'crosshair',"zoom_in","zoom_out", hover])


# In[496]:


up.add_tile(tile_provider)


# In[497]:


mapper = CategoricalColorMapper(factors=vege_map.STATE.unique(), 
                                palette=Inferno[4]+Category20b[20]+Purples[9])


# In[498]:


scatter = up.circle('x', 'y', source=cds, size= "dot_size",
                    color={'field': 'STATE','transform': mapper}, alpha=.5,
                    selection_color='black',
                    nonselection_fill_alpha=.1,
                    nonselection_fill_color='gray',)


# In[499]:


vege.head()


# In[501]:


p = gridplot([[up]], toolbar_location='left')

show(p)


# In[58]:


#2.DATA VISUALIZATIONS


# In[ ]:


#2.1. Price ranges in states


# In[472]:


plt.figure(figsize=(13,6))

g= sns.barplot(x=vege_map.STATE.unique(), y=vege_map.STATE.value_counts(), palette = Inferno[4]+Category20b[11]+Purples[9]).set(title='Number of Vegan/Vegetarian Restaurants in Each State', xlabel = "States", ylabel = "Count")
plt.savefig(title, dpi=200)
plt.show()


# In[109]:


import seaborn as sns
sns.set()

plt.figure(figsize=(13,6))

sns.scatterplot(x=vege['STATE'], y=vege['priceRangeMax'],
                hue=vege['primaryCategories'], sizes=(20,600))

title = 'Vegetarian Restaurants Scatterplot'
plt.title(title)

plt.savefig(title, dpi=200)
plt.show()


# In[ ]:




