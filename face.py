""" 
print("Hola Ricardo")
"""

from facebook_page_scraper import Facebook_scraper
page_list = ["frasecorta"]
proxy_port = 6000
posts_count = 10
browser = "chrome"
timeout = 600
headless = False

for page in page_list:
	proxy = f'http://{"spy3z1lq4m"}:{"yenaL6uvqYQj271qsM"}@gate.smartproxy.com:'+str(proxy_port)
	scraper = Facebook_scraper(page,posts_count, browser,proxy=proxy, timeout=timeout, headless=headless)
	directorio = "/home/ricardo/Descargas/1_WEB_SCRAPING/data/"
	filename = page
	scraper.scrap_to_csv(filename,directorio)
	proxy_port+=1

