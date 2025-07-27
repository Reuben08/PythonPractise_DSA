# from gensim.models import KeyedVectors
#
# # Load the provided vector model
# model = KeyedVectors.load_word2vec_format('/Users/reubenharuray/Downloads/reducedvector.bin', binary=True)
# words = [
#     'wife', 'husband', 'child', 'queen', 'king', 'man', 'woman', 'birth',
#     'doctor', 'nurse', 'teacher', 'professor', 'engineer', 'scientist', 'president'
# ]
# import pandas as pd
#
# # Compute similarities
# results = []
# for word in words:
#     try:
#         sim_man = model.similarity('man', word)
#         sim_woman = model.similarity('woman', word)
#         results.append((word, sim_man, sim_woman))
#     except KeyError:
#         results.append((word, 'NA', 'NA'))  # Handle missing words in the vocab
#
# # Convert to DataFrame
# df = pd.DataFrame(results, columns=['Word', 'Similarity to Man', 'Similarity to Woman'])
#
# # Rank by similarity
# df_sorted_man = df.sort_values(by='Similarity to Man', ascending=False).reset_index(drop=True)
# df_sorted_woman = df.sort_values(by='Similarity to Woman', ascending=False).reset_index(drop=True)
#
# print("🔹 Similarity Ranking to 'Man':\n", df_sorted_man)
# print("\n🔹 Similarity Ranking to 'Woman':\n", df_sorted_woman)
#
# from gensim.models import KeyedVectors
# import pandas as pd
#
#
# # Load the Word2Vec model
# model_path = '/Users/reubenharuray/Downloads/reducedvector.bin'  # update this path as needed
# model = KeyedVectors.load_word2vec_format(model_path, binary=True)
#
# # List of singular-plural pairs
# word_pairs = [
#     ("album", "albums"), ("application", "applications"), ("area", "areas"), ("car", "cars"),
#     ("college", "colleges"), ("council", "councils"), ("customer", "customers"), ("day", "days"),
#     ("death", "deaths"), ("department", "departments"), ("development", "developments"),
#     ("difference", "differences"), ("director", "directors"), ("event", "events"),
#     ("example", "examples"), ("fact", "facts"), ("friend", "friends"), ("god", "gods"),
#     ("government", "governments"), ("hour", "hours"), ("idea", "ideas"), ("language", "languages"),
#     ("law", "laws"), ("member", "members"), ("month", "months"), ("night", "nights"),
#     ("office", "offices"), ("period", "periods"), ("player", "players"), ("population", "populations"),
#     ("problem", "problems"), ("product", "products"), ("resource", "resources"), ("river", "rivers"),
#     ("road", "roads"), ("role", "roles"), ("science", "sciences"), ("solution", "solutions"),
#     ("song", "songs"), ("street", "streets"), ("student", "students"), ("system", "systems"),
#     ("thing", "things"), ("town", "towns"), ("user", "users"), ("version", "versions"),
#     ("village", "villages"), ("website", "websites"), ("week", "weeks"), ("year", "years")
# ]
#
# # Compute similarity scores
# results = []
# for singular, plural in word_pairs:
#     if singular in model and plural in model:
#         sim = round(model.similarity(singular, plural), 4)
#     else:
#         sim = 'NA'
#     results.append((singular, plural, sim))
#
# # Create DataFrame
# df = pd.DataFrame(results, columns=['Singular', 'Plural', 'Similarity Score'])
#
# # Display or save
# print(df)
#
# # Optionally save to CSV
# # df.to_csv("singular_plural_similarity_scores.csv", index=False)
#
# # List of analogies to complete using Word2Vec (A is to B as C is to ?)
# analogy_questions = [
#     ("king", "throne", "judge"),      # throne : king :: ? : judge
#     ("giant", "dwarf", "genius"),
#     ("college", "dean", "jail"),
#     ("arc", "circle", "line"),
#     ("french", "france", "dutch"),
#     ("man", "woman", "king"),
#     ("water", "ice", "liquid"),
#     ("bad", "good", "sad"),
#     ("nurse", "hospital", "teacher"),
#     ("usa", "pizza", "japan"),
#     ("human", "house", "dog"),
#     ("grass", "green", "sky"),
#     ("video", "cassette", "computer"),
#     ("universe", "planet", "house"),
#     ("poverty", "wealth", "sickness")
# ]
#
# # Try to find the best analogy completion
# analogy_results = []
# for a, b, c in analogy_questions:
#     try:
#         result = model.most_similar(positive=[b, c], negative=[a], topn=1)[0]
#         predicted_word = result[0]
#         similarity_score = round(result[1], 4)
#     except KeyError:
#         predicted_word = 'NA'
#         similarity_score = 'NA'
#     analogy_results.append({
#         "A": a, "B": b, "C": c,
#         "Predicted Word": predicted_word,
#         "Similarity Score": similarity_score
#     })
#
# # Create and display DataFrame
# analogy_df = pd.DataFrame(analogy_results)
#
# print(analogy_df)
#
# # Optionally save to CSV
# analogy_df.to_csv("analogy_completions.csv", index=False)

