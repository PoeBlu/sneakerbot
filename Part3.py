import requests
import bs4
import random
import webbrowser
import csv
import threading
import RandomHeaders
proxies = {
			'http': "",
			'https': "",
		}

ModelNumber = 'BB9043'
SizeList = [9, 13, 4, 10]
ThreadCount = 10

# Base URL =  http://www.adidas.com/us/BB9043.html?forceSelSize=BB9043_600
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def GetItem(model, size):
	ShoeSizeCode = size_to_size_code(size)
	url = 'http://www.adidas.com/us/' + str(model) + '.html?Quantity=1&forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	res = requests.get(url)
	page = bs4.BeautifulSoup(res.text, "lxml")
	webbrowser.open(url, new=2)


def size_to_size_code(size):
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	return ShoeSizeCode
	

def CheckStock(url):
	RawHTML = requests.get(url, headers=RandomHeaders.LoadHeader())
	print(RawHTML)
	Page = bs4.BeautifulSoup(RawHTML.text, "lxml")
	ListOfRawSizes = Page.select('.size-dropdown-block')
	Sizes = str(ListOfRawSizes[0].getText()).replace('\t', '')
	Sizes = Sizes.replace('\n\n', ' ')
	Sizes = Sizes.split()
	Sizes.remove('Select')
	Sizes.remove('size')
	print(Sizes)
	return Sizes

def SneakerBot(model, size=None):
	# while True:
	# 	try:
	url = 'http://www.adidas.com/us/{}.html'.format(model)
	print(url)
	Sizes = CheckStock(url)
	if size != None:
		#If you didn't input size
		if str(size) in Sizes:
			GetItem(model, size)
	else:
		for a in Sizes:
			GetItem(model, a)
		# except:
		# 	pass

SneakerBot(ModelNumber, 9)
# Main(ModelNumber, 9)
# threads = [threading.Thread(name='ThreadNumber{}'.format(n), target=SneakerBot, args=(ModelNumber, size,)) for size in SizeList for n in range(ThreadCount)]
# for t in threads: t.start()
