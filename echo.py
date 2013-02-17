from pyechonest import *
from StringIO import StringIO
import pickle

config.ECHO_NEST_API_KEY="8IOOXXQIU4NHRY5DY"

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
		self.plist = None

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

	def make_playlist(self):
		if self.plist:
			self.plist.delete()
		self.plist = playlist.Playlist(type='catalog-radio', seed_catalog=self.cat_id)
		out = []
		for i in range(5):
			out.append(self.plist.get_next_songs(1))
		return out

	def edit_playlist(self, playlist):
		return 0

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

	def print_catalog(self):
		print self.catalog.get_item_dicts()

class ExistingUser(User):
	def __init__(self, name):
		self.cat_id = user_info[name]
		self.name = name
		self.catalog = catalog.Catalog(self.cat_id)
		self.item_id = len(self.catalog.get_item_dicts())
		self.plist = None

class SuperUser(User):
    def __init__(self, name): # list of catalogs
        self.catalog = create_new_profile(name)
        self.cat_id = self.catalog.id
        self.id_track = 0
        self.plist = None
    def addCatalog(self,catalog):
        for item in catalog.get_item_dicts(results=100):
            self.catalog.update([{'action':'update','item':item['request']}])
            self.i = int(item['request']['item_id'])
            item['request']['item_id'] = unicode(self.i+self.id_track)
        self.id_track += len(catalog.get_item_dicts(results=100))

avi = ExistingUser('avi')
oren = ExistingUser('oren')

us = SuperUser('us')
avi.add_artist('Tool')
us.addCatalog(avi.catalog)
us.addCatalog(oren.catalog)
print us.make_playlist()