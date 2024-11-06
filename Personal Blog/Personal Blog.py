
#home page - list all articles displayed on the blog, 
# Article page - display content of article along with date of publishing
# Dashboard - display list of articles published on the blog along with  option to add a new article, edit an existing article, or delete an article.
# Add Article Page - Contain a form to add a new article, edit existing article, or delete an article
# Edit article page - edit existing article, fields like title, content, date of publication.

#TODO; STORAGE

#TODO: FLASK ROUTINg

import json, os, copy
from send2trash import send2trash 
from flask import Flask, request, Response, render_template
article_dir = (r'G:\01101000111101\Programming\Projects\Backend Projects\Personal Blog\articles')
#change directory to where your articles folder is located. 


USERNAME = 'admin'
PASSWORD = 'password'
filepath_list = []

app = Flask(__name__)

def check_auth(username, password):

    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Could not verify! Please provide valid credentials.',401, {'WWW-Authenticate' : 'Basic realm = "Login Required"'})

@app.route('/article/<int:id>', methods = ['GET', 'POST'])
def article_page(id):


    return render_template('article.html', article_nested_dict = article_nested_dict, id = id)

def ArticleUpdate():

    global article_nested_dict 
    global article_title_list
    article_title_list = []
    article_nested_dict = {}
    x = 0

    for  folder, subfolders, files in os.walk(article_dir):
            
            if files != []:
                filepath = os.path.join(folder, files[0])
                x += 1
                filepath_list.append(filepath)


                with open(filepath, 'r') as jsonfile:
                    article_json = json.load(jsonfile)
                    article_nested_dict[x] = article_json
                    article_title_list.append(article_json['title'])

@app.route('/')
def home():

    if request.method == 'GET':
        ArticleUpdate()

        
    return render_template('home.html', article_nested_dict = article_nested_dict, article_title_list = article_title_list)


@app.route('/dashboard')
def dashboard():
    auth = request.authorization

    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    
    if request.method == 'GET':
        ArticleUpdate()
    

    return render_template('dashboard.html', article_nested_dict = article_nested_dict, article_title_list = article_title_list)

@app.route('/delete/<int:id>', methods = ['GET','POST'])
def delete_page(id):

    with open (filepath_list[id - 1], 'r') as jsonread:
        article_json = json.load(jsonread)

    if request.method == 'POST':
        ArticleDelPath = r'\Article' +  ' ' + str(id)
        send2trash(article_dir + ArticleDelPath)


    return render_template('delete.html', article_nested_dict = article_nested_dict, article_json = article_json, id = id)

    

@app.route('/add', methods = ['POST', 'GET'])
def add_page():

    new_article = {}

    if request.method == 'POST':

        TitleEdit = request.form.get('Article_Title')
        PublishingDateEdit = request.form.get('Publishing_Date')
        ContentEdit = request.form.get('Content')

        new_article['title'] = TitleEdit
        new_article['Date'] = PublishingDateEdit
        new_article['Content'] = ContentEdit
        new_article['id'] = len(article_nested_dict) + 1
        jsonConv = json.dumps(new_article) 
        NewArticleName = r'\article' + str(len(article_nested_dict)+1) + '.json'


        new_article_folder = '\Article' + ' ' + str(len(article_nested_dict)+1)
        new_directory = article_dir + new_article_folder

        os.mkdir(new_directory)

        with open (new_directory + NewArticleName, 'w') as file:
            file.write(jsonConv)

    
    return render_template('add.html')

@app.route('/edit_page/<int:id>', methods = ['POST', 'GET'])
def edit_page(id):

    with open (filepath_list[id - 1], 'r') as jsonread:
        article_json = json.load(jsonread)


    if request.method == 'POST':

        TitleEdit = request.form.get('Article_Title')
        PublishingDateEdit = request.form.get('Publishing_Date')
        ContentEdit = request.form.get('Content')

        UpdatedArticle = copy.deepcopy(article_nested_dict[id])  
        UpdatedArticle['title'] = TitleEdit
        UpdatedArticle['Date'] = PublishingDateEdit
        UpdatedArticle['Content'] = ContentEdit

        ArticleStr = 'article' + str(UpdatedArticle['id'])+ '.json'

        jsonConv = json.dumps(UpdatedArticle)

        for  folder, subfolders, files in os.walk(article_dir):
                
                if files != []:
                    if files[0] == ArticleStr:
                        filepath = os.path.join(folder, ArticleStr)
                        with open (filepath, 'w') as jsonfile:
                            jsonfile.write(jsonConv)

        article_json = UpdatedArticle


    return render_template('edit.html', article_json = article_json, article_nested_dict = article_nested_dict, id = id)


if __name__ == '__main__':
    app.run(debug=True)



#TODO = Fix formatting to match edit article page