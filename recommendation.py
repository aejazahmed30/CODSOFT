
import math
import tkinter as tk
from tkinter import messagebox


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


def get_selected_movie_ids():
    selected_indices = listbox_likes.curselection()
    ids = []
    for idx in selected_indices:
        movie = movies[idx]
        ids.append(movie["id"])
    return ids

def on_recommend():
    liked_ids = get_selected_movie_ids()
    if not liked_ids:
        messagebox.showinfo("Info", "Please select at least one movie you like.")
        return

    recs = recommend_movies(liked_ids, movies, movie_vectors, vocabulary, top_n=3)

   
    text_output.config(state="normal")
    text_output.delete("1.0", tk.END)

    text_output.insert(tk.END, "You like:\n")
    for m in movies:
        if m["id"] in liked_ids:
            text_output.insert(tk.END, f"- {m['title']}\n")

    text_output.insert(tk.END, "\nRecommended for you:\n")
    if not recs:
        text_output.insert(tk.END, "No recommendations found.\n")
    else:
        for movie, score in recs:
            text_output.insert(tk.END, f"- {movie['title']} (score: {score:.3f})\n")

    text_output.config(state="disabled")


root = tk.Tk()
root.title("Simple Movie Recommender")
root.geometry("500x400")

label_select = tk.Label(root, text="Select movies you like (Ctrl+Click for multiple):")
label_select.pack(pady=5)


listbox_likes = tk.Listbox(root, selectmode=tk.MULTIPLE, height=8)
for m in movies:
    listbox_likes.insert(tk.END, f"{m['title']} ({', '.join(m['genres'])})")
listbox_likes.pack(fill=tk.X, padx=10, pady=5)

btn_recommend = tk.Button(root, text="Recommend", command=on_recommend)
btn_recommend.pack(pady=10)

label_output = tk.Label(root, text="Output:")
label_output.pack()

text_output = tk.Text(root, height=10, state="disabled")
text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
