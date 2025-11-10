import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading data and building recommendation model...")

# --- 1. Load and Prepare Data ---
try:
    # Load the data from the CSV
    df = pd.read_csv("D:\Project8\DataSet.csv")
except FileNotFoundError:
    print("Error: 'DataSet.csv' not found. Make sure it's in the same folder.")
    exit()

# Clean data: drop rows with no title and remove duplicate titles
df_rec = df.dropna(subset=['title']).drop_duplicates(subset=['title'])

# --- 2. Build the Model (from Task 5) ---

# Initialize TF-IDF Vectorizer. This converts text titles into numerical features.
tfidf = TfidfVectorizer(stop_words='english')

# Create the TF-IDF matrix by fitting and transforming the 'title' data
tfidf_matrix = tfidf.fit_transform(df_rec['title'])

# Compute the cosine similarity matrix
# This matrix (cosine_sim) contains the similarity score between all job titles
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a mapping from job titles to their index in the DataFrame
# This allows us to quickly find a job by its title
indices = pd.Series(df_rec.index, index=df_rec['title'])

print("Model built successfully.")

# --- 3. Create the Recommendation Function ---

def get_job_recommendations(title):
    """
    Finds a job by title and returns the top 10 most similar jobs.
    """
    try:
        # Get the index of the job that matches the title
        idx = indices[title]
    except KeyError:
        # Handle case where the job title is not in our dataset
        return {"error": f"Job title '{title}' not found in the dataset."}

    # Get the pairwise similarity scores of all jobs with that job
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the jobs based on the similarity scores (in descending order)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar jobs (skip the first one, as it is the job itself)
    sim_scores = sim_scores[1:11]

    # Get the job indices from the similarity scores
    job_indices = [i[0] for i in sim_scores]

    # Get the titles and links of the recommended jobs
    recommendations = df_rec.iloc[job_indices][['title', 'link']]

    # Return the recommendations as a list of dictionaries (which is easy to convert to JSON)
    return recommendations.to_dict('records')