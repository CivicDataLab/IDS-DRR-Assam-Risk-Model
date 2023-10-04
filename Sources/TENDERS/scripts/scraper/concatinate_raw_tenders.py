import pandas as pd
import os
import glob

path = os.getcwd() + '/Sources/TENDERS/scripts/scraper/scraped_recent_tenders/2022_july_dec'
data_path = os.getcwd() + '/Sources/TENDERS/data/'

csvs = glob.glob(path+'/f*.csv')
print(len(csvs))
dfs= []

for csv in csvs:
    df = pd.read_csv(csv)
    dfs.append(df)

master_df = pd.concat(dfs)
master_df = master_df.dropna(subset=['Tender ID'])
master_df = master_df[['Tender ID','Tender Reference Number', 'Title', 'Work Description', 'Tender Category', 'Tender Type',
                       #'Form of contract',
                       'Product Category', 'Is Multi Currency Allowed For BOQ', 'Allow Two Stage Bidding', 'Independent External Monitor/Remarks',
                       'Publish Date', 'Pre Bid Meeting Date', 'Bid Validity(Days)', 'Should Allow NDA Tender', 'Allow Preferential Bidder',
                       'Payment Mode', 'Bid Opening Date', 'Organisation Chain', 'Location', 'Pincode','No. of Covers', 'Tender Value in ₹',
                       'Bidder Name', 'Awarded Value', 'Status', 'Contract Date :', 'Tender Stage']]

master_df['Department'] = master_df['Organisation Chain']
master_df = master_df.rename(columns={'Tender Reference Number':'tender_externalreference',
                                      'Title': 'tender_title',
                                      'No. of Covers': 'No of Bids Received',
                                      'Publish Date': 'Published Date',
                                      'Location': 'location'})
master_df.to_csv(data_path+'2023aprmerged.csv')