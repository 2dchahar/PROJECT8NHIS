from flask import Flask, request, jsonify
from engine import get_job_recommendations  # Import your "brain"

# Initialize the Flask application
app = Flask(__name__)

# --- Define the API Endpoint ---
# This tells Flask that anyone visiting '/recommend' will trigger this function
@app.route('/recommend', methods=['GET'])
def recommend():
    # 1. Get the 'title' from the URL query (e.g., .../recommend?title=Developer)
    job_title = request.args.get('title')

    # 2. Check if the 'title' parameter was provided
    if not job_title:
        # Return an error message and a 400 'Bad Request' status
        return jsonify({"error": "Missing 'title' query parameter"}), 400

    # 3. Call your engine's function to get recommendations
    results = get_job_recommendations(job_title)

    # 4. Check if the engine returned an error (like 'job not found')
    if 'error' in results:
        # Return the error and a 404 'Not Found' status
        return jsonify(results), 404
    
    # 5. Return the successful results as JSON
    return jsonify(results)

# --- Run the Flask App ---
if __name__ == '__main__':
    # host='0.0.0.0' allows the container to be accessed from outside
    app.run(debug=False, host='0.0.0.0', port=5000)