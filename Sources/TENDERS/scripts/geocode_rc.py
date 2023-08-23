import pandas as pd
import os
import re
import geopandas as gpd

ASSAM_VILLAGES = gpd.read_file(os.getcwd()+'/Maps/assam_village_complete_with_revenueCircle_district_35_oct2022.geojson',
                               driver='GeoJSON')

idea_frm_tenders_df  = pd.read_csv(os.getcwd()+'/Sources/TENDERS/data/IDEA_FRM_DISTRICT_GEOTAG.csv')
VILLAGE_CORRECTION_DICT = {
    "SOKARBILA(BOLGARBARI)(DARIAPAR" : "SOKARBILA(BOLGARBARI)(DARIAPAR)",
    "MANGALDAI EXTENDED TOWN (BHEBA" : "MANGALDAI EXTENDED TOWN (BHEBA)",
    "UPPER DIHING R.F. (SOUTH BLOCK" : "UPPER DIHING R.F. (SOUTH BLOCK)",
    "KACHARI MAITHCHAGAON NO.1(BAR" : "KACHARI MAITHCHAGAON NO.1(BAR)",
}

MASTER_DFs = []
for FOCUS_DISTRICT in ['KAMRUP']: #ASSAM_VILLAGES.district_2.unique():
    print(FOCUS_DISTRICT)
    # Create dictionary for FOCUS DISTRICTS
    FOCUSDIST_village_dict = {}
    FOCUSDIST_block_dict = {}
    FOCUSDIST_subdistrict_dict = {}
    FOCUSDIST_revcircle_dict = {}
    FOCUSDIST_district_dict = {}
    
    for index,row in ASSAM_VILLAGES[ASSAM_VILLAGES.district_2==FOCUS_DISTRICT].iterrows():
        if row["VILNAM_SOI"]:
            row["VILNAM_SOI"] = re.sub(r'[^a-zA-Z]', "", row["VILNAM_SOI"])
            if row["VILNAM_SOI"] in VILLAGE_CORRECTION_DICT:
                row["VILNAM_SOI"] = VILLAGE_CORRECTION_DICT[row["VILNAM_SOI"]]

            FOCUSDIST_village_dict[row["VILNAM_SOI"]] = {"village_id" : row["OBJECTID"],
                                                     "block_name" : row["block_name"],
                                                     "subdistrict" : row["sdtname_2"],
                                                     "revenuecircle": row["revenue_ci"],
                                                     "district_2" : row["district_2"]}

        FOCUSDIST_block_dict[row["block_name"]] = {"subdistrict" : row["sdtname_2"],
                                               "revenuecircle": row["revenue_ci"],
                                               "district_2" : row["district_2"]}

        FOCUSDIST_subdistrict_dict[row["sdtname_2"]] = {"district_2" : row["district_2"]} 
        FOCUSDIST_revcircle_dict[row["revenue_ci"]] = {"district_2" : row["district_2"]} 
        FOCUSDIST_district_dict[row["district"]] = True
    
    try:
        del FOCUSDIST_village_dict['RIVER']
        del FOCUSDIST_block_dict['JORHAT']
    except:
        pass
    
    FOCUSDIST_villages = list(FOCUSDIST_village_dict.keys())
    FOCUSDIST_blocks = list(FOCUSDIST_block_dict.keys())
    FOCUSDIST_subdistricts = list(FOCUSDIST_subdistrict_dict.keys())
    FOCUSDIST_revcircles = list(FOCUSDIST_revcircle_dict.keys())
    
    print(FOCUSDIST_revcircles)
    ## GEO-CODE VILLAGES, BLOCKS, REVENUE-CIRCLES
    idea_frm_tenders_df_FOCUSDISTRICT = idea_frm_tenders_df[idea_frm_tenders_df["DISTRICT_FINALISED"] == FOCUS_DISTRICT]
    for idx, row in idea_frm_tenders_df_FOCUSDISTRICT.iterrows():
        tender_villages = []
        tender_village_id = ""
        tender_block = ""
        tender_revenueci = ""
        tender_subdistrict = ""

        tender_slug = str(row['tender_externalreference']) + ' ' + str(row['tender_title']) + ' ' + str(row['Work Description'])
        tender_slug = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tender_slug)

        # List of substrings to remove from GPE names
        substrings_to_remove = ["(pt)", "\n"]
        # Construct the regex pattern by joining the substrings with "|"
        pattern = "|".join(map(re.escape, substrings_to_remove))

        for village in FOCUSDIST_villages:
            if not re.search('[a-zA-Z]', village):
                continue 
            village = re.sub(r"[\[\]]?", "", village)
            
            if village in VILLAGE_CORRECTION_DICT:
                village = VILLAGE_CORRECTION_DICT[village]

            village_search = village.lower()
            village_search = re.sub(pattern, "", village_search)

            if re.findall(r'\b%s\b'%village_search.strip(), tender_slug.lower()):
                tender_villages.append(village)
                tender_village_id = FOCUSDIST_village_dict[village]['village_id']
                tender_block = FOCUSDIST_village_dict[village]['block_name']
                tender_revenueci = FOCUSDIST_village_dict[village]['revenuecircle']
                tender_subdistrict = FOCUSDIST_village_dict[village]['subdistrict']

        for block in FOCUSDIST_blocks:
            block_search = block.lower()
            block_search = re.sub(pattern, "", block_search)
            if re.findall(r'\b%s\b'%block_search.strip(), tender_slug.lower()):
                tender_block = block
                tender_revenueci = FOCUSDIST_block_dict[block]['revenuecircle']
                tender_subdistrict = FOCUSDIST_block_dict[block]['subdistrict']
                break

        for revenue_circle in FOCUSDIST_revcircles:
            revenue_circle_search = revenue_circle.lower()
            revenue_circle_search = re.sub(pattern, "", revenue_circle_search)
            if re.findall(r'\b%s\b'%revenue_circle_search.strip(), tender_slug.lower()):
                tender_revenueci = revenue_circle
                break

        for subdistrict in FOCUSDIST_subdistricts:
            subdistrict_search = subdistrict.lower()
            subdistrict_search = re.sub(pattern, "", subdistrict_search)
            if re.findall(r'\b%s\b'%subdistrict_search.strip(), tender_slug.lower()):
                tender_subdistrict = subdistrict
                break


        idea_frm_tenders_df_FOCUSDISTRICT.loc[idx,'tender_villages'] = str(tender_villages)[1:-1]
        idea_frm_tenders_df_FOCUSDISTRICT.loc[idx,'tender_block'] = tender_block
        idea_frm_tenders_df_FOCUSDISTRICT.loc[idx,'tender_subdistrict'] = tender_subdistrict
        idea_frm_tenders_df_FOCUSDISTRICT.loc[idx,'tender_revenueci'] = tender_revenueci
        
    MASTER_DFs.append(idea_frm_tenders_df_FOCUSDISTRICT)  


MASTER_DFs.append(idea_frm_tenders_df[idea_frm_tenders_df["DISTRICT_FINALISED"] == 'NA'])

MASTER_DF = pd.concat(MASTER_DFs)
MASTER_DF[['Tender ID','tender_externalreference','tender_title','Work Description', 'location',
           'DISTRICT_FINALISED','tender_villages', 'tender_block','tender_subdistrict','tender_revenueci']].to_csv(os.getcwd()+'/Sources/TENDERS/data/IDEA_FRM_RC_GEOTAG_KAMRUP.csv')