from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post(blog_post):
    missing_fields = []
    if "title" not in blog_post:
        missing_fields.append("title")
    if "content" not in blog_post:
        missing_fields.append("content")
    return missing_fields


def validate_sorting_params(sort_by, sorting_direction):
    invalid_params = []
    if sort_by not in ("title", "content", None):
        invalid_params.append(sort_by)
    if sorting_direction not in ("asc", "desc", None):
        invalid_params.append(sorting_direction)
    return invalid_params


def find_post_by_id(post_id):
    return next((post for post in POSTS if post.get("id") == post_id), None)


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
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
        sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=reverse)
    elif direction == "desc":
        # no sort field given, but direction is "desc" -> sort by ID descending
        sorted_posts = sorted(POSTS, key=lambda x: x["id"], reverse=True)
    else:
        # no sort field given, but direction is "asc" -> original order is already ascending
        return jsonify(POSTS)
    return jsonify(sorted_posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PATCH'])
def edit_post(post_id):
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
        if "title" in updated_post:
            post["title"] = updated_post["title"]
        if "content" in updated_post:
            post["content"] = updated_post["content"]
        return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_for_posts():
    title = request.args.get("title")
    content = request.args.get("content")
    matching_posts = []
    for post in POSTS:
        if title and title not in post.get("title", ""):
            continue
        if content and content not in post.get("content", ""):
            continue
        matching_posts.append(post)
    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
