#%%
import requests

#%%
r = requests.get('https://www.comuniate.com/jugadores/415/raul-garcia')

#%%
r.text

#%%
from bs4 import BeautifulSoup

#%%
b = BeautifulSoup(r.text, 'html.parser')

#%%
comentario = b.select_one('small > p')

#%%
comentario.