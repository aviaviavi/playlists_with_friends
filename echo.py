from pyechonest import config, catalog, artist, song
from StringIO import StringIO
import pycurl
import pickle

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
pkl_file = open('user_info.pkl', 'r')
user_info = pickle.load(pkl_file)
pkl_file.close()

def create_new_profile(name):
	c = catalog.Catalog(name, 'general')
	return c

class User:
	def __init__(self, name):
		self.catalog = create_new_profile(name)
		self.cat_id = self.catalog.id
		self.name = name
		self.item_id = 0
		user_info[self.name] = str(self.cat_id)
		pkl_file = open('user_info.pkl', 'w')
		pickle.dump(user_info, pkl_file)
		pkl_file.close()

	def delete(self):
		self.catalog.delete()
		del(user_info[self.name])
		pkl_file = open('user_info.pkl', 'w')
		pickle.dump(user_info, pkl_file)
		pkl_file.close()

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

	def add_song(self, song_name, artist_name):
		songID = song.search(title=song_name, artist=artist_name)[0].id
		song_object = song.Song(songID)
		item = [{'item':
			{
				'item_id':str(self.item_id),
				'song_name': song_object.title
			}
		}]
		self.catalog.update(item)
		self.item_id+=1

class ExistingUser(User):
	def __init__(self, name):
		self.cat_id = user_info[name]
		self.name = name
		self.catalog = catalog.Catalog(self.cat_id)
		self.item_id = len(self.catalog.get_item_dicts())

avi = ExistingUser('avi')
