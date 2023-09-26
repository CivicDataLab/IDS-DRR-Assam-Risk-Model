from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os

service_account = ' idsdrr@ee-idsdrr.iam.gserviceaccount.com'
# tasks = ee.data.listOperations()
# for task in tasks[:2]:
#     print(task['metadata']['description'], task['metadata']['state'])
# exit()
# tasks = ee.data.getTaskList()
# # Iterate through tasks and terminate export to Drive tasks
# for task in tasks:
#         print(f"Terminating task: {task['id']}")
#         ee.data.cancelTask(task['id'])   

# authenticate to Google Drive (of the Service account)
gauth = GoogleAuth()
scopes = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('Sources/NASADEM/ee-idsdrr-d856f70748a7.json',
                                                                      scopes=scopes)

drive = GoogleDrive(gauth)

## To get folder ID
# file_list  = drive.ListFile().GetList()
# for file in file_list:
#     print(file["title"], file["id"])

NASADEM_folder_id = '1NfiKDY3JaOCrL2vRgZOojefhzwTLP8gW'

# get list of files
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(NASADEM_folder_id)}).GetList()

for file in file_list:
    filename = file['title']
    print(file["title"], file["mimeType"])

    # download file into working directory (in this case a tiff-file)
    file.GetContentFile(os.getcwd()+'/Sources/NASADEM/data/'+filename,
                        mimetype=file['mimeType'])

    # delete file afterwards to keep the Drive empty
    #file.Delete()