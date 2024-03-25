from . import app
from fake_data.posts import post_data

# Define a route
@app.route("/")
def index():
    first_name = 'Brian'
    age = 55
    return 'Hello ' + first_name + ' who is ' + str(age) + ' years old'


# Post Endpoints

# Get All Posts
@app.route('/posts')
def get_posts():
    # Get the posts from storage (fake data -> tomorrow will be db)
    posts = post_data 
    return posts