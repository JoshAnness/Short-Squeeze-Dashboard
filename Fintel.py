headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

def getFintel(ticker):
    url = 'https://fintel.io/ss/us/' + ticker
    response = Request(url, headers = headers)
    webpage = urlopen(response).read()
    html = soup(webpage, "html.parser")
    table = html.find("table", attrs={"class":"table table-sm"})

    sir = ''
    sif = ''
    dpsv = ''
    dpsvr = ''

    array = []
    for data in table.find_all('td'):
        array.append(data.get_text())

    index = 0;
    for data in array:
        if data == 'Short Interest Ratio':
            sir = array[index+1]
        if data == 'Short Interest % Float':
            sif = array[index+1][1 : 7]
        if data == 'Dark Pool Short Volume':
            dpsv = array[index+1][0 : 14]
        if data == 'Dark Pool Short Volume Ratio':
            dpsvr = array[index+1][0 : 6]
        index += 1

    table = html.find("table", attrs={"class":"table table-sm", "id":"topic-table-body"})
    array = []
    for data in table.find_all('td'):
        array.append(data.get_text())

    sharesAvailable = array[2].strip()

    table = html.findAll("table", attrs={"class":"table table-sm", "id":"topic-table-body"})[1]
    array = []
    for data in table.find_all('td'):
        array.append(data.get_text())

    fee = array[2].strip()

    data = np.array([sir, sif, dpsv, dpsvr, sharesAvailable, fee])

    return data

getFintel('BLNK')
