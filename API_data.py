#!/usr/bin/env python
# coding: utf-8

# In[1]:


from yelpapi import YelpAPI


# In[2]:


import pandas as pd
import requests
import json
from config import API_Key 
# from config import bea_api


# In[3]:


from pprint import pprint


# In[4]:


yelp_api = YelpAPI(API_Key)


# In[91]:


bea_url = 'https://apps.bea.gov/api/data'
bea_api = '0BEDA572-87F5-46AB-8614-4949AE2FE5B8'


# In[11]:


bea_final_url = f'{bea_url}?&UserID={bea_api}&method=GetData&Datasetname=Regional&TableName=CAINC1&LineCode=3&GeoFIPS=COUNTY&Year=2014&ResultFormat=JSON'


# In[6]:


bea_list_url=f'https://apps.bea.gov/api/data?&UserID={bea_api}&method=GETDATASETLIST&'


# In[7]:


bea_list = requests.get(bea_list_url).json()


# In[92]:


bea_data = requests.get(bea_final_url).json()


# In[93]:


data = bea_data['BEAAPI']['Results']['Data']


# In[94]:


PCI = pd.DataFrame(data)


# In[96]:


PCI.drop(['Code', 'GeoFips', 'CL_UNIT', 'UNIT_MULT', 'NoteRef'], axis = 1, inplace=True)


# In[97]:


PCI.to_csv("PCI.csv")


# In[24]:


PCI = pd.read_csv('PCI.csv')


# In[25]:


PCI.loc[PCI['GeoName'] == 'Denver, CO']


# In[26]:


pop_html = pd.read_html('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')


# In[27]:


pop_db = pop_html[4]


# In[28]:


pop_db.drop(['Location', '2016 population density', '2016 population density.1', '2018rank'], axis = 1, inplace=True)


# In[29]:


pop_db = pop_db.rename(columns={'State[c]':'State'})


# In[30]:


x = 'New York'


# In[31]:


x.partition('[')


# In[32]:


pop_db['City'] = pop_db['City'].apply(lambda x: x.partition('[')[0])


# In[33]:


pop_db.to_csv('pop_db.csv')


# In[156]:


PCI['GeoName'].p


# In[35]:


x = PCI['GeoName'][0]


# In[36]:


x.partition(',')[0]


# In[37]:


PCI['City'] = PCI['GeoName'].apply(lambda x: x.partition(',')[0])
PCI['State'] = PCI['GeoName'].apply(lambda x: x.partition(',')[2])


# In[38]:


PCI.drop(['GeoName', 'TimePeriod'], axis=1, inplace=True)


# In[40]:


st_abbr = pd.read_csv('st_abbr.csv')


# In[41]:


st_abbr.drop(['Abbrev'], axis=1, inplace=True)


# In[42]:


population = st_abbr.merge(pop_db, on='State')


# In[43]:


population.drop(['State'], axis=1, inplace=True)


# In[44]:


population = population.rename(columns={'Code':'State'})


# In[46]:


final_db = population.merge(PCI, on='City')


# In[48]:


#delete empty spaces before and after State abbr
PCI['State'] = PCI['State'].apply(lambda x: x.strip())


# In[50]:


final_db = population.merge(PCI, on=['City', 'State'])


# In[53]:


final_db.to_csv('merged_data.csv')


# In[5]:


final_db = pd.read_csv("merged_data.csv")


# In[34]:


yelp_list_st = []
yelp_list_city = []
for row in final_db.iterrows():
    yelp_list_city.append(row[1][2])
    yelp_list_st.append(row[1][1])

# results_mexi = yelp_api.search_query(term='massage', location='denver, co')


# In[8]:


terms = ['spas', 'privateschools', 'restaurants']
terms[0]


# In[9]:


import time 


# In[ ]:


for i in range(0,19):
    if i == 0:
        offset = 0
    else: 
        offset = offset + 50
    print(offset)


# In[120]:


x = round(test['total']/50)
x


# In[155]:


try: 
    ag
    print('try')
except:
    ag= {}
    print('except')
    
finally:
    print('finally')


# In[156]:


#loop through results and create dataframe for desired info
# def test(location, terms):
#     print(location , terms)

def getresults(location, terms):
    
    time.sleep(5)
    name = []
    cat = []
    price = []
    rating = []
    review = []
    state = []
    city = []
    bus_Type = []
    
    try:
        results = yelp_api.search_query(term=terms, location=location, offset=0)
        time.sleep(2)
    except: 
        print(f'no listing for {location} and {terms}')
        dict1 = {}
        return dict1
     
    #loop through creating offsets of 50 for each request     
    offset = 0
    x = round(results['total']/50) #calculate how many offset calls to make
    for i in range(0,x):
        if i == 0:
            offset = 0
        else: 
            offset = offset + 50 #increase each offset by 50 for each iteration
        
        try:
            results = yelp_api.search_query(term=terms, location=location, offset=offset) 
            time.sleep(3)
            
            #get results and append to list
            for rest in results['businesses']:
                name.append(rest['name'])
                cat.append(rest['categories'][0]['title'])
                city.append(location.split(',')[1])
                state.append(location.split(',')[0])
                bus_Type.append(terms)

                try:
                    price.append(f"{rest['price']}")
                except: 
                    price.append('0')
                try:
                    rating.append(rest['rating'])
                except: 
                    rating.append('0')  
                try:                
                    review.append(rest['review_count'])
                except:
                    review.append('0')
            
            
            dict1 = {'State': state,
                'City': city,
                'name': name,
                'cat': cat,
                'price': price,
                'rating': rating, 
                'review': review}
                                 
        except: 
            print(f'error reached at {location} and {terms} offset {offset}')
            try: 
                dict1
            except:
                dict1 = {}
            finally:
                return dict1
    try:                             
        return dict1                        
    except UnboundLocalError:
        dict1={}
        return dict1


# In[300]:


location.split(',')[0]


# In[171]:


resulttest = []

test_city = ['tuscaloosa, al']
test_term = ['spa']
for x in range(0, len(test_term)):
    for i in range(0, len(test_city)):
        result = getresults(test_city[i], test_term[x])
        resulttest.append(result)
        


# In[159]:


#main loop to call query function
resultx = []
for x in range(0, len(terms)):
    for i in range(0, len(yelp_list_ab)):
        location = f'{yelp_list_city[i].lower()}, {yelp_list_st[i].lower()}'
        result = getresults(location, terms[x])
        resultx.append(result)
        
        


# In[105]:


new_list=['worcester, ma']


# In[121]:


#loop and query 
resulty = []
result = []
new_city_list = yelp_list_city[26:49]
new_state_list = yelp_list_st[26:49]
for i in range(0, len(new_city_list)):
    location = f'{new_city_list[i].lower()}, {new_state_list[i].lower()}'
    result = getresults(location, 'spa')
    print('success')
    resulty.append(result)


# In[167]:


b = pd.DataFrame(resultx[0])
for i in range(1, len(resultx)):
    try:
        c = pd.DataFrame(resultx[i])
        b = b.append(c)
    except ValueError:
        print(f'error at {i}')


# In[168]:


b


# In[27]:


b = pd.DataFrame(resultx[0])
for i in range(1, len(resultx)):
    c = pd.DataFrame(resultx[i])
    b = b.append(c)


# In[61]:


b.loc[b['name'] == 'La Peau Spa']


# In[173]:


b.to_csv('bigdata.csv')


# In[175]:


b = b.reset_index(drop=True)


# In[242]:


pd.set_option('max_rows', 100)


# In[177]:


b = b.rename(columns={'State':'City', 'City':'State'})


# In[184]:


City_list = b['City'].unique()


# In[239]:


d = b.sample(frac=.1)
 


# In[230]:


d['price'] = d['price'].apply(lambda x: 1 if (x == '$')


# In[241]:


d['price']=d['price'].apply(lambda x: 1 if (x == "$") else x)
d['price']=d['price'].apply(lambda x: 2 if (x == "$$") else x)
d['price']=d['price'].apply(lambda x: 3 if (x == "$$$") else x)
d['price']==d['price'].apply(lambda x: 4 if (x == "$$$$") else x)


# In[196]:


for p in d['price']:
    if p == "$":
        p = 1
    

