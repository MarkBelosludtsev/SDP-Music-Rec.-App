import gensim

def make_playlist(seed_tracks):

    if seed_tracks:
        # CURRENTLY NO MODEL
        model = gensim.models.Word2Vec.load('word2vec.model')
        num_tracks = 100
        seed_window = num_tracks
        for i in range(0, num_tracks - len(seed_tracks)):
            next_track = model.wv.most_similar(positive=seed_tracks[-seed_window:], topn=1)
            if next_track == None:
                break
            seed_tracks.append(next_track[0][0])
        return seed_tracks
    
    else:
        return None