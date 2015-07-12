import sys, os, io, time
import pp


def fetchWeb(url):
	try:
		page = requests.get(url)

	except requests.exceptions.RequestException as e:
		print "Error en solicitud de pagina"
		return
	else:
		print "Pagina " + url + " obtenida"
	return page

def csv_writer(data, path):
	#for csv delimeter definition on Dialect
	csv.register_dialect("pipes", delimiter="|")
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


def getListOfIssueLinks(volume, url, origin):
	data = []
	lista = []
	tmp_a = []
	tmp_b = []

	soup = bs4.BeautifulSoup(fetchWeb(url).text)
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

	if (len(lista) == 0) or (lista is None):
		return None

	for link in lista:
		ref = ""
		#Para JUCS y caso normal de sciencedirect
		if link.a:
			tmp_a = (link.a["href"]).split("/")
			if (origin == "jucs"):
				vol = tmp_a[1].split("_")
				if volume <= int(vol[1]):
					data.append(link.a["href"])
			elif (origin == "computer"):
				data.append(link.a["href"])
			elif (origin == "sciencedirect"):
				vol = tmp_a[4]
				if volume <= int(vol):
					data.append(link.a["href"])

		#Caso especial de sciencedirect
		elif link.find("span"):
			ref = url.replace("http://www.sciencedirect.com", "")
			tmp_link = ref.encode("utf-8")
			slash = tmp_link.split("/")
			if volume <= int(slash[4]):
				data.append(tmp_link)
			
	data.sort()
	return data


def obtainAbstract(url, origin):
	page = fetchWeb(url).text
	
	soup = bs4.BeautifulSoup(page)
	abstract = ""
	if origin == "sciencedirect":
		tmp = soup.find_all("div", attrs={"class": "abstract svAbstract "})
		if len(tmp) > 0:
			for p in tmp:
				abstract = abstract + " " + p.text.replace("\n", "").encode("utf-8")
	elif  origin == "jucs":
		tmp = soup.find_all("p")
		if len(tmp) >0:
			for p in tmp:
				abstract = abstract + " " + p.text.replace("\n", "").encode("utf-8")
	elif origin == "computer":
		tmp = soup.find("div", attrs={"class": "abstractText"})
		tmp1 = tmp.get_text().replace("<p>", "")
		tmp2 = tmp1.replace("</p>", "")
		tmp3 = tmp2.replace("<it>", "")
		tmp4 = tmp3.replace("</it>", "")
		abstract = tmp4.encode("utf-8")

	if abstract is not None:
		return abstract.rstrip("\n")
	else:
		return None



