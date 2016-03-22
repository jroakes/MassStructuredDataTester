import urllib.parse
import urllib.request
import json
import csv
import time

# To Do: - Proxy Support

urlinput = input('Enter input text file: ')
urls = open(urlinput, "r")
outputcsv = input('Enter a filename (minus file extension): ') + '.csv'
seconds = input('Enter number of seconds to wait between URL checks: ')

google = 'https://structured-data-testing-tool.developers.google.com/sdtt/web/validate'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
headers = { 'User-Agent' : user_agent, 'Referer' : 'https://structured-data-testing-tool.developers.google.com/sdtt/web?', 'Origin' : 'https://structured-data-testing-tool.developers.google.com' }

f = csv.writer(open(outputcsv, "w+", newline="\n", encoding="utf-8"))
f.writerow(["URL", "Number of Errors"])

for line in iter(urls):
	values = {'url' : line}
	data = urllib.parse.urlencode(values)
	data = data.encode('utf-8')
	req = urllib.request.Request(google, data, headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	data = respData[5:].decode('utf-8')
	j_obj = json.loads(data)
	total = 0
	for i in range(len(j_obj['tripleGroups'])):
		total += int(j_obj['tripleGroups'][(i-1)--1]['numErrors'])
	f.writerow([j_obj['url'], total])
	print("Checked URL: " + line)
	print("Waiting " + str(seconds) + " seconds until checking next URL.\n")
	time.sleep(float(seconds))
urls.close()

print ("Writing to " + outputcsv + " complete.")