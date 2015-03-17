import json
import urllib
from string import Template
from datetime import date


def getPicAddress(ASIN):
    str1="http://112.124.1.3:8004/api/commodity/"
    str2="?field=['productInfo']"
    data=json.loads(urllib.urlopen(str1+ASIN+str2).read())
    data['productInfo'][0]['img']


def getProductName(ASIN):
    str1="http://112.124.1.3:8004/api/commodity/"
    str2="?field=['productInfo']"
    data=json.loads(urllib.urlopen(str1+ASIN+str2).read())
    return data['productInfo'][0]['name'].replace('"','&quot;').replace(",",'&apos;')
    

def getAllProductsInCategory(categoryName):
    categoryName=categoryName.replace('&','$')
    count=getProductCount(categoryName)
    if count%20==0:
        pageNum=count/20
    else:
        pageNum=count/20+1
    ret=[]
    for i in range(1,pageNum+1):
        str1='http://112.124.1.3:8004/api/commodity?category_name=${name}'
        str2="page=${num}&field=['ASIN']"
        data=json.loads(urllib.urlopen('&'.join([Template(str1).safe_substitute(name=categoryName),Template(str2).safe_substitute(num=str(i))])).read())
        for item in data:
            ret.append(item)
    return ret


def getProductCount(categoryName):
    categoryName=categoryName.replace('&','$')
    data=json.loads(urllib.urlopen('http://112.124.1.3:8004/api/commodity/count/?category_name='+categoryName).read())
    return data['count']


def getSaleTime(ASIN):
    str1=Template('http://112.124.1.3:8004/api/commodity/${product}').safe_substitute(product=ASIN)
    str2="field=['review']"
    data=json.loads(urllib.urlopen('?'.join([str1,str2])).read())
    ret=[]
    for item in data['review']:
        datestr=item['publishTime'].split(None,1)[0]
        datearr=datestr.split('-')
        dateobj=date(int(datearr[0]),int(datearr[1]),int(datearr[2]))
        ret.append(dateobj)
    list.sort(ret)
    return ret


#Only the lowest price of the same time is obtained...
def getOfferList(ASIN):
    str1=Template('http://112.124.1.3:8004/api/commodity/${product}').safe_substitute(product=ASIN)
    str2="field=['offer']"
    data=json.loads(urllib.urlopen('?'.join([str1,str2])).read())
    ret=dict()
    for item in data['offer']:
        for smallerItem in item['info']:
            datestr=smallerItem['timestamp'].split(None,1)[0]
            datearr=datestr.split('-')
            key=date(int(datearr[0]),int(datearr[1]),int(datearr[2]))
            if ret.has_key(key):
                if smallerItem['price']<ret[key]:
                    ret[key]=smallerItem['price']
            else:
                ret[key]=smallerItem['price']
    return sorted(ret.iteritems(),key=lambda f:f[0])


def getReviews(ASIN):
    str1=Template('http://112.124.1.3:8004/api/commodity/${product}').safe_substitute(product=ASIN)
    str2="field=['review']"
    data=json.loads(urllib.urlopen('?'.join([str1,str2])).read())
    return data['review']


def getReviewCount(ASIN):
    return len(getReviews(ASIN))


def getStarRate(ASIN):
    ret=[0,0,0,0,0,0]
    for item in getReviews(ASIN):
        star=int(float(item['star'].split(' ',1)[0]))
        ret[star]+=1
    return ret


def getComment_Length(ASIN):
    ret=[]
    for item in getReviews(ASIN):
        star=int(float(item['star'].split(' ',1)[0]))
        length=len(item['content'].split())
        ret.append([length,star])
    return ret


def getPrice_deltaReview(ASIN):
    ret=[]
    priceList=getOfferList(ASIN)
    saleTime=getSaleTime(ASIN)
    p=0
    for i in range(1,len(priceList)):
        currentTime=priceList[i][0]
        deltaPrice=priceList[i][1]-priceList[i-1][1]
        count=0
        while p<len(saleTime):
            if saleTime[p]<=priceList[i][0]:
                p+=1
                count+=1
            else:
                break
        ret.append((currentTime,deltaPrice,count))
    return ret


def getOfferByDifferentSellers(ASIN):
    str1=Template('http://112.124.1.3:8004/api/commodity/${product}').safe_substitute(product=ASIN)
    str2="field=['offer']"
    data=json.loads(urllib.urlopen('?'.join([str1,str2])).read())
    temp=dict()
    for item in data['offer']:
        for smallerItem in item['info']:
            seller=smallerItem['seller']['name']
            datestr=smallerItem['timestamp'].split(None,1)[0]
            datearr=datestr.split('-')
            offerDate=date(int(datearr[0]),int(datearr[1]),int(datearr[2]))
            if temp.has_key(seller):
                temp[seller].append((offerDate,smallerItem['price']))
            else:
                temp[seller]=[(offerDate,smallerItem['price'])]
    for item in temp.keys():
        temp[item].sort()
    ret=list(sorted(temp.iteritems(),key=lambda f:f[0]))
    return ret


def getSellerOfferRank(categoryName):
    categoryName=categoryName.replace('&','$')
    ret=dict()
    for item in getAllProductsInCategory(categoryName):
        ASIN=item['ASIN']
        sellers=[item[0] for item in getOfferByDifferentSellers(ASIN)]
        for seller in sellers:
            if seller!='Null':
                if ret.has_key(seller):
                    ret[seller]+=1
                else:
                    ret[seller]=1
    return sorted(ret.iteritems(),key=lambda f:f[1],reverse=True)


def getSellerCount(categoryName):
    categoryName=categoryName.replace('&','$')
    return len(getSellerOfferRank(categoryName))
