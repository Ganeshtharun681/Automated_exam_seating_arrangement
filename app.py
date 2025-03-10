from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load movie data from a CSV file
movies = pd.read_csv('/path/to/movies.csv')  # Update this path to your actual movie dataset

@app.route('/')
def index():
    return render_template('js.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    genre = request.args.get('genre')
    recommendations = movies[movies['genre'].str.contains(genre, case=False, na=False)]  # Filter movies by genre
    return jsonify(recommendations=recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