def extract(_input):
	print ("Computing results with PID [%d]" % os.getpid())
	line1 = _input[0]
	line2 = _input[1]
	_FILES = _input[2]
	nameSource = ""
	URL = ""
	url = ""
	journal = ""
	jour_begin = ""
	jour_end = ""

	line = line1.rstrip("\n")
	tmp = ""
	url = line.rstrip("\n")
	data = []
	brokenURL = line.split(".")
	#----------------------------------------------------
	#To obtain journal"s name to give csv files a path
	tmp = brokenURL[2].split("/")
	#ScienceDirect Journals
	if brokenURL[1] == "sciencedirect":
		nameSource = brokenURL[1] + "-" + tmp[len(tmp)-1]
	#IEEE Transactions
	elif brokenURL[1] == "computer":
		nameSource = brokenURL[1] + "-" + tmp[1] + "-" + tmp[2] + "-" + tmp[3]	
	#JUCS
	elif brokenURL[1] == "jucs":
		nameSource = brokenURL[1]
	#------------------------------------------------------------
	nextLine = line2
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
		minn = []
		maxx = []
		
		#JUCS
		if brokenURL[1] == "jucs":
			_URL = url + "_" + str(i)						
		#IEEE
		elif (brokenURL[1] == "computer"):
			_URL = url.replace("/index.html","") + "/" + str(i) + "/index.html"
		#ScienceDirect
		elif (brokenURL[1] == "sciencedirect"):
			_URL = url + "/" + str(i)

		if len(pageLinks) == 0:
			pageLinks = getListOfIssueLinks(i, _URL, brokenURL[1])
		if ((pageLinks is not None)) and (brokenURL[1] == "sciencedirect"):
			if len(pageLinks) > 0:
				minn = pageLinks[0].split("/")
				maxx = pageLinks[len(pageLinks)-1].split("/")
				if(len(minn) == 4):
					if i < maxx[3]:
						i = int(maxx[3])
				elif(len(minn) > 4):
					if i < maxx[4]:
						i = int(maxx[4])
		if pageLinks is None:
			i = i + 1
			continue
		pageLinks.sort()
		#Hasta aca funciona el paralelismo
		
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
					soup = bs4.BeautifulSoup(webPage) #se cae aca
					for row in soup.find_all("a", attrs={"class": "cLink artTitle S_C_artTitle "}):
						absRef = row["href"]
						abstract = obtainAbstract(absRef, brokenURL[1])
						if(first):
							if abstract is not None:
								data.append([vol, issue, "http://www.sciencedirect.com" + page , row.get_text().encode("utf-8"), abstract ])
							else:
								data.append([vol, issue, "http://www.sciencedirect.com" + page , row.get_text().encode("utf-8"), ""])
							first = False
						else:
							if abstract is not None:
								data.append([vol, issue, "" , row.get_text().encode("utf-8"), abstract ])
							else:
								data.append([vol, issue, "" , row.get_text().encode("utf-8"), ""])
			#------------------------------------------------------------
			
			elif (brokenURL[1] == "jucs"):
				arr = page.split("_")
				issue = arr[len(arr)-1]
				vol = arr[len(arr)-2]
				if (int(vol) <= int(end)):
					webPage = fetchWeb("http://www.jucs.org" + page). text
					soup = bs4.BeautifulSoup(webPage)
					toc = "toc_" + vol + "_" + issue
					for row in soup.find_all("td", attrs={"valign": "top", "width": "335"}):
						tmpAbsRef = row.a["href"]
						absRef = "http://www.jucs.org" + tmpAbsRef
						abstract = obtainAbstract(absRef, brokenURL[1])
						if (first):
							if abstract is not None:
								data.append([vol, issue, "http://www.jucs.org" + page, row.get_text().encode("utf-8"), abstract ])
							else:
								data.append([vol, issue, "http://www.jucs.org" + page, row.get_text().encode("utf-8"), "" ])
							first = False
						else:
							if abstract is not None:
								data.append([vol, issue, "", row.get_text().encode("utf-8"), abstract ])
							else:
								data.append([vol, issue, "", row.get_text().encode("utf-8"), "" ])
			
			#------------------------------------------------------------
			elif (brokenURL[1] == "computer"):
				arr = page.split("/")
				issue = arr[len(arr)-2]
				vol = arr[len(arr)-3]
				if (int(vol) <= int(end)):
					webPage = fetchWeb("https://www.computer.org" + page). text
					soup = bs4.BeautifulSoup(webPage)
					for row in soup.find_all("div", attrs={"class": "tableOfContentsLineItemTitle"}):
						tmpAbsRef = row.a["href"]
						absRef = "https://www.computer.org" + tmpAbsRef
						abstract = obtainAbstract(absRef, brokenURL[1])
						if (first):
							if abstract is not None:
								data.append([vol, issue, "https://www.computer.org" + page, row.a.text.encode("utf-8"), abstract])
							else:
								data.append([vol, issue, "https://www.computer.org" + page, row.a.text.encode("utf-8"), ""])
							first = False
						else:
							if abstract is not None:
								data.append([vol, issue, "", row.a.text.encode("utf-8"), abstract])
							else:
								data.append([vol, issue, "", row.a.text.encode("utf-8"), ""])
		#Separador de Volumenes
		csv_writer(data, _PATH)
		pageLinks = []
		i = i + 1
		print "\n"


_FILES = "FILES/"
#read list of resources
_fileURL = open("links", "r")

inputs = []
for line in _fileURL:
	if(line[0] != "#") and (line[0] == "h"):
		nextLine = next(_fileURL)
		inputs.append([line, nextLine,_FILES])

_fileURL.close()

#create job server for parallelism  
ppservers = ()
job_server = pp.Server(ppservers=ppservers)
print "Starting pp with", job_server.get_ncpus(), "workers\n"

jobs_procs = [(_input, job_server.submit(extract,(_input,), (fetchWeb,csv_writer, getListOfIssueLinks, obtainAbstract,), modules=("sys", "requests", "csv", "re", "os", "io", "bs4",))) for _input in inputs]

for _input, job in jobs_procs:
	job()

job_server.print_stats()