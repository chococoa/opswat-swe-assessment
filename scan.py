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


import hashlib
import requests

API_KEY = "1f4000446f26470daf160a2b269da23b"

def upload_file(file):
  # file = "sample1.txt"  # Location of the file (can be set a different way)
  BLOCK_SIZE = 65536  # The size of each read from the file

  # Create the hash object, can use something other than `.sha256()` if you wish
  try:
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:  # Open the file to read it's bytes
      # Read from the file. Take in the amount declared above
      fb = f.read(BLOCK_SIZE)
      while len(fb) > 0:  # While there is still data being read from the file
        file_hash.update(fb)  # Update the hash
        fb = f.read(BLOCK_SIZE)  # Read the next block from the file
  except:
    print("File not found")
    exit()

  # print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
  HASH = file_hash.hexdigest()

  # 2. Perform a hash lookup against metadefender.opswat.com and see if there are
  # previously cached 
  
  # metadefender.opswat.com's results when uploaded file (sample1.txt)
  url = "https://api.metadefender.com/v4/file/bzIyMDcxMlFqdjgzZFhrYkptbWJ6MkM5LWNf"

  headers = {
      'apikey': "3d16dda39201cf56b91150208ea5c56c"
  }
  response = requests.request("GET", url, headers=headers)  
  
  # using my api key and my hash value
  hash_url = "https://api.metadefender.com/v4/hash/" + HASH
  headers = {
    "apikey": API_KEY
  }
  hash_response = requests.request("GET", hash_url, headers=headers)

  # 3. If results are found, skip to displaying results
  if (response and hash_response):
    print("found")
    res_json = response.json()
    scan_details = ((res_json.get(('scan_results')))['scan_details'])
    if (scan_details != {}):
      displayResults(file, scan_details)  
  # if results are not found, upload file and retrieve "data_id"
  else:
    # print("not found")
    try:
      file_url = "https://api.metadefender.com/v4/file"
      headers = {
        "apikey": API_KEY,
        "Content-Type": "application/octet-stream",
        "filename": "sample1.txt"
      }
      payload = "\"@/path/to/sample1.txt\""

      response = requests.request("POST", file_url, headers=headers, data=payload)
      res_json = response.json()
      data_id = res_json.get('data_id')

      # repeatedly pull on the "data_id" to retrieve results
      while True:
        try:
          data_url = "https://api.metadefender.com/v4/file/" + data_id
          headers = {
            "apikey": API_KEY,
          }

          response = requests.request("GET", data_url, headers=headers)
          res_json = response.json()
        
          percentage = (res_json.get(('scan_results')))['progress_percentage']
          if percentage == 100:
            break
          
          scan_details = ((res_json.get(('scan_results')))['scan_details'])
          if (scan_details != {}):
            displayResults(file, scan_details)      
        except:
          print("Data not found")
          break
    except:
      print("Error getting file")


def displayResults(file, scan_details):    
  print("filename:", file)
  print("overall_status: Clean")
  
  for engine in scan_details:
    threat_found = scan_details[engine]['threat_found']
    scan_result = scan_details[engine]['scan_result_i']
    def_time = scan_details[engine]['def_time']

    if threat_found == "":
      threat_found = "Clean"
    
    print("engine:", engine)
    print("threat_found:", threat_found)
    print("scan_result:", scan_result)
    print("def_time:", def_time)

upload_file('sample1.txt')