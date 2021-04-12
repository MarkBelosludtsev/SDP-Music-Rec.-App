from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from AI.make_playlist import make_playlist
# from AI.logger import logger
import gensim
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     data_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self): 
#         return '<Task %r>' % self.id

print('loading model...')
model = gensim.models.Word2Vec.load('/home/sam/Desktop/web-server/AI/model/word2vec.model')
print('model loaded.')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return "POST"
    if request.method == 'GET':
        seed_tracks = [request.args.get('s1'), request.args.get('s2'), request.args.get('s3')]
        return jsonify(make_playlist(seed_tracks))
            # [{ "s1": request.args.get('s1'), "s2": request.args.get('s2'), "s3": request.args.get('s3') }])


def make_playlist(seed_tracks):

    if seed_tracks:
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

if __name__ == '__main__':
    app.run()