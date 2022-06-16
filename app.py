from flask import Flask, render_template,request
import pickle
import numpy as np

popular_top_50 = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
new_data = pickle.load(open('new_data.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular_top_50['Book-Title'].values),
                            author = list(popular_top_50['Book-Author'].values),
                            image = list(popular_top_50['Image-URL-M'].values),
                            votes = list(popular_top_50['rating_count'].values),
                            rating =list(popular_top_50["rating_avg"].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods =['post'])
def recommend():
    user_input = request.form.get('user_input')
    index1 = np.where(new_data.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index1])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == new_data.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
