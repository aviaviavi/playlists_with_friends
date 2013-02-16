from pyechonest import config, catalog, artist
from StringIO import StringIO
import pycurl

config.ECHO_NEST_API_KEY="8IOOXXQIU4NHRY5DY"

#create a new user taste profile
# curl -F "api_key=FILDTEOIK2HBORODV" -F "format=json" -F "type=artist" 
# -F "name=test_artist_catalog" "http://developer.echonest.com/api/v4/catalog/create"
# def create_new_profile(name):
# 	storage = StringIO()
# 	c = pycurl.Curl()
# 	c.setopt(c.URL, 'http://developer.echonest.com/api/v4/catalog/create')
# 	c.setopt(c.WRITEFUNCTION, storage.write)
# 	c.setopt(c.POSTFIELDS, 'api_key={0}&format=json&type=artist&name={1}'.format(config.ECHO_NEST_API_KEY, name))
# 	c.setopt(c.VERBOSE, True)
# 	c.perform()
# 	c.close()
# 	return storage.getvalue()

def create_new_profile(name):
	c = catalog.Catalog(name, 'general')
	print 'got it'
	return c

class User:
	def __init__(self, name):
		self.catalog = create_new_profile(name)
		self.cat_id = self.catalog.id
		self.name = name
		self.item_id = 0
	def delete(self):
		self.catalog.delete()
	def add_artist(self, artist_name):
		artist_object = artist.Artist(artist_name)
		item = [{ 'item':
			{
				'item_id' : str(self.item_id),
				'artist_name' : artist_object.name
			}
		}]
		self.catalog.update(item)
		self.item_id += 1