# from gensim.models import KeyedVectors
# from docx import Document
#
# # Load the Word2Vec model (adjust the path to your local model file)
# model = KeyedVectors.load_word2vec_format('/Users/reubenharuray/Downloads/reducedvector.bin', binary=True)
#
# # Define analogy questions (A is to B as C is to ?)
# analogy_questions = [
#     ("king", "throne", "judge"),
#     ("giant", "dwarf", "genius"),
#     ("college", "dean", "jail"),
#     ("arc", "circle", "line"),
#     ("french", "france", "dutch"),
#     ("man", "woman", "king"),
#     ("water", "ice", "liquid"),
#     ("bad", "good", "sad"),
#     ("nurse", "hospital", "teacher"),
#     ("usa", "pizza", "japan"),
#     ("human", "house", "dog"),
#     ("grass", "green", "sky"),
#     ("video", "cassette", "computer"),
#     ("universe", "planet", "house"),
#     ("poverty", "wealth", "sickness")
# ]
#
# # Run analogies and collect results
# analogy_sentences = []
# for a, b, c in analogy_questions:
#     try:
#         result = model.most_similar(positive=[b, c], negative=[a], topn=1)[0]
#         predicted_word = result[0]
#         similarity_score = round(result[1], 4)
#         sentence = f"{a} is to {b} as {c} is to {predicted_word} (score: {similarity_score})"
#     except KeyError:
#         sentence = f"{a} is to {b} as {c} is to [Not Available]"
#     analogy_sentences.append(sentence)
#
# # Print results
# for s in analogy_sentences:
#     print(s)
#
# # Write to a Word document
# doc = Document()
# doc.add_heading('Word2Vec Analogy Results', 0)
# for sentence in analogy_sentences:
#     doc.add_paragraph(sentence)
# doc.save("word2vec_analogy_sentences.docx")

# import os
# import pandas as pd
#
# # Path to UTKFace images
# dataset_path = '/Users/reubenharuray/Downloads/crop_part1'
#
# # Parse data from filenames
# data = []
# for filename in os.listdir(dataset_path):
#     if filename.endswith('.jpg'):
#         try:
#             age, gender, race = map(int, filename.split('_')[:3])
#             data.append({'age': age, 'gender': gender, 'race': race})
#         except:
#             continue
#
# df = pd.DataFrame(data)
#
# # Create age bins
# age_bins = [0, 20, 40, 60, 80, 116]
# age_labels = ['0-20', '21-40', '41-60', '61-80', '81-116']
# df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, include_lowest=True)
#
# # Compute frequency per (age group, gender, race)
# subgroup_counts = df.groupby(['age_group', 'gender', 'race']).size().reset_index(name='count')
#
# # Save to CSV or print
# subgroup_counts.to_csv('utkface_subgroup_frequencies.csv', index=False)
# print(subgroup_counts)

import os
import pandas as pd

# Set the correct path to your extracted UTKFace dataset folder
dataset_path = "/Users/reubenharuray/Downloads/crop_part1"

# Read metadata from filenames
data = []
for file in os.listdir(dataset_path):
    if file.endswith(".jpg"):
        try:
            age, gender, race = map(int, file.split('_')[:3])
            data.append({'age': age, 'gender': gender, 'race': race})
        except:
            continue

df = pd.DataFrame(data)

# Define age bins
bins = [0, 20, 40, 60, 80, 116]
labels = ['0-20', '21-40', '41-60', '61-80', '81-116']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, include_lowest=True)

# Create gender table
gender_table = pd.pivot_table(df, values='age', index='gender', columns='age_group', aggfunc='count', fill_value=0)
gender_table['Total'] = gender_table.sum(axis=1)
gender_table.index = gender_table.index.map({0: 'Male', 1: 'Female'})

# Create race table
race_labels = {0: 'White', 1: 'Black', 2: 'Asian', 3: 'Indian', 4: 'Others'}
df['race_label'] = df['race'].map(race_labels)
race_table = pd.pivot_table(df, values='age', index='race_label', columns='age_group', aggfunc='count', fill_value=0)
race_table['Total'] = race_table.sum(axis=1)

# Total summary row
total_row = df.groupby('age_group').size()
total_row['Total'] = total_row.sum()

# Display all tables
print("Gender Distribution Table:\n", gender_table)
print("\nRace Distribution Table:\n", race_table)
print("\nTotal Images per Age Group:\n", total_row)

# Optional: Save to CSV
gender_table.to_csv("gender_distribution.csv")
race_table.to_csv("race_distribution.csv")
total_row.to_frame(name='Count').T.to_csv("age_totals.csv")