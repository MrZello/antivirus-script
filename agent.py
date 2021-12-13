import requests
import hashlib, time, os

diction = {}
baseline = 0

def virusTotal(fileName):
    API = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
          
    #Upload File Below to VT
    postfileURL = 'https://www.virustotal.com/vtapi/v2/file/scan'
    files = {'file': (fileName, open(fileName, 'rb'))}
    
    print(f'Uploading New File {fileName}!')
    resp = requests.post(postfileURL, files = files, params = {'apikey': API})
    resp = resp.json()

    #Retrieve File Below
    filtKey = 'md5'
    resource = resp.get(filtKey)

    print(f'Getting Report for {fileName}!')
    retrieveURL = 'https://www.virustotal.com/vtapi/v2/file/report'
    report = requests.get(retrieveURL, params = {'apikey': API,
                                                'resource': resource})
    
    while report.status_code == 204:   #VT rate limit exceeded, so wait 90 secs
        time.sleep(90)
        report = requests.get(retrieveURL, params = {'apikey': API,
                                                     'resource': resource})
        
    #Save Total & Positives
    report = report.json()
    positives = report.get('positives')
    totals = report.get('total')

    #Calc percentage
    perc = 0.0
    try:
        perc = positives / totals
        perc *= 100.0
        print(f'Percentage detected by VT for {fileName} is {perc}!')
    except:
        perc = 0.0

    #return true if greater than 5% detection
    if perc >= 5.0:
        params = {'fileName': fileName, 'md5': resource}
        r = requests.post(f"http://127.0.0.1:8080/api/add", params=params)
        return True
        
    return False

                            #########################


while 1:
    obj = os.scandir(path = '.')
    
    for each in obj : 
        if each.is_file():

            fileName = each.name
            fileOpen = open(fileName,'rb')
            fileHash = hashlib.md5(fileOpen.read()).hexdigest()
            fileOpen.close()
            
            if(baseline == 0):  #Baseline what is already in the directory
                print(f'File {fileName} found!')
                diction[fileName] = fileHash
            
            if(baseline > 0):   #Only submit new files to VT (after initial scan)
                if fileName in diction.keys():
                    pass
                else:           #new file detected                        
                    send = virusTotal(fileName)     #send new file to VT func
                                           
                    if send == True:
                        os.remove(fileName) #remove malicious file
                    else:                           #otherwise
                        diction[fileName] = fileHash #add file to baseline

    obj.close()

    baseline = 1 #baseline complete
    time.sleep(5)
    #takes forever to rescan for malicious files at 5 mins so I put 5 secs
    
    
