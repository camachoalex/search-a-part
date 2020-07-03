import sys
from lxml import html
import requests


def runSetup():
    File = "./setupToySearch.txt"
    setup_components = []
    
    print("Returning part number, part name, and unique identifier key from", File)
    with open(File) as f:
        StringArray = f.read().split("/")
        ptName = StringArray[-3]
        uID = StringArray[-2]
        ptNum = StringArray[-1].replace('.html\n','')
    
    print("Part Name: "  ,ptName)
    print("Part Number: ",ptNum)
    print("Unique ID: "  ,uID)
    print("*********************************")
    
    return ptNum,ptName,uID


def returnDealerURL(year, ptNum,ptName,uID,zip_code):
    # This is currently hardcoded for tacoma. I can use a radio button for other choices        
    top_dealers = "https://parts.toyota.com/findDealer.aspx?ref=/productdetails.aspx_makeName=toyota*modelYear="+str(year)+"*modelName=tacoma*stockNumber="+ptNum+"*ukey_product="+uID +"&ukey_product="+uID +"&zipCode="+str(zip_code)
    
    page = requests.get(top_dealers)
    tree = html.fromstring(page.content)
    url_vec = tree.xpath('//div[@class="col-md-3"]/a/@href')
    
    return url_vec
def getPricesPerURL(url_vec):
    # This section of the code iterates through each url in url_vec and returns the price for each part.
    price_vec = []
    print("Returning prices from dealers...")

    for url in url_vec:
        page = requests.get(url)
        tree = html.fromstring(page.content)
    
        price = tree.xpath('//span[@class="productPriceSpan money-3"]/text()')    
        price_vec.append(price[0])
    return price_vec

def write2File(price_vec,url_vec):
    msg_vec = []
    #file = open("./results_toyota_shop.csv","w")
    #for url in url_vec:
    for index in range(0,1):#range(len(price_vec)):
        # some tring clean up before saving to text file
        p = price_vec[index].replace(' ','');
        p = p.replace('\n','')
        p = p.replace('\r','')
        msg = url_vec[index] + ","+p+"\n"
        msg_vec.append(msg)        
        #file.write(msg)
    return msg_vec
    #file.close()

def runGetPrices(zip_code,year):    
    # Run Setup
    ptNum,ptName,uID = runSetup()
    # get dealers
    url_vec = returnDealerURL(year,ptNum,ptName,uID,zip_code)
    # get prices
    price_vec = getPricesPerURL(url_vec)
    # write to file
    msg_vec = write2File(price_vec,url_vec)
    return msg_vec
    
# overhead stuff that grabs the inputs from the command line
if len( sys.argv ) == 3:
    zip_code  = sys.argv[1]
    year      = sys.argv[2]
else:
    zip_code = "90650"
    year = "2018"

# main call
runGetPrices(zip_code,year)


