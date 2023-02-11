from bs4 import BeautifulSoup
import requests
import urllib
import urllib.parse
import time
def GetRecipeURL(name, genre, scene):

  name, genre, scene = name, genre, scene = str(name), str(genre), str(scene)
  x = name + ' ' + genre + ' ' + scene
  name_quote = urllib.parse.quote(x)
   
  base_url = 'https://recipe.rakuten.co.jp/search/' + name_quote
  print(base_url)
  response = requests.get(base_url)
   
  response.encoding = response.apparent_encoding
  
  bs = BeautifulSoup(response.text, 'html.parser')
 
  li_tag_list = bs.find_all('li', class_='recipe_ranking__item', limit=3) 
 
  global url_list
  url_list = []
 
  for li_tag in li_tag_list:
      for a_tag in li_tag.find_all('a'):
        href = a_tag.attrs['href']
        url = 'https://recipe.rakuten.co.jp/' + href
        url_list.append(url)
    
  global recipe_name_list
  recipe_name_list = []
  for li_tag_name in li_tag_list:
      for span_tag in li_tag_name.find_all('span', class_='recipe_ranking__recipe_title omit_2line'):
        recipe_name_list.append(span_tag.get_text())
  global recipe_img_list
  recipe_img_list = []
  for li_tag_img in li_tag_list:
      for img_tag in li_tag_img.find_all('img'):
        img_url = img_tag.attrs['src']
        recipe_img_list.append(img_url)

  global time_list
  time_list = []
  for all_recipe in url_list:

      base_url =  all_recipe
      response = requests.get(base_url)
      response.encoding = response.apparent_encoding
      bs = BeautifulSoup(response.text, 'html.parser')

      data_count = []
      recipe_data_set = []

      time = bs.find('li', class_= 'recipe_info_text__note_item recipe_info__time')
      time1 = time.text.replace('\n', '').replace(' ', '')
      time_list.append(time1)

  return url_list, recipe_name_list, recipe_img_list, time_list
  time.sleep(1)

#--------------------------------------#