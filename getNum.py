from backgroundSupport import getAllProductsInCategory
from backgroundSupport import getReviewCount
from backgroundSupport import getStarRate
from backgroundSupport import getSaleTime
from backgroundSupport import getComment_Length
from backgroundSupport import getPrice_deltaReview
from backgroundSupport import getSellerCount
from backgroundSupport import getSellerOfferRank
from backgroundSupport import getProductCount

print getSellerCount('Clothing & Accessories>Baby>Baby Girls')
print getSellerOfferRank('Clothing & Accessories>Baby>Baby Girls')
products=getAllProductsInCategory('Clothing & Accessories>Baby>Baby Girls')
print len(products)
print getProductCount('Clothing & Accessories>Baby>Baby Girls')
count=0;
for item in products:
    count+=getReviewCount(item['ASIN'])
print count
print
print

print getSellerCount('Clothing & Accessories>Baby>Unisex')
print getSellerOfferRank('Clothing & Accessories>Baby>Unisex')
products=getAllProductsInCategory('Clothing & Accessories>Baby>Unisex')
print len(products)
print getProductCount('Clothing & Accessories>Baby>Unisex')
count=0;
for item in products:
    count+=getReviewCount(item['ASIN'])
print count
print
print

print getSellerCount('Health & Personal Care>Household Supplies>Air Fresheners')
print getSellerOfferRank('Health & Personal Care>Household Supplies>Air Fresheners')
products=getAllProductsInCategory('Health & Personal Care>Household Supplies>Air Fresheners')
print len(products)
print getProductCount('Health & Personal Care>Household Supplies>Air Fresheners')
count=0;
for item in products:
    count+=getReviewCount(item['ASIN'])
print count
print
print

print getSellerCount('Health & Personal Care>Household Supplies>Household Cleaning')
print getSellerOfferRank('Health & Personal Care>Household Supplies>Household Cleaning')
products=getAllProductsInCategory('Health & Personal Care>Household Supplies>Household Cleaning')
print len(products)
print getProductCount('Health & Personal Care>Household Supplies>Household Cleaning')
count=0;
for item in products:
    count+=getReviewCount(item['ASIN'])
print count
