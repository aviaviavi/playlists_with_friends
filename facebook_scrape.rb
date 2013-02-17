require 'koala'
oauth_access_token =
@graph = Koala::Facebook::API.new(oauth_access_token)

out = []
music_likes = @graph.get_connections("me", "music")
for index in 0..music_likes.length - 1
	out.push(music_likes[index]["name"])
end

puts(out)
