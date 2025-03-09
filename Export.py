import requests
import json
import time
import os
import shutil

#-------------------------------------------------------------------------------------------------------------------------------------------
# Headers for API requests
#-------------------------------------------------------------------------------------------------------------------------------------------
# Authentication (Replace with your OAuth token or API key) Set as an env variable
ACCESS_TOKEN = '<access token>'
BASE_URL = '<URL>' # verify later through test API page

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
}
#-------------------------------------------------------------------------------------------------------------------------------------------
# This function grabs all the contacts such as Skill ID, Contact ID, Skill Name, Team Name
#-------------------------------------------------------------------------------------------------------------------------------------------
#Nov 12th was day of start
Start_date = "2024-11-14"
End_date = "2024-11-15"
Amount = 4500 #max is 10000
#sending the request to gather contact IDs
def api_request_contacts(headers):
    url = f'{BASE_URL}startDate={Start_date}&endDate={End_date}&fields=masterContactId%2C%20skillId%2C%20contactId%2C%20skillName%2C%20teamName%2C%20stateId%2C%20contactStartDate&top={Amount}'
    response = requests.get(url, headers=headers)
    Call_data = response.json()
    #Putting the Json in a file to deal with later.
    with open('Data.json', 'w') as file:
        json.dump(Call_data, file)

    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()
#-------------------------------------------------------------------------------------------------------------------------------------------
# This grabs all the contacts such as Skill ID, Contact ID, Skill Name, Team Name
#-------------------------------------------------------------------------------------------------------------------------------------------
def api_request_calls(headers):
    #Change to proper URL for video URL download.
    url = f'{BASE_URL}?acd-call-id={lst_master_ID[0]}&media-type=voice-only&exclude-waveforms=true&exclude-qm-categories=true&isDownload=false'
    response = requests.get(url, headers=headers)
    Call_data = response.json()
    #Putting the Json in a file to deal with later.
    with open('video.json', 'w') as file:
        json.dump(Call_data, file)
    
    
    if response.status_code != 200: #Possible to add if !=200 send refresh token once I know how to do so. 
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def api_request_meta(headers):
    #Change to proper URL for metadata download
    url = f'{BASE_URL}/{lst_contact_ID[0]}'
    response = requests.get(url, headers=headers)
    data = response.json()
    #Putting the Json in a file to deal with later.
    contact_info = data['contactId']
    abandoned = contact_info.get('abandoned', False)
    agent_id = contact_info.get('agentId', None)

    # Check if abandoned is True or agentId is None
    if abandoned or agent_id is None:
        print("Condition met: Abandoned is True or agentId is None")
        print(f'Call Id {lst_contact_ID[0]} will be removed from MasterContactId list \n this will skip the call download for this ID')
        lst_master_ID.remove(lst_contact_ID[0])

    else:
        print("Condition not met: agentId is Valid and Abandoned is False")
        print(f'ContactID is good {lst_contact_ID[0]} apending metadata to Meta.json')
        with open('meta.json', 'a') as file:
            json.dump(data, file)
    
    #Check if Abandoned is true and agentId is null if so drop the metadata and remove the ID from the MasterContactId list
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

api_request_contacts(headers)
#-------------------------------------------------------------------------------------------------------------------------------------------
# This filters out the data for Sonesta calls within the exported data
#-------------------------------------------------------------------------------------------------------------------------------------------
lst_contact_ID = []
lst_master_ID = []

# Read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)  # Parse JSON content from the file

# Filter contacts based on conditions
filtered_contacts = [
    contact for contact in data["contacts"]
    #if contact["skillName"] == "Outbound" and contact["teamName"].strip() == "Extended"
    if contact["skillName"] == "Skiil Name" or contact["skillName"] == "Skiil Name" or contact["skillName"] == "Skiil Name" or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000 or contact["skillId"] == 000000
]
# Print the results
for contact in filtered_contacts:
    if contact["contactId"] != contact["masterContactId"]:
        filtered_contacts.remove(contact)
    print(contact)
    with open('Filtered.txt', 'a') as file:
        file.write(f'{contact}\n')
        file.close()

for contact in filtered_contacts:
    Contact_IDs = contact["contactId"]
    Master_ID = contact["masterContactId"]
    lst_contact_ID.append(Contact_IDs)
    lst_master_ID.append(Master_ID)


#-------------------------------------------------------------------------------------------------------------------------------------------
# Pass the contact ID for Metadata download
#-------------------------------------------------------------------------------------------------------------------------------------------
#appends all the sonesta contactIds to a file
with open('ContactId.txt', 'a') as file:
    for each in lst_contact_ID:
        #print(lst_contact_ID[0])
        file.write(f'{lst_contact_ID[0]}\n')
        api_request_meta(headers)
        first_val = lst_contact_ID.pop(0)


#-------------------------------------------------------------------------------------------------------------------------------------------
# Pass the Master contact ID and whatever other data is needed to download the call
#-------------------------------------------------------------------------------------------------------------------------------------------

#print(lst_contact_ID)
print("Sleep Timer starts now, cancel run for testing")
time.sleep(5)

lst_call_links = []

#appends all the sonesta masterIds to a file

for each in lst_master_ID:
    #print(lst_master_ID[0])
    with open('MasterId.txt', 'a') as file:
        file.write(f'{lst_master_ID[0]}\n')
        file.close()
    api_request_calls(headers)
    # Open the output file in append mode
    # Read JSON data from the file
    with open("video.json", 'r') as file1:
        audio = json.load(file1)
        file1.close()
    with open("audio_links.txt", 'a') as file2:
        # Iterate through interactions and write links to the output file
        for interaction in audio.get("interactions", []):
            file_to_play_url = interaction["data"].get("fileToPlayUrl")
            if file_to_play_url:  # Only write if the URL is not None
                file2.write(file_to_play_url + "\n")
                file2.close()
            #donwload Audi file
            url = file_to_play_url
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Try to get the file name from the Content-Disposition header
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition and 'filename=' in content_disposition:
                    # Extract the file name from the header
                    file_name = content_disposition.split('filename=')[1].strip('\"')
                else:
                    # If no filename is found in the header, use the URL's last part as the name
                    file_name = os.path.basename(url)

                # Save the content with the original file name
                with open(file_name, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded successfully as {file_name} {lst_master_ID[0]}")
                time.sleep(10)
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
    #print(f"Audio links {file_to_play_url}.")
    first_val = lst_master_ID.pop(0)
#moving calls to the shared drive
source_dir = os.getcwd()
destination_dir = '<folder location>'

# Make sure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    # Check if the file has a .mp4 extension
    if filename.endswith('.mp4'):
        # Construct full file path
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        
        # Copy the file to the destination directory
        shutil.move(source_file, destination_file)
        print(f"Copied: {filename}")
