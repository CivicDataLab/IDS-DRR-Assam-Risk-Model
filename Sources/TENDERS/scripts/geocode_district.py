import pandas as pd
import geopandas as gpd
import re
import os
from difflib import SequenceMatcher

idea_frm_tenders_df = pd.read_csv(os.getcwd()+'/Sources/TENDERS/data/flood_tenders_all.csv')

#ASSAM_VILLAGES = gpd.read_file(os.getcwd()+'/Maps/assam_village_complete_with_revenueCircle_district_35_oct2022.geojson',
 #                              driver='GeoJSON')
ASSAM_VILLAGES = pd.read_csv(os.getcwd()+'/Maps/ASSAM_VILLAGES_MASTER.csv', encoding='utf-8').dropna()

#Clean village names
assam_villages = ASSAM_VILLAGES["VILNAM_SOI"]
village_duplicates_df = ASSAM_VILLAGES[assam_villages.isin(assam_villages[assam_villages.duplicated()])].sort_values("VILNAM_SOI")
VILLAGE_CORRECTION_DICT = {
    "SOKARBILA(BOLGARBARI)(DARIAPAR" : "SOKARBILA(BOLGARBARI)(DARIAPAR)",
    "MANGALDAI EXTENDED TOWN (BHEBA" : "MANGALDAI EXTENDED TOWN (BHEBA)",
    "UPPER DIHING R.F. (SOUTH BLOCK" : "UPPER DIHING R.F. (SOUTH BLOCK)",
    "KACHARI MAITHCHAGAON NO.1(BAR" : "KACHARI MAITHCHAGAON NO.1(BAR)",
}
ASSAM_VILLAGES.revenue_ci = ASSAM_VILLAGES.revenue_ci.str.replace('\(Pt\)','')
ASSAM_VILLAGES.revenue_ci = ASSAM_VILLAGES.revenue_ci.str.replace('\(Pt-I\)','')
ASSAM_VILLAGES.revenue_ci = ASSAM_VILLAGES.revenue_ci.str.replace('\(Pt-II\)','')
ASSAM_VILLAGES.revenue_ci = ASSAM_VILLAGES.revenue_ci.str.replace('\n',' ')
ASSAM_VILLAGES.revenue_ci = ASSAM_VILLAGES.revenue_ci.str.strip()

ASSAM_VILLAGES.sdtname_2 = ASSAM_VILLAGES.sdtname_2.str.replace('\(Pt\)','')
ASSAM_VILLAGES.sdtname_2 = ASSAM_VILLAGES.sdtname_2.str.replace('\(Pt-I\)','')
ASSAM_VILLAGES.sdtname_2 = ASSAM_VILLAGES.sdtname_2.str.replace('\(Pt-II\)','')


locations = []
for idx, row in idea_frm_tenders_df.iterrows():
    LOCATION = row['location'].lower()
    LOCATION = LOCATION.replace('village','')
    LOCATION = LOCATION.replace('district','')
    LOCATION = LOCATION.replace('dist','')
    LOCATION = re.sub('[^a-zA-Z\n\.]', ' ', LOCATION)
    scores = []
    for revenue_circle in ASSAM_VILLAGES.revenue_ci.dropna().unique():
        score = SequenceMatcher(None, LOCATION, revenue_circle.lower().strip()).ratio()
        scores.append(score)
    if max(scores)>0.8:
        locations.append(ASSAM_VILLAGES.revenue_ci.dropna().unique()[scores.index(max(scores))])
    else:
        locations.append(row['location'])

idea_frm_tenders_df.location = locations

rev_circles = ASSAM_VILLAGES[["revenue_ci",'district_2']].drop_duplicates().dropna()
#These revenue circles are across multiple districts
problematic_rev_circles = rev_circles[rev_circles.duplicated(['revenue_ci'],keep=False)].sort_values('revenue_ci')

sdts= ASSAM_VILLAGES[["sdtname_2",'district_2']].drop_duplicates().dropna()
#These revenue circles are across multiple districts
problematic_sdts = sdts[sdts.duplicated(['sdtname_2'],keep=False)].sort_values('sdtname_2')

# GEOCODE DISTRICTS

