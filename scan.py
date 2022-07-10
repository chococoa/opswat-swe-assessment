# 1. Calculate the hash of a given file (i.e. samplefile.txt) 
# 2. Perform a hash lookup against metadefender.opswat.com and see if there are 
# previously cached results for the file 
# 3. If results are found, skip to step 6 
# 4. If results are not found, upload the file and receive a "data_id" 
# 5. Repeatedly pull on the "data_id" to retrieve results 
# 6. Display results in format below (SAMPLE OUTPUT) 
# 7. You should also have some basic error handling for common HTTP results 
#    It is not necessary to account for every idiosyncrocy of the API. 
#    You can show any errors to the standard error and exit the application. 

# SAMPLE INPUT COMMAND: 
#     upload_file samplefile.txt 
# SAMPLE OUTPUT: 
#     filename: samplefile.txt 
#     overall_status: Clean 
#     engine: Ahnlab 
#     threat_found: SomeBadMalwareWeFound 
#     scan_result: 1 
#     def_time: 2017-12-05T13:54:00.000Z 
#     engine: Cyren 
#     threat_found: Clean 
#     scan_result: 0 
#     def_time: 2017-12-05T17:43:00.000Z 
#     <repeats for each engine> 


import hashlib

import requests

API_KEY = "1f4000446f26470daf160a2b269da23b"

# print(hashlib.algorithms_guaranteed)

file = "sample1.txt" # Location of the file (can be set a different way)
BLOCK_SIZE = 65536 # The size of each read from the file

file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
with open(file, 'rb') as f: # Open the file to read it's bytes
    fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
    while len(fb) > 0: # While there is still data being read from the file
        file_hash.update(fb) # Update the hash
        fb = f.read(BLOCK_SIZE) # Read the next block from the file

# print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash

HASH = file_hash.hexdigest()
print(HASH)


# 2. Perform a hash lookup against metadefender.opswat.com and see if there are 
# previously cached results for the file 

url = "https://api.metadefender.com/v4/apikey/"
headers = {
 "apikey": API_KEY
}

response = requests.request("GET", url, headers=headers)
print(response.text)


url = "https://api.metadefender.com/v4/file"
headers = {
 "apikey": API_KEY,
 "Content-Type": "application/octet-stream",
 "filename": "sample1.txt"
}
payload = "\"@/path/to/sample1.txt\""

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

DATA_ID = "bzIyMDcxMGhvMklBaWZvdkVHVHgzU3M5ZWk"

url = "https://api.metadefender.com/v4/hash/a1c139ae07086ecbd038dc15e61553a6c8092764c17cd2d95a6e3a9df5fed23d"
headers = {
 "apikey": API_KEY
}

response = requests.request("GET", url, headers=headers)

print(response.text)