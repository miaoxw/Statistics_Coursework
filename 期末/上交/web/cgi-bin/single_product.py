# -*- coding: utf-8 -*-
import os
import json
import cgi
import datetime
import sys
from string import Template
import backgroundSupport

def getLowestPrices(ASIN):
    date=[]
    price=[]
    for item in backgroundSupport.getOfferList(ASIN):
        date.append(item[0].isoformat())
        price.append(item[1])
    return (json.dumps(date),json.dumps(price))


def getPriceOfDifferentSellers(ASIN):
    date=[]
    price=[]
    temp=set()
    allData=backgroundSupport.getOfferByDifferentSellers(ASIN)
    for (seller,sales) in allData:
        if(seller!=None and seller!='Null'):
            for item in sales:
                temp.add(item[0])
    date=sorted([i.isoformat() for i in temp])
    for (seller,sales) in allData:
        if(seller!=None and seller!='Null'):
            saleData=[]
            for singleDate in date:
                if(singleDate in [i[0].isoformat() for i in sales]):
                    for j in sales:
                        if j[0].isoformat()==singleDate:
                            saleData.append(j[1])
                            break
                else:
                    if(len(saleData)==0):
                        saleData.append(None)
                    else:
                        saleData.append(saleData[-1])
            price.append({'name':seller,'data':saleData})
    retPrice=''
    for item in price:
        retPrice+='{name:"'+item['name']+'",data:'+json.dumps(item['data'])+'},'
    retPrice=retPrice.rstrip(',')
    retPrice='['+retPrice+']'
    return (json.dumps(date),retPrice)
    

def getSaleNumber(ASIN):
    offerList=backgroundSupport.getSaleTime(ASIN)
    temp=dict()
    dates=[]
    for item in offerList:
        if temp.has_key(item):
            temp[item]+=1
        else:
            temp[item]=1
            dates.append(item)
    ret=''
    for (date,number) in sorted(temp.iteritems(),key=lambda f:f[0]):
        yesterday=date-datetime.timedelta(days=1)
        tomorrow=date+datetime.timedelta(days=1)
        if(yesterday not in dates):
            ret+='[Date.UTC('+str(yesterday.year)+','+str(yesterday.month-1)+','+str(yesterday.day)+'),'+str(0)+'],'
        ret+='[Date.UTC('+str(date.year)+','+str(date.month-1)+','+str(date.day)+'),'+str(number)+'],'
        if(tomorrow not in dates):
            ret+='[Date.UTC('+str(tomorrow.year)+','+str(tomorrow.month-1)+','+str(tomorrow.day)+'),'+str(0)+'],'
    ret=ret.rstrip(',')
    return '['+ret+']'


def getPriceChange(ASIN):
    sales=backgroundSupport.getSaleTime(ASIN)
    offer=backgroundSupport.getOfferList(ASIN)
    priceChangeDate=[]
    priceChangeData=[]
    saleChangeData=[]
    index=0
    count1=0
    count2=0
    price1=offer[0][1]
    price2=offer[0][1]
    for item in offer:
        price2=item[1]
        while index<len(sales) and sales[index]<item[0]:
            index+=1
            count2+=1
        priceChangeDate.append(item[0].isoformat())
        priceChangeData.append(price2-price1)
        saleChangeData.append(count2-count1)
        count1=count2
        price1=price2
    return (json.dumps(priceChangeDate),json.dumps(priceChangeData),json.dumps(saleChangeData))

reload(sys)
sys.setdefaultencoding('utf8')

print 'Content-type: text/html\r\n\r\n'

#所有的数据预处理工作完成
params=cgi.FieldStorage()
ASIN=params['ASIN'].value
pictureAddress=backgroundSupport.getPicAddress(ASIN)
##print pictureAddress
(lowestPrice_date,lowestPrice_price)=getLowestPrices(ASIN)
##print lowestPrice_date
##print lowestPrice_price
(price_date,price_data)=getPriceOfDifferentSellers(ASIN)
##print price_date
##print price_data
starRate=str(backgroundSupport.getStarRate(ASIN))
##print starRate
sales=getSaleNumber(ASIN)
commentAndRate=str(backgroundSupport.getComment_Length(ASIN))
##print commentAndRate
(priceChange_date,priceChange_data,saleChange_data)=getPriceChange(ASIN)
##print priceChange_date
##print priceChange_data
##print saleChange_data



#读网页模板文件，替换格式字符串，输出
with open('C:\web\single_product_origin.html','r') as f:
    content=f.read()
    content=Template(content).safe_substitute(pic_add=pictureAddress)
    content=Template(content).safe_substitute(lowestPriceDate=lowestPrice_date)
    content=Template(content).safe_substitute(ASIN=ASIN)
    content=Template(content).safe_substitute(lowestPrice=lowestPrice_price)
    content=Template(content).safe_substitute(product_name=backgroundSupport.getProductName(ASIN))
    content=Template(content).safe_substitute(priceDate=price_date)
    content=Template(content).safe_substitute(priceData=price_data)
    content=Template(content).safe_substitute(starRateList=starRate)
    content=Template(content).safe_substitute(saleNumber=sales)
    content=Template(content).safe_substitute(comment_rate=commentAndRate)
    content=Template(content).safe_substitute(priceChangeDate=priceChange_date)
    content=Template(content).safe_substitute(priceChangeData=priceChange_data)
    content=Template(content).safe_substitute(saleChangeData=saleChange_data)

    
    print content
