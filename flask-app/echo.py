from pyechonest import *
from StringIO import StringIO
import pickle
import facebook
#import pycurl
from Queue import Queue

config.ECHO_NEST_API_KEY="8IOOXXQIU4NHRY5DY"

# pkl_file = open('user_info.pkl', 'r')
# user_info = pickle.load(pkl_file)
# pkl_file.close()

def get_spotify_id(spot_song):
	out = spot_song.get_tracks('spotify-WW')[0]['foreign_id'][17:]
	#print(out)
	return out
def create_new_profile(name):
	c = catalog.Catalog(name, 'general')
	return c

class User:

	def __init__(self, name, catalog=None):
		if not catalog:
			self.catalog = create_new_profile(name)
			self.item_id = 0
		else:
			self.catalog = catalog
			self.item_id = len(self.catalog.get_item_dicts())
		self.cat_id = self.catalog.id
		self.name = name
		# user_info[self.name] = str(self.cat_id)
		# pkl_file = open('user_info.pkl', 'w')
		# pickle.dump(user_info, pkl_file)
		# pkl_file.close()
		self.plist = None
		# print 'user created!', name

	def delete(self):
		self.catalog.delete()
		del(user_info[self.name])
		# pkl_file = open('user_info.pkl', 'w')
		# pickle.dump(user_info, pkl_file)
		# pkl_file.close()

	def add_artist(self, artist_name):
		try:
			artist_object = artist.Artist(artist_name)
			item = [{ 'item':
				{
					'item_id' : str(self.item_id),
					'artist_name' : artist_object.name
				}
			}]
			self.catalog.update(item)
			self.item_id += 1
		except:
			print 'artist not found'


	def make_playlist(self):
		if self.plist:
			self.plist.delete()
		self.plist = playlist.Playlist(type='catalog-radio', seed_catalog=self.cat_id, buckets=['id:spotify-WW'])
		output = self.plist.get_next_songs(5)
		return output

	def edit_playlist(self, attr):
		if attr == 'dance':
			self.playlist.steer(min_danceability=.5)
		elif attr == 'not_dance':
			self.playlist.steer(max_danceability=.5)
		elif attr == 'energy':
			self.playlist.steer(min_energy=.5)
		elif attr == 'not_energy':
			self.playlist.steer(max_energy=.5)
		elif attr == 'hottt':
			self.playlist.steer(min_hotttnesss=.5)
		elif attr == 'not_hottt':
			self.playlist.steer(max_hotttnesss=.5)
		self.playPlaylist()

	def add_song(self, song_name, artist_name):
		try:
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
		except:
			print 'song not found'

	def print_catalog(self):
		print self.catalog.get_item_dicts()

	def get_fb_likes(self, music_tastes):
		for band in music_tastes['data']:
			try:
				self.add_artist(band['name'])
				print band['name'] + " added!"
			except:
				continue

	def playPlaylist(self):
		playlist = self.plist.get_next_songs(5)
		out = ''
		for songList in playlist:
			spotID = get_spotify_id(songList)
			out += spotID
			out+=','

		return out[:-1]
		

class ExistingUser(User):
	def __init__(self, catalog):		
			# self.name = name
			self.catalog = catalog
			self.cat_id = self.catalog.id
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
            item['request']['item_id'] = str(self.item_id)
            self.add_artist(item['request']['artist_name'])
            self.item_id += 1

