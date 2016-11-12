# -*- coding: utf-8 -*-
import json, sys, re, webbrowser, urllib.request
from datetime import datetime

PAGE = 'https://www.gog.com'
PAGE_POSTFIX ='/games/ajax/filtered?mediaType=game&page='

JSON_TOTAL_PAGES = "totalPages"
JSON_PRODUCTS = "products"
JSON_PRICE = "price"
JSON_PRICE_BASE = "baseAmount"
JSON_PRICE_FINAL = "finalAmount"
JSON_DISCOUNT = "discount"
JSON_TITLE = "title"
JSON_URL = "url"
JSON_IMAGE = "image"

PARAM_SALE = 'sale'

def main(argv):
	gog_json = json.loads( urllib.request.urlopen(PAGE+PAGE_POSTFIX+'1').readall().decode('utf-8'))
	print('Processing total '+str(gog_json[JSON_TOTAL_PAGES])+' pages')
	gog_game = parse_games(gog_json[JSON_TOTAL_PAGES], "" if len(argv)<2 else argv[1])
	gog_game.sort(key=lambda x: x[4])
	date_today = datetime.strftime(datetime.now(), "%d_%m_%Y")
	file_name = date_today+'.html'
	html(gog_game, file_name)
	webbrowser.open_new_tab(file_name)

def parse_games(total_pages, sort_mode):
	result = []  #list games
	for i in range(1, total_pages+1):
		print('Processing '+str(i)+' page')
		json_page= urllib.request.urlopen(PAGE+PAGE_POSTFIX+str(i)).readall().decode('utf-8')
		gog_page = json.loads(json_page)
		for x in range(0, len(gog_page[JSON_PRODUCTS])):
			gog_price = gog_page[JSON_PRODUCTS][x][JSON_PRICE]
			if gog_price[JSON_PRICE_BASE]>gog_price[JSON_PRICE_FINAL] and sort_mode == PARAM_SALE or sort_mode == "":
				result.append(product(gog_page[JSON_PRODUCTS][x]))
	return result

def product(gog_item):
	gog_game_img = gog_item[JSON_IMAGE]
	gog_game_url = gog_item[JSON_URL]
	gog_game_title = gog_item[JSON_TITLE]
	gog_game_discount = gog_item[JSON_PRICE][JSON_DISCOUNT]
	gog_game_price = int(gog_item[JSON_PRICE][JSON_PRICE_FINAL])
	return [gog_game_img, gog_game_url, gog_game_title, gog_game_discount, gog_game_price]

def html(list_game, file_name):
	date_today = datetime.strftime(datetime.now(), "%d_%m_%Y")
	file = open(file_name, 'w+')
	file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <style> table{width: 60%; margin-left: auto; margin-right: auto;} a{text-decoration: none; color: black;} a:visited{color: grey;} tr:hover{background-color:#cce6ff;}</style> \n<h2>'+date_today+"</h2>\n<table style='border-collapse: collapse;'>\n<tr style='border:solid 1px black; text-align:center;'>\n<td>Изображение</td>\n<td>Название</td>\n<td>Скидка</td>\n<td>Цена</td>\n</tr>\n")
	for i in range(0,len(list_game)):
		list_item =	'<td style ="text-align:center"><img src="http://'+str(list_game[i][0])+'_100.jpg"/></td>'+'<td><a href="'+PAGE+str(list_game[i][1])+'">'+list_game[i][2]+"</a></td>"+"<td style ='text-align:center'>"+str(list_game[i][3])+"%</td>"+"<td style ='text-align:center'>"+str(list_game[i][4])+"</td>"
		file.write("<tr style='border:solid 1px grey;'>"+str(list_item)+"</tr>\n")
	file.write("</table>")
	file.close()

if __name__ == "__main__":
   main(sys.argv)