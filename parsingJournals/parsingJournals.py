import sys, requests, csv, re, os, io
from bs4 import BeautifulSoup
import bs4

#for csv delimeter definition on Dialect
csv.register_dialect("pipes", delimiter="|")

def fetchWeb(url):
	try:
		page = requests.get(url)

	except requests.exceptions.RequestException as e:
		print ("Error: ", e)
		return Exception("Error al cargar página")
	else:
		print ("Página " + url + " obtenida")
	return page

def csv_writer(data, path):
	try:
		csvfile = open(path,"a")
	except IOError:
		csvfile = open(path,"w+")
	else:	

		fieldnames = ["volume", "issue", "url", "title", "abstract"]
		dialect = csv.get_dialect("pipes")
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=dialect)
		writer.writeheader()
		for row in data:
			writer.writerow({"volume": row[0], "issue": row[1], "url": row[2], "title": row[3], "abstract": row[4]})

def getListOfIssueLinks(url, origin):
	data = []
	lista = []

	soup = BeautifulSoup(fetchWeb(url).text)
	#------------------------------------------------------------
	#ScienceDirect
	if(origin == "sciencedirect"):
		lista = soup.find_all("div", attrs={"class": "txt currentVolumes"})			
	#------------------------------------------------------------
	elif(origin == "computer"):
		lista = soup.find_all("div", attrs={"class": "issuePeriod"})
	#------------------------------------------------------------
	#JUCS
	elif(origin == "jucs"):
		lista = soup.find_all( "div", attrs={"class": "nv nvi"})
	#Springer
	"""
	elif (origin == "springer"):
		arr = (url.split("/"))
		vol = arr[len(arr)-1]
		idV = "volume" + vol
		dic = {"id" : idV}
		newUrl = url.replace("volumesAndIssues/", "")
		getVol = soup.find_all("div", dic)
		print(getVol)
		#lista = getVol.find_all("div", attrs={"class": "issue-item"})
		#print(lista)
	"""
	if (len(lista) == 0) or (lista is None):
		return None
	for link in lista:
		if link.a:
			data.append(link.find("a")["href"])
		else:
			if (origin == "sciencedirect"):
				extra = (link.find("span").get_text()).split(" ")
				if (len(extra) > 2):
					ref = url.replace("http://www.sciencedirect.com", "") + "/" + extra[len(extra)-1]
				else:
					ref = url.replace("http://www.sciencedirect.com", "")
				data.append(ref)
	data.sort()
	return data


def obtainAbstract(url, origin):
	abstract = ""
	try:
		page = fetchWeb(url).text
	except Exception as inst:
		return "No se pudo cargar el abstract! BUSCAR MANUALMENTE. Error: " + inst
	soup = BeautifulSoup(page)
	abstract = ""
	if origin == "sciencedirect":
		tmp = soup.find_all("div", attrs={"class": "abstract svAbstract "})
		if len(tmp) > 0:
			for p in tmp:
				abstract = abstract + p.text.replace("\n", "") + " "
	elif  origin == "jucs":
		tmp = soup.find_all("p")
		if len(tmp) >0:
			for p in tmp:
				abstract = abstract + p.text.replace("\n", "") + " " 
	elif origin == "computer":
		tmp = soup.find("div", attrs={"class": "abstractText"})
		abstract = tmp.get_text()
	if abstract is not None:
		return abstract.rstrip("\n")
	else:
		return None



#read list of resources

_FILES = "FILES/"
nameSource = ""
_URL = ""
url = ""
resource = ""
journal = ""
jour_begin = ""
jour_end = ""

