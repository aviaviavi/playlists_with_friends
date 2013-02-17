from pyechonest import *
from StringIO import StringIO
import pickle
import facebook
import pycurl

config.ECHO_NEST_API_KEY="8IOOXXQIU4NHRY5DY"

pkl_file = open('user_info.pkl', 'r')
user_info = pickle.load(pkl_file)
pkl_file.close()

def get_spotify_id(spot_song):
	out = spot_song.get_tracks('spotify-WW')[0]['foreign_id'][17:]
	#print(out)
	return out
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
		out = []
		for i in range(5):
			out.append(self.plist.get_next_songs(1))
		return out

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

	def get_fb_likes(self):
		graph = facebook.GraphAPI(oauth_access_token)
		music = graph.get_connections("me", "music")
		for band in music:
			try:
				self.add_artist(band)
				print band['name'] + " added!"
			except:
				continue
	def playPlaylist(self):
		playlist = self.make_playlist()
		out = ''
		for songList in playlist:
			spotID = get_spotify_id(songList[0])
			out += spotID
			out+=','

		return out[:-1]
		

class ExistingUser(User):
	def __init__(self, name):
		try:
			self.cat_id = user_info[name]
			self.name = name
			self.catalog = catalog.Catalog(self.cat_id)
			self.item_id = len(self.catalog.get_item_dicts())
			self.plist = None
		except:
			print 'user not found'

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
print(oren.playPlaylist())

"http://developer.echonest.com/api/v4/song/search?api_key={0}&format=json&results=1&artist=radiohead&title=karma%20police&bucket=id:spotify-WW&bucket=tracks&limit=true"
 	 	
