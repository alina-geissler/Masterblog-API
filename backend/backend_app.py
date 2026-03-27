from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post(blog_post):
    """
    Check that a blog post contains all required fields.

    :param blog_post: dict – the post data to validate
    :return: list of missing field names, empty if valid
    """
    missing_fields = []
    if "title" not in blog_post:
        missing_fields.append("title")
    if "content" not in blog_post:
        missing_fields.append("content")
    return missing_fields


def validate_sorting_params(sort_by, sorting_direction):
    """
    Check that sorting parameters contain only accepted values.

    :param sort_by: str or None – field to sort by ('title', 'content')
    :param sorting_direction: str or None – sort order ('asc', 'desc')
    :return: list of invalid parameter values, empty if valid
    """
    invalid_params = []
    if sort_by not in ("title", "content", None):
        invalid_params.append(sort_by)
    if sorting_direction not in ("asc", "desc", None):
        invalid_params.append(sorting_direction)
    return invalid_params


def find_post_by_id(post_id):
    """
    Find a post in POSTS by its ID.

    :param post_id: int – the ID to search for
    :return: post dict if found, None otherwise
    """
    return next((post for post in POSTS if post.get("id") == post_id), None)


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """
    Handle GET and POST requests for /api/posts.

    POST: Create a new post. Requires 'title' and 'content' in request body.
          Returns created post with status 201 on success.
          Returns 400 if fields are missing.

    GET:  Return all posts as JSON. Supports optional query parameters:
          - sort: 'title' or 'content'
          - direction: 'asc' (default) or 'desc'
          Returns unsorted posts if no parameters are provided.
          Returns sorted posts if valid parameters are provided.
          Returns 400 if parameters are invalid.
    """
    if request.method == 'POST':
        new_post = request.get_json()
        # validate that required fields are present
        missing_fields = validate_post(new_post)
        if missing_fields:
            return jsonify({"error": "missing fields", "fields": missing_fields}), 400
        # generate a new unique ID (default=0 prevents crash if list is empty)
        new_id = max((post.get("id") for post in POSTS), default=0) + 1
        new_post["id"] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    # no params provided -> return posts in original order
    if not sort and not direction:
        return jsonify(POSTS)
    # reject invalid sort/ direction values before processing
    invalid_params = validate_sorting_params(sort, direction)
    if invalid_params:
        return jsonify({"error": "invalid sorting parameters", "parameters": invalid_params}), 400
    if sort:
        # sort by given field; reverse=True only if direction is explicit "desc"
        reverse = direction == "desc"
        sorted_posts = sorted(POSTS, key=lambda x: x.get(sort, ""), reverse=reverse)
    elif direction == "desc":
        # no sort field given, but direction is "desc" -> sort by ID descending
        sorted_posts = sorted(POSTS, key=lambda x: x.get("id", ""), reverse=True)
    else:
        # no sort field given, but direction is "asc" -> original order is already ascending
        return jsonify(POSTS)
    return jsonify(sorted_posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PATCH'])
def edit_post(post_id):
    """
    Handle PATCH and DELETE requests for /api/posts/<post_id>.

    DELETE: Remove the post with the given ID.
            Returns confirmation message on success.
    PATCH:  Update 'title' and/or 'content' of the post with the given ID.
            Returns updated post on success.
            Returns 400 if no data is provided.

    :param post_id: int – ID of the post to edit or delete
    """
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": f"No post with ID {post_id} found."}), 404
    if request.method == 'DELETE':
        POSTS.remove(post)
        return jsonify({f"message": f"Post with ID {post_id} has been deleted successfully."})
    else:
        updated_post = request.get_json()
        if not updated_post:
            return jsonify({"error": "No data provided."}), 400
        if "title" not in updated_post and "content" not in updated_post:
            return jsonify({"error": "No valid fields provided."}), 400
        if "title" in updated_post:
            post["title"] = updated_post["title"]
        if "content" in updated_post:
            post["content"] = updated_post["content"]
        return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_for_posts():
    """
    Search posts by title and/or content (case-insensitive substring match).

    Query parameters (both optional):
    - title: filter posts containing this string in the title
    - content: filter posts containing this string in the content

    :return: list of matching posts as JSON, empty if no match found
    """
    title = request.args.get("title")
    content = request.args.get("content")
    matching_posts = []
    for post in POSTS:
        if title and title.lower() not in post.get("title", "").lower():
            continue
        if content and content.lower() not in post.get("content", "").lower():
            continue
        matching_posts.append(post)
    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