_fileURL = open("links", "r")
for line in _fileURL:
	line = line.rstrip("\n")
	tmp = ""
	url = line.rstrip("\n")
	data = []
	if(line[0] != "#"):
		brokenURL = line.split(".")
		#----------------------------------------------------
		#To obtain journal"s name to give csv files a path
		if (line[0] == "h"):
			tmp = brokenURL[2].split("/")
			#ScienceDirect Journals
			if brokenURL[1] == "sciencedirect":
				nameSource = brokenURL[1] + "-" + tmp[len(tmp)-1]
			#IEEE Transactions
			elif brokenURL[1] == "computer":
				nameSource = brokenURL[1] + "-" + tmp[1] + "-" + tmp[2] + "-" + tmp[3]
			#Springer Link
			#elif brokenURL[1] == "springer":
			#	nameSource = brokenURL[1] + "-" + tmp[len(tmp)-1]	
			#JUCS
			elif brokenURL[1] == "jucs":
				nameSource = brokenURL[1]
		#------------------------------------------------------------
		#Read next line to obtain the first and last journal to read
		nextLine = next(_fileURL)
		begin = nextLine.split(" ")[0]
		end = nextLine.split(" ")[1]
		#Volumes
		i = int(begin)
		while (i < (int(end) + 1)):
			tmpURL = ""
			_PATH = _FILES + nameSource + ".csv"
			pageLinks = []
			vol = ""
			issue = ""
			maxx = []
			
			#JUCS
			if brokenURL[1] == "jucs":
				_URL = url + "_" + str(i)						
			#IEEE
			elif (brokenURL[1] == "computer"):
				_URL = url.replace("/index.html","") + "/" + str(i) + "/index.html"
			#Springer
			#elif (brokenURL[1] == "springer"):
			#	_URL = url + "/" + str(i)
			#ScienceDirect
			elif (brokenURL[1] == "sciencedirect"):
				_URL = url + "/" + str(i)

			if len(pageLinks) == 0:
				pageLinks = getListOfIssueLinks(_URL, brokenURL[1])
			#Caso especial para sciencedirect
			if ((pageLinks is not None)) and (brokenURL[1] == "sciencedirect"):
				if len(pageLinks) > 0:
					if pageLinks[0] < pageLinks[len(pageLinks)-1]: #Aprovechando que se puede comparar un string así :D
						maxx = pageLinks[len(pageLinks)-1].split("/")
					else:
						maxx = pageLinks[0].split("/")
					if(len(maxx) == 4):
						i = int(maxx[3])
					else:
						i = int(maxx[4])
			if pageLinks is None:
				i = i + 1
				continue
			pageLinks.sort()
			
			print ("HTML adquirido: ", _URL)
			print ("Escribiendo títulos para URL: " + _URL)
			for page in pageLinks:
				first = True
				arr = []
				if (brokenURL[1] == "sciencedirect"):
					arr = page.split("/")
				#------------------------------------------------------------
					#Exclusivo de ScienceDirect
					if(len(arr) > 5):
						issue = arr[len(arr)-1]
					else:
						issue = "-"
					vol = arr[4]

					if (int(vol) <= int(end)):
						webPage = fetchWeb("http://www.sciencedirect.com" + page).text
						try:
							soup = BeautifulSoup(webPage) #se cae acá
						except Exception("algo pasó con BeautifulSoup"):
							print("paso soup")
							print(soup.get_text())
						print ("\n\nArtículos:")
						for row in soup.find_all("a", attrs={"class": "cLink artTitle S_C_artTitle "}):
							absRef = row["href"]
							abstract = obtainAbstract(absRef, brokenURL[1])
							if(first):
								if abstract is not None:
									data.append([vol, issue, "http://www.sciencedirect.com" + page , row.get_text(), abstract ])
								else:
									data.append([vol, issue, "http://www.sciencedirect.com" + page , row.get_text(), ""])
								first = False
							else:
								if abstract is not None:
									data.append([vol, issue, "" , row.get_text(), abstract ])
								else:
									data.append([vol, issue, "" , row.get_text(), ""])
					#------------------------------------------------------------
				elif (brokenURL[1] == "jucs"):
					arr = page.split("_")
					issue = arr[len(arr)-1]
					vol = arr[len(arr)-2]
					if (int(vol) <= int(end)):
						webPage = fetchWeb("http://www.jucs.org" + page). text
						soup = BeautifulSoup(webPage)
						toc = "toc_" + vol + "_" + issue
						for row in soup.find_all("td", attrs={"valign": "top", "width": "335"}):
							tmpAbsRef = row.a["href"]
							absRef = "http://www.jucs.org" + tmpAbsRef
							abstract = obtainAbstract(absRef, brokenURL[1])
							if (first):
								if abstract is not None:
									data.append([vol, issue, "http://www.jucs.org" + page, row.get_text(), abstract ])
								else:
									data.append([vol, issue, "http://www.jucs.org" + page, row.get_text(), "" ])
								first = False
							else:
								if abstract is not None:
									data.append([vol, issue, "", row.get_text(), abstract ])
								else:
									data.append([vol, issue, "", row.get_text(), "" ])
				
				#------------------------------------------------------------
				elif (brokenURL[1] == "computer"):
					arr = page.split("/")
					issue = arr[len(arr)-2]
					vol = arr[len(arr)-3]
					if (int(vol) <= int(end)):
						webPage = fetchWeb("https://www.computer.org" + page). text
						soup = BeautifulSoup(webPage)
						for row in soup.find_all("div", attrs={"class": "tableOfContentsLineItemTitle"}):
							tmpAbsRef = row.a["href"]
							absRef = "https://www.computer.org" + tmpAbsRef
							abstract = obtainAbstract(absRef, brokenURL[1])
							if (first):
								if abstract is not None:
									data.append([vol, issue, "https://www.computer.org" + page, row.a.text, abstract])
								else:
									data.append([vol, issue, "https://www.computer.org" + page, row.a.text, ""])
								first = False
							else:
								if abstract is not None:
									data.append([vol, issue, "", row.a.text, abstract])
								else:
									data.append([vol, issue, "", row.a.text, ""])

			#Separador de Volumenes
			csv_writer(data, _PATH)
			print("\nArtículos y Abstracts de " + _URL + " obtenidos\n\n")
			pageLinks = []
			i = i + 1
_fileURL.close()
