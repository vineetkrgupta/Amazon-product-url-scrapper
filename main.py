import Amazonscrapper as scrapper 
product=input("Enter the product you want to search : ")
pages=input("Enter how many pages you want to crawl: ")
pincode=input("Enter pincode ")
hid=input("Enter 0 for running program in background else 1 :")

if hid==0:
    hid= False
else:
    hid=True
scrapper.search_amazon(product, pincode , pages ,hid )