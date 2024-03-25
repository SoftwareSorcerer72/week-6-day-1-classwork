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


# Get a Single Post By ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the posts from storage
    posts = post_data
    # For each dictionary in the list of post dictionaries
    for post in posts:
        # If the key of 'id' matches the post_id from the URL
        if post['id'] == post_id:
            # Return that post dictionary
            return post
    # If we loop through all of the posts without returning, the post with that ID does not exist
    return {'error': f"Post with an ID of {post_id} does not exist"}, 404
