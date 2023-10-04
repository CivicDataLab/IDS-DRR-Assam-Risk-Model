import pandas as pd
import os
import re
import dateutil.parser

# input_df - after the scraper code is run
input_df = pd.read_csv(os.getcwd()+'/Sources/TENDERS/data/2023aprmerged.csv')

# De-Duplication (Change the logic once the time of scraping is added in the input_df)
input_df = input_df.drop_duplicates()
tender_ids = input_df["Tender ID"]
duplicates_df = input_df[tender_ids.isin(tender_ids[tender_ids.duplicated()])].sort_values("Tender ID")
input_df = input_df.drop(duplicates_df[duplicates_df['No of Bids Received'].isnull()].index)
input_df.reset_index(drop=True, inplace=True)
deduped_df = input_df.drop_duplicates(subset=['Tender ID'],keep='last')
deduped_df.to_csv(os.getcwd()+'/Sources/TENDERS/data/deduped_master_tender_list.csv', encoding='utf-8')

# Identify flood related tenders using keywords
def populate_keyword_dict(keyword_list): 
    keywords_dict = {}
    for keyword in keyword_list:
        keywords_dict[keyword] = 0
    return keywords_dict

def flood_filter(row):
    '''
    :param row: row of the dataframe that contains tender title, work description
    
    :return: Tuple of (is_flood_tender, positive_kw_dict, negative_kw_dict) for every row
    '''
    positive_keywords_dict = populate_keyword_dict(POSITIVE_KEYWORDS)
    negative_keywords_dict = populate_keyword_dict(NEGATIVE_KEYWORDS)
    tender_slug = str(row['tender_externalreference']) + ' ' + str(row['tender_title']) + ' ' + str(row['Work Description'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    is_flood_tender = False
    for keyword in POSITIVE_KEYWORDS:
        keyword_count = len(re.findall(r"\b%s\b" % keyword.lower(), tender_slug.lower()))
        positive_keywords_dict[keyword] = keyword_count
        if keyword_count > 0:
            is_flood_tender = True
            
    for keyword in NEGATIVE_KEYWORDS:
        keyword_count = len(re.findall(r"\b%s\b" % keyword.lower(), tender_slug.lower()))
        negative_keywords_dict[keyword] = keyword_count
        if keyword_count > 0:
            is_flood_tender = False
           
    return str(is_flood_tender), str(positive_keywords_dict), str(negative_keywords_dict)

#Flood Keywords
global POSITIVE_KEYWORDS
POSITIVE_KEYWORDS = ['Flood', 'Embankment', 'embkt', 'Relief', 'Erosion', 'SDRF', 'Inundation', 'Hydrology',
                   'Silt', 'Siltation', 'Bund', 'Trench', 'Breach', 'Culvert', 'Sluice', 'Dyke',
                   'Storm water drain','Emergency','Immediate', 'IM', 'AE','A E', 'AAPDA MITRA']
global NEGATIVE_KEYWORDS
NEGATIVE_KEYWORDS = ['Floodlight', 'Flood Light','GAS', 'FIFA', 'pipe','pipes', 'covid']

flood_filter_tuples = deduped_df.apply(flood_filter,axis=1)
deduped_df.loc[:,'is_flood_tender'] = [var[0] for var in list(flood_filter_tuples)]
deduped_df.loc[:,'positive_keywords_dict'] = [var[1] for var in list(flood_filter_tuples)]
deduped_df.loc[:,'negative_keywords_dict'] = [var[2] for var in list(flood_filter_tuples)]

# Removing tenders from certain departments that are not related to flood management.
idea_frm_tenders_df = deduped_df[(deduped_df.is_flood_tender=='True')&
                                 (~deduped_df.Department.isin(["Directorate of Agriculture and Assam Seed Corporation","Department of Handloom Textile and Sericulture"]))]

print('Number of flood related tenders filtered: ', idea_frm_tenders_df.shape[0])

# Classify tenders based on Monsoons
for index, row in idea_frm_tenders_df.iterrows():
    monsoon = "" 
    published_date = dateutil.parser.parse(row['Published Date'])
    if 1 <= published_date.month <= 5:
        monsoon = "Pre-Monsoon"
        if published_date.month == 5 and published_date.day > 14:
            monsoon = "Monsoon"
    elif 6 <= published_date.month <= 10:
        monsoon = "Monsoon"
        if published_date.month == 10 and published_date.day > 14:
            monsoon = "Post-Monsoon"
    else:
        monsoon = "Post-Monsoon"
    idea_frm_tenders_df.loc[index, "Season"] = monsoon

# identify scheme related information
schemes_identified = []
scheme_kw = {'ridf','sdrf','sopd','cidf','ltif'}
for idx, row in idea_frm_tenders_df.iterrows():
    tender_slug = row['tender_title']+' '+row['tender_externalreference']+' '+row['Work Description']
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug).lower()

    tender_slug = set(re.split(r'[-.,()_\s/]\s*',tender_slug))
    try:
        schemes_identified.append(list(tender_slug & scheme_kw)[0].upper())
    except:
        schemes_identified.append('')

idea_frm_tenders_df.loc[:,'Scheme'] = schemes_identified

#Classification of Tenders based on Response Type
IMMEDIATE_MEASURES_KEYWORDS = ['sdrf','im','i/m','gr','g/r','relief','package','pkt','immediate']
PREPAREDNESS_MEASURES_KEYWORDS = ['protection','new', 'reconstruction', 'constn' ,'recoupment', 'restoration', 'embankment', 'embkt',
                      'dyke','culvert','storm water', 'drainage','drain','drains','box','rcc','silt','desiltation','prosiltation','anti erosion',
                      'erosion','a/e','ae','a e','bank protection','bank breach','breach','sludging','desludging','sluice','bund','bundh',
                      'dam','canal','road','roads','bridge','bridges','data','drone','rescue','consultation','advisory','consult','study']

for index, row in idea_frm_tenders_df.iterrows():
    immedidate_measures_dict = populate_keyword_dict(IMMEDIATE_MEASURES_KEYWORDS)
    preparedness_measures_dict = populate_keyword_dict(PREPAREDNESS_MEASURES_KEYWORDS)
    response_type = "Others"
    tender_slug = str(row['tender_externalreference']) + ' ' + str(row['tender_title']) + ' ' + str(row['Work Description'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for keyword in immedidate_measures_dict:
        keyword_count = len(re.findall(r"\b%s\b" % keyword.lower(), tender_slug.lower()))
        immedidate_measures_dict[keyword] = keyword_count
        if not keyword_count:
            immedidate_measures_dict[keyword] =  False
        else:
            response_type = "Immediate Measures"
    
    for keyword in preparedness_measures_dict:
        keyword_count = len(re.findall(r"\b%s\b" % keyword.lower(), tender_slug.lower()))
        preparedness_measures_dict[keyword] = keyword_count
        if not keyword_count:
            preparedness_measures_dict[keyword] =  False
        elif response_type == "Others":
            response_type = "Preparedness Measures"
    idea_frm_tenders_df.loc[index, "Response Type"] = response_type
    
    if response_type == "Immediate Measures":
        sub_head_dict = {k: v for k, v in immedidate_measures_dict.items() if v is not False}
        idea_frm_tenders_df.loc[index, "Flood Response - Subhead"] = str(sub_head_dict)
    elif response_type == "Preparedness Measures":
        sub_head_dict = {k: v for k, v in preparedness_measures_dict.items() if v is not False}
        idea_frm_tenders_df.loc[index, "Flood Response - Subhead"] = str(sub_head_dict)  

idea_frm_tenders_df.to_csv(os.getcwd()+'/Sources/TENDERS/data/IDEA-FRM_filtered_tenders_with_metadata_2023apr.csv',
                           encoding='utf-8')