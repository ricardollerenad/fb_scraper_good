#import Facebook_scraper class from facebook_page_scraper
from facebook_page_scraper import Facebook_scraper

#instantiate the Facebook_scraper class

page_or_group_name = "Meta"
posts_count = 10
browser = "Chrome"
proxy = "IP:PORT" #if proxy requires authentication then user:password@IP:PORT
timeout = 600 #600 seconds
headless = True
# get env password
fb_password = "ElianaSofia94@@"
fb_email = "ricardo.llerena.d@gmail.com"
# indicates if the Facebook target is a FB group or FB page
isGroup= False
meta_ai = Facebook_scraper(page_or_group_name, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless, isGroup=isGroup)
