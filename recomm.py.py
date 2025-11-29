import math

movies = [
    {"id": 1, "title": "The Matrix", "genres": ["Action", "Sci-Fi"], "tags": ["robots", "future", "virtual"]},
    {"id": 2, "title": "John Wick", "genres": ["Action", "Thriller"], "tags": ["hitman", "revenge", "guns"]},
    {"id": 3, "title": "Interstellar", "genres": ["Sci-Fi", "Drama"], "tags": ["space", "time", "family"]},
    {"id": 4, "title": "The Notebook", "genres": ["Romance", "Drama"], "tags": ["love", "relationship", "tearjerker"]},
    {"id": 5, "title": "Inception", "genres": ["Action", "Sci-Fi"], "tags": ["dream", "heist", "mind"]},
    {"id": 6, "title": "La La Land", "genres": ["Romance", "Musical"], "tags": ["music", "love", "dreams"]},
]

def build_vocabulary(items):
    vocab = []
    for item in items:
        for g in item["genres"]:
            if g not in vocab:
                vocab.append(g)
        for t in item["tags"]:
            if t not in vocab:
                vocab.append(t)
    return vocab

vocabulary = build_vocabulary(movies)

def movie_to_vector(movie, vocab):
    vector = []
    for term in vocab:
        if term in movie["genres"] or term in movie["tags"]:
            vector.append(1)
        else:
            vector.append(0)
    return vector

movie_vectors = {}
for m in movies:
    movie_vectors[m["id"]] = movie_to_vector(m, vocabulary)

def cosine_similarity(a, b):
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))

def build_user_profile(liked_movie_ids, movie_vecs, vocab):
    profile = [0.0] * len(vocab)
    if not liked_movie_ids:
        return profile
    for movie_id in liked_movie_ids:
        vec = movie_vecs[movie_id]
        for i in range(len(vec)):
            profile[i] += vec[i]
    count = float(len(liked_movie_ids))
    for i in range(len(profile)):
        profile[i] = profile[i] / count
    return profile

def recommend_movies(liked_movie_ids, all_movies, movie_vecs, vocab, top_n=3):
    user_profile = build_user_profile(liked_movie_ids, movie_vecs, vocab)
    scores = []
    for m in all_movies:
        if m["id"] in liked_movie_ids:
            continue
        vec = movie_vecs[m["id"]]
        sim = cosine_similarity(user_profile, vec)
        scores.append((m, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

def ask_user_likes():
    print("Available movies:")
    for m in movies:
        print(f"{m['id']}: {m['title']} ({', '.join(m['genres'])})")
    print()
    raw = input("Enter the IDs of movies you like (comma separated): ")
    parts = raw.split(",")
    liked = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if not p.isdigit():
            continue
        mid = int(p)
        # check if id exists
        if any(m["id"] == mid for m in movies):
            liked.append(mid)
    liked = list(set(liked))
    return liked

if __name__ == "__main__":
    print("Simple Movie Recommendation System")
    liked_ids = ask_user_likes()

    if not liked_ids:
        print("You did not enter any valid movie IDs. Exiting.")
    else:
        recs = recommend_movies(liked_ids, movies, movie_vectors, vocabulary, top_n=3)
        print("\nYou like:")
        for m in movies:
            if m["id"] in liked_ids:
                print(f"- {m['title']}")
        print("\nRecommended for you:")
        if not recs:
            print("No recommendations found.")
        else:
            for movie, score in recs:
                print(f"- {movie['title']} (score: {score:.3f})")
