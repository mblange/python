class Song(object):

    def __init__(self, lyrics):
        self.foo = lyrics

    def sing_me_a_song(self):
        for line in self.foo:
            print line

happy_bday = Song(["Happy birthday to you",
			"I don't want to get sued",
			"So I'll stop right there"])

bulls_on_parade = Song(["They rally around tha family",
			"With pockets full of shells"])

a = ["in the", "garden of", "eden, baby"]
b = ["son, she said,", "have i got", "a little story for you"]

a_song = Song(a)

b_song = Song(b)

happy_bday.sing_me_a_song()

bulls_on_parade.sing_me_a_song()

a_song.sing_me_a_song()
b_song.sing_me_a_song()

a_lyric = a_song.foo

print a_lyric[2]
