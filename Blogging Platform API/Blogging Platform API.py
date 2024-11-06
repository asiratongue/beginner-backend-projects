from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime

x = 0
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file.db'
db = SQLAlchemy(app)

#handle errors gracefully
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "The requested resource was not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "an internal server error occurred"}), 500

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "You don't have permission to access this resource"})


# create table columns with an SQL object
class BlogPost(db.Model):

    id_sq = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(8000))
    tag = db.Column(db.String(80), unique=False, nullable =True)
    CreatedAt = db.Column(db.DateTime, default=datetime.datetime.now)
    LastUpdatedAt = db.Column(db.DateTime, onupdate=datetime.datetime.now)

with app.app_context():
    db.create_all()


#main route for CRUD operations
@app.route('/posts/<int:idx>', methods = {"POST", "GET", "PUT", "DELETE"})
def posts_int_endpoint(id):

    # MUST send request with article in json format, correct keys.
    if request.method == "POST":
        data = request.get_json(force=True)
        post = BlogPost(id_sq = id , title = data['title'], content = data['content'], tag = data['tag']) # convert json input into a blogpost object, attributes stored as cells in sql.
        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "Post created successfully", 
                        "post": {"id": post.id_sq, "title": post.title, "content" : post.content, 
                                    "tag" : post.tag, "CreatedAt" : post.CreatedAt, "LastUpdatedAt" : post.LastUpdatedAt}}), 201

    if request.method == "GET":
        SelectedArticle = BlogPost.query.filter(BlogPost.id_sq == id).all()
        post_list = [
        {
            "id": post.id_sq,
            "title": post.title,
            "content": post.content,
            "tag": post.tag,
            "created_at": post.CreatedAt,
            "last_updated_at": post.LastUpdatedAt
        }
        for post in SelectedArticle

        ]

        return jsonify(post_list)

    if request.method == "DELETE":
       SelectedArticle = BlogPost.query.filter(BlogPost.id_sq == id).all()

       for post in SelectedArticle:
            db.session.delete(post)

       db.session.commit()

       return f"post{id} deleted."
    
    if request.method == "PUT":
        article2update = BlogPost.query.filter(BlogPost.id_sq == id).first()
        data2 = request.get_json(force=True)

        article2update.title = data2['title']
        article2update.content = data2['content'] 
        article2update.tag = data2['tag']

        db.session.commit()


        return jsonify({"message": "Post updated successfully", 
                        "post": {"id": article2update.id_sq, "title": article2update.title, "content" : article2update.content, 
                                    "tag" : article2update.tag, "CreatedAt" : article2update.CreatedAt, "LastUpdatedAt" : article2update.LastUpdatedAt}}), 201



@app.route('/posts', methods = {"POST", "GET", "PUT"})
def posts_endpoint():

    if request.method == "GET":
        allPosts = BlogPost.query.all()


        print(allPosts)
    post_list = [
        {
            "id": post.id_sq,
            "title": post.title,
            "content": post.content,
            "tag": post.tag,
            "created_at": post.CreatedAt,
            "last_updated_at": post.LastUpdatedAt
        }
        for post in allPosts
    ]


    return jsonify(post_list)


@app.route('/postsearch', methods = {"GET"})
def search_posts():
    search = request.args.get('term')
    SearchedList = []

    if request.method == "GET":
        CheckAll = BlogPost.query.filter(BlogPost.title.like(f'%{search}%')).all(), BlogPost.query.filter(BlogPost.content.like(f'%{search}%')).all(), BlogPost.query.filter(BlogPost.tag.like(f'%{search}%')).all()
        print(CheckAll)

        def filterFunk(x):
            if x == []:
                return False
            else:
                return True 
            
        SearchedFilter = filter(filterFunk, CheckAll)
        for postlist in SearchedFilter:
            for post in postlist:
                SearchedList.append(post)


        print(SearchedList)
        if CheckAll != ():

            post_list = [
            {
                "id": post.id_sq,
                "title": post.title,
                "content": post.content,
                "tag": post.tag,
                "created_at": post.CreatedAt,
                "last_updated_at": post.LastUpdatedAt
            }
            for post in SearchedList

            ]

            return jsonify("here you go", post_list) 
        else:

            return f"no posts were found to match with {search}"



if __name__ == '__main__':

    app.run(debug=True)


