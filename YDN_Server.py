import pytube
import os
import thread
from flask import Flask
import requests

app = Flask(__name__)

@app.route("/download/<id>") # id submitted by extension.
def hello(id):
	thread.start_new_thread(download,("https://www.youtube.com/watch?v="+id,None));
	return id
	

def download(url,i):
	print "[*] Getting Video Info"
	yt = pytube.YouTube(url)
	r = requests.get(url)
	al = r.text
	title = al[al.find('<title>') + 7 : al.find('</title>')]
	print title
	yt.set_filename(title.replace("|","_").replace("?","").replace("*",""))
	print "[+] Getting 720p as Default...."
	try:
		video = yt.get('mp4', '720p') #Chosing a good available res.
	except pytube.exceptions.DoesNotExist:
		video = yt.get('mp4', '360p')
		print "[-] Switching to 360p..."
	print "[+] Downloading : ",title
	video.download(os.getcwd())
	print "[++] Completed! :",title
	
if __name__ == "__main__":
    app.run()