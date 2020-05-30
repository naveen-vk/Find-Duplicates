import string
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import time
import pandas

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


def compute_execution_time(questions_data):
    print('Questions Count: ' + str(len(questions_data)))
    start = time.time()
    find_duplicates(questions_data)
    end = time.time()
    print('Time elapsed:' + time.strftime("%H:%M:%S", time.gmtime(end - start)))

colnames = ['Id', 'OwnerUserId', 'CreationDate', 'ClosedDate', 'Score', 'Title', 'Body']
data = pandas.read_csv('Questions.csv', names=colnames,
                       encoding='latin-1')
print('Total Data: ' + str(len(data)))
questions_data = data.Title.to_list()

# hundred questions
compute_execution_time(questions_data[0:100])
# thousand questions
compute_execution_time(questions_data[0:1000])
# ten thousand questions
compute_execution_time(questions_data[0:10000])
# hundred thousand questions
compute_execution_time(questions_data[0:100000])
# 1 million questions
compute_execution_time(questions_data[0:1000000])