#MAKE A DICTIONARY OF ONLY NON-REPEATED REVENUE CIRCLES, SUB-DISTRICTS, BLOCKS and VILLAGES MAPPED TO THEIR DISTRICTS
assam_revenue_circles_dict = ASSAM_VILLAGES[['revenue_ci','district_2']].dropna().drop_duplicates().drop_duplicates(['revenue_ci'],keep=False).set_index('revenue_ci').to_dict(orient='index')
assam_subdist_dict = ASSAM_VILLAGES[['sdtname_2','district_2']].dropna().drop_duplicates().drop_duplicates(['sdtname_2'],keep=False).set_index('sdtname_2').to_dict(orient='index')
assam_blocks_dict = ASSAM_VILLAGES[['block_name','district_2']].dropna().drop_duplicates().drop_duplicates(['block_name'],keep=False).set_index('block_name').to_dict(orient='index')
assam_villages_dict = ASSAM_VILLAGES[['VILNAM_SOI','district_2']].drop_duplicates(['VILNAM_SOI'],keep=False).set_index('VILNAM_SOI').to_dict(orient='index')

#Force fit duplicate revenue circles in districts
assam_revenue_circles_dict['Baganpara']={'district_2': 'BAKSA'}
assam_revenue_circles_dict['Bagribri']={'district_2': 'DHUBRI'}
assam_revenue_circles_dict['Bajali']={'district_2': 'BAJALI'}
assam_revenue_circles_dict['Barnagar']={'district_2': 'BAKSA'}
assam_revenue_circles_dict['Chapar']={'district_2': 'DHUBRI'}
assam_revenue_circles_dict['Dalgaon']={'district_2': 'DARRANG'}
assam_revenue_circles_dict['Dhakuakhana']={'district_2': 'LAKHIMPUR'}
assam_revenue_circles_dict['Dhekiajuli']={'district_2': 'SONITPUR'}
assam_revenue_circles_dict['Dhubri']={'district_2': 'DHUBRI'}
assam_revenue_circles_dict['Ghograpar']={'district_2': 'NALBARI'}
assam_revenue_circles_dict['Golokganj']={'district_2': 'DHUBRI'}
assam_revenue_circles_dict['Gossaigaon']={'district_2': 'KOKRAJHAR'}
assam_revenue_circles_dict['Jalah']={'district_2': 'BAKSA'}
assam_revenue_circles_dict['Khoirabari']={'district_2': 'UDALGURI'}
assam_revenue_circles_dict['Kokrajhar']={'district_2': 'KOKRAJHAR'}
assam_revenue_circles_dict['Lakhipur']={'district_2': 'GOALPARA'}
assam_revenue_circles_dict['Mangaldoi']={'district_2': 'DARRANG'}
assam_revenue_circles_dict['Pathorighat']={'district_2': 'DARRANG'}
assam_revenue_circles_dict['Sarupeta']={'district_2': 'BAJALI'}
assam_revenue_circles_dict['Sidli']={'district_2': 'CHIRANG'}
assam_revenue_circles_dict['Subansiri']={'district_2': 'LAKHIMPUR'}
assam_revenue_circles_dict['Rangia']={'district_2': 'KAMRUP'}

#MAKE LIST OF DISTRICTS, REVENUE CIRCLES, SUB-DISTRICTS, BLOCKS and VILLAGES WITH NON-REPEATING NAMES
problematic_rev_circlesUPPERCASE = [] #Empty after forcefitted. #[rc.upper().strip() for rc in problematic_rev_circles.revenue_ci.unique()]
problematic_sdtsUPPERCASE = [sdt.upper().strip() for sdt in problematic_sdts.sdtname_2.unique()]
assam_villages = list(set(assam_villages_dict.keys())-set(problematic_rev_circlesUPPERCASE)-set(problematic_sdtsUPPERCASE))
assam_blocks = list(set(assam_blocks_dict.keys())-set(problematic_rev_circlesUPPERCASE)-set(problematic_sdtsUPPERCASE))
assam_districts = list(set(ASSAM_VILLAGES.district_2.dropna())-set(['KAMRUP','KAMRUP METRO']))

assam_revenue_circles = list(set(assam_revenue_circles_dict.keys()))#-set(problematic_rev_circles.revenue_ci.unique())-set(problematic_sdts.sdtname_2.unique()))
assam_sub_districts = list(set(assam_subdist_dict.keys())-set(problematic_rev_circles.revenue_ci.unique())-set(problematic_sdts.sdtname_2.unique()))

# CREATE A DICTIONARY OF DISTRICT IDENTIFIERS FROM externalReference COLUMN
three_letter_distirct_identifiers_dict = {"bak":"BAKSA", "baksa":"BAKSA",
                                          "bar":"BARPETA", "re-bar": "BARPETA", "barpeta":"BARPETA",
                                          "bongaigoan":"BONGAIGAON",
                                          "tez":"SONITPUR","re-tez":"SONITPUR","tezpur":"SONITPUR","tej":"SONITPUR","re-tej":"SONITPUR",
                                          "silchar":"CACHAR", "re-silchar":"CACHAR","resilchar":"CACHAR","re-sil(mech)":"CACHAR","silchar (mech)":"CACHAR","sil":"CACHAR","sil (mech)":"CACHAR","sil(mech)":"CACHAR",
                                          "dhubri":"DHUBRI", "dhu": "DHUBRI",
                                          "siv":"SIVSAGAR","sivsagar":"SIVSAGAR","re-siv":"SIVSAGAR","sivasagar":"SIVSAGAR",
                                          "chirang":"CHIRANG",
                                          "mang":"DARRANG","re-mang":"DARRANG","mangaldai":"DARRANG","mangaldoi":"DARRANG",
                                          "dhe":"DHEMAJI","dhemaji":"DHEMAJI","dmj":"DHEMAJI","redhemaji":"DHEMAJI",
                                          "hailakandi":"HAILAKANDI","hkd":"HAILAKANDI","re-hailakandi":"HAILAKANDI",
                                          "dib-west":"DIBRUGARH","dib":"DIBRUGARH","dibrugarh":"DIBRUGARH","redib":"DIBRUGARH",
                                          "dima-hasao":"DIMA HASAO","haf":"DIMA HASAO","haflong":"DIMA HASAO",
                                          "goalpara":"GOALPARA","GLP":"GOALPARA",
                                          "diphu":"K.ANGLONG","rediphu":"K.ANGLONG",
                                          "jor":"JORHAT","jorhat":"JORHAT",
                                          "nag":"NAGAON","re-nag":"NAGAON","nagaon":"NAGAON","hatimura":"NAGAON",
                                          "nal":"NALBARI","nalbari":"NALBARI",
                                          "morigaon":"MORIGAON","mor":"MORIGAON","re-mor":"MORIGAON",
                                          "maj":"MAJULI","re-maj":"MAJULI","maju":"MAJULI","majuli":"MAJULI",
                                          "n.lakhimpur":"LAKHIMPUR","dhakuakhana":"LAKHIMPUR","nlp":"LAKHIMPUR","nl":"LAKHIMPUR","dhk":"LAKHIMPUR",
                                          "kar":"KARIMGANJ","rekar":"KARIMGANJ","re-kar":"KARIMGANJ","karimganj":"KARIMGANJ","badarpur":"KARIMGANJ",
                                          "gmda":"KAMRUP METRO","ghy east":"KAMRUP METRO","ghy.east":"KAMRUP METRO","ghy. east":"KAMRUP METRO","ghyeast":"KAMRUP METRO","g.east":"KAMRUP METRO","ghy east":"KAMRUP METRO","ghy west":"KAMRUP METRO","ge":"KAMRUP METRO","ghy.west":"KAMRUP METRO","ghy. west":"KAMRUP METRO","ghywest":"KAMRUP METRO",
                                          "kok":"KOKRAJHAR",
                                          "rangia":"KAMRUP",
                                          "gdd":"KAMRUP METRO"
                                         }

# METHOD-2 WEIGHTAGE METHOD
# GET TENDER DISTRICT BASED ON externalReference COLUMN

idea_frm_tenders_df['tender_district_externalReference'] = None
for idx, row in idea_frm_tenders_df.iterrows():
    
    district_identifier = str(row['tender_externalreference']).split(r'/')[0].lower()
    if 'rgr' in district_identifier:
        district_identifier = district_identifier.split('rgr')[0].strip()[:-1]
    
    if district_identifier in three_letter_distirct_identifiers_dict:
        idea_frm_tenders_df.loc[idx,'tender_district_externalReference'] = three_letter_distirct_identifiers_dict[district_identifier]
        
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_externalreference'] != None:
        continue
    tender_slug = str(row['tender_externalreference'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    for district in assam_districts:
        if re.findall(r'\b%s\b'%district.lower().strip(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_externalReference'] = district
            break
            
## REVENUE
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_externalreference'] != None:
        continue
    
    tender_slug = str(row['tender_externalreference'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for revenue_circle in assam_revenue_circles:
        if re.findall(r'\b%s\b'%revenue_circle.lower().strip(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_externalReference'] = assam_revenue_circles_dict[revenue_circle]['district_2']
            break

            
## SUB DISTRICT
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_externalreference'] != None:
        continue
    
    tender_slug = str(row['tender_externalreference'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for sub_district in assam_sub_districts:
        if re.findall(r'\b%s\b'%sub_district.lower(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_externalReference'] = assam_subdist_dict[sub_district]['district_2']
            break

# GET TENDER DISTRICT BASED ON TITLE AND WORK DESCRIPTION

idea_frm_tenders_df['tender_district_title_description'] = None
for idx, row in idea_frm_tenders_df.iterrows():
    tender_slug = str(row['tender_title']) + ' ' + str(row['Work Description'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    for district in assam_districts:
        if re.findall(r'\b%s\b'%district.lower().strip(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_title_description'] = district
            break
            
## REVENUE
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_district_title_description'] != None:
        continue
    
    tender_slug = str(row['tender_title']) + ' ' + str(row['Work Description'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for revenue_circle in assam_revenue_circles:
        if re.findall(r'\b%s\b'%revenue_circle.lower().strip(), tender_slug.lower()):
            print(revenue_circle)
            idea_frm_tenders_df.loc[idx,'tender_district_title_description'] = assam_revenue_circles_dict[revenue_circle]['district_2']
            break

            
## SUB DISTRICT
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_district_title_description'] != None:
        continue
    
    tender_slug = str(row['tender_title']) + ' ' + str(row['Work Description'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for sub_district in assam_sub_districts:
        if re.findall(r'\b%s\b'%sub_district.lower(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_title_description'] = assam_subdist_dict[sub_district]['district_2']
            break
# GET TENDER DISTRICT BASED ON LOCATION COLUMN
idea_frm_tenders_df['tender_district_location'] = None
for idx, row in idea_frm_tenders_df.iterrows():
    tender_slug = str(row['location']) 
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    for district in assam_districts:
        if re.findall(r'\b%s\b'%district.lower().strip(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_location'] = district
            break
            
## REVENUE
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_district_location'] != None:
        continue
    
    tender_slug = str(row['location'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for revenue_circle in assam_revenue_circles:
        if re.findall(r'\b%s\b'%revenue_circle.lower().strip(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_location'] = assam_revenue_circles_dict[revenue_circle]['district_2']
            break

            
## SUB DISTRICT
for idx, row in idea_frm_tenders_df.iterrows():
    if row['tender_district_location'] != None:
        continue
    
    tender_slug = str(row['location'])
    tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    for sub_district in assam_sub_districts:
        if re.findall(r'\b%s\b'%sub_district.lower(), tender_slug.lower()):
            idea_frm_tenders_df.loc[idx,'tender_district_location'] = assam_subdist_dict[sub_district]['district_2']
            break

# BTC FLAG
idea_frm_tenders_df['BTC_flag'] = None
for idx, row in idea_frm_tenders_df.iterrows():
    BTC_flag = False
    
    #tender_slug = str(row['Tender ID']) + ' ' + str(row['tender_title']) + ' ' + str(row['Work Description'] + ' ' + str(row['location']))
    #tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)
    
    #skip Bodoland tenders
    department_slug = str(row["Organisation Chain"] + ' ' + row["Department"])
    department_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', department_slug)
    if re.findall(r"bodoland", department_slug.lower()):
        BTC_flag= True
    
    bodoland_dept_slugs = ["BoTC", "BTC"]
    for slug in bodoland_dept_slugs:
        if slug in row["Tender ID"]:
            BTC_flag= True

    idea_frm_tenders_df.loc[idx,'BTC_flag'] = BTC_flag

# WEIGHTAGE LOGIC
idea_frm_tenders_df['tender_district_externalReference'].fillna('NA',inplace=True) 
idea_frm_tenders_df['tender_district_title_description'].fillna('NA',inplace=True) 
idea_frm_tenders_df['tender_district_location'].fillna('NA',inplace=True) 

idea_frm_tenders_df['DISTRICT_FINALISED'] = ''

for idx, row in idea_frm_tenders_df.iterrows():
    district1 = row['tender_district_externalReference']
    district2 = row['tender_district_title_description']
    district3 = row['tender_district_location']
    districts = [district1,district2,district3]
    districts = set([x for x in districts if x!='NA'])

    if len(districts)==1:
        DISTRICT_SELECTED = list(districts)[0]
    elif len(districts)==0:
        DISTRICT_SELECTED = 'NA'
    else:
        DISTRICT_SELECTED = 'CONFLICT'
    
    idea_frm_tenders_df.loc[idx,'DISTRICT_FINALISED'] = DISTRICT_SELECTED

idea_frm_tenders_df.to_csv(os.getcwd()+'/Sources/TENDERS/data/floodtenders_districtgeotagged.csv',index=False)

print('Total number of flood related tenders: ', idea_frm_tenders_df.shape[0])
print('Number of tenders whose district could not be geo-tagged: ',idea_frm_tenders_df[idea_frm_tenders_df['DISTRICT_FINALISED']=='NA'].shape[0])
print('Number of tenders whose district identification is a CONFLICT: ',idea_frm_tenders_df[idea_frm_tenders_df['DISTRICT_FINALISED']=='CONFLICT'].shape[0])