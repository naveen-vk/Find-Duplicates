from flask import Flask, render_template, request, redirect
import string
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
app = Flask(__name__)

@app.route("/")
def home_view():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def handle_data():
    results = {}
    selected_option = 0
    if request.form['questions'] and request.form['selected_option']:
        input_data = request.form['questions'].splitlines()
        results = find_duplicates(input_data)
        selected_option = request.form['selected_option']
        # filter based on selected option
        results = list(filter(lambda x: x['similarity_percentage'] == int(selected_option), results.values()))
    return render_template('result.html', len=len(results), results=results, selected_option=selected_option)

@app.route("/", methods=['POST'])
def redirect_to_home_view():
    return redirect("/")

def clean_text(data):
    # remove html tags
    data = BeautifulSoup(data, "html.parser").text
    # remove punctuations
    data = ''.join([word for word in data if word not in string.punctuation])
    return data

def round_to_nearest_multiple_of_10(n):
    # Smaller multiple
    a = (n // 10) * 10
    # Larger multiple
    b = a + 10
    # Return of closest of two
    return b if n - a > b - n else a

def find_duplicates(input_data):
    cleaned = list(map(clean_text, input_data))
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)

    result = {}
    result_count = 0

    rows = len(csim)
    columns = len(csim[0])
    for i in range(0, rows):
        for j in range(0, columns):
            # fetch only upper triangular matrix
            if i != j and i < j:
                result[result_count] = {}
                result[result_count]['original_string'] = input_data[i]
                result[result_count]['compared_string'] = input_data[j]
                result[result_count]['similarity_percentage'] = round_to_nearest_multiple_of_10(
                    int(round(csim[i][j], 2) * 100))
                result_count = result_count + 1
    return result
