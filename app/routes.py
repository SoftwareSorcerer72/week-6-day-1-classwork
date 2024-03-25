from flask import request
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


# Create a Post
@app.route('/posts', methods=['POST'])
def create_post():
    # Check to see if the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    # For each of the required fields
    for field in required_fields:
        # If the field is not in the request body dictionary
        if field not in data:
            # Add that field to the list of missing fields
            missing_fields.append(field)
    # If there are any missing fields, return 400 status code with the missing fields listed
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get data values
    title = data.get('title')
    body = data.get('body')

    # Create a new post dictionary with data
    new_post = {
        'id': len(post_data) + 1,
        'title': title,
        'body': body,
        'userId': 1,
        'dateCreated': '2024-03-25T15:21:35',
        'likes': 0
    }

    # Add the new post to storage (post_data -> will be db tomorrow)
    post_data.append(new_post)

    # Return the newly created post dictionary with a 201 Created Status Code
    return new_post, 201
