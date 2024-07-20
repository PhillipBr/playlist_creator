import tkinter as tk
from tkinter import ttk
import json
import os
import glob

def load_json(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    base_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Databases')
    all_tracks_data = []

    song_files = glob.glob(os.path.join(base_directory, "Song_Index_*.json"))
    track_files = glob.glob(os.path.join(base_directory, "Tracks_Songs_*.json"))
    audio_features_files = glob.glob(os.path.join(base_directory, "Audio_Features_*.json"))

    for song_file, track_file, audio_features_file in zip(song_files, track_files, audio_features_files):
        song_data = load_json(song_file)
        track_data = load_json(track_file)
        audio_features_data = load_json(audio_features_file)

        song_dict = {str(song['SongID']): song for song in song_data}
        track_dict = {str(track['SongID']): track for track in track_data}
        audio_features_dict = {str(feature['SongID']): feature for feature in audio_features_data}

        for song_id, song in song_dict.items():
            song.update(track_dict.get(song_id, {}))
            song.update(audio_features_dict.get(song_id, {}))
            popularity = int(song.get('Popularity', 0))

            def round_tempo(tempo):
                return int(tempo) if tempo - int(tempo) < 0.5 else int(tempo) + 1

            track_info = {
                "SongID": song_id,
                "Title": song.get('Title', 'N/A'),
                "Artist": song.get('Artist', 'N/A'),
                "Album": song.get('Album', 'N/A'),
                "Duration": song.get('Duration', 'N/A'),
                "Popularity": popularity,
                "ReleaseDate": song.get('ReleaseDate', 'N/A')[:4],
                "Genre": song.get('Genre', 'N/A'),
                "Key": song.get('Key', 'N/A'),
                "Tempo": round_tempo(song.get('Tempo', 0))
            }

            all_tracks_data.append(track_info)

    all_tracks_data.sort(key=lambda x: x['Popularity'], reverse=True)
    top_tracks_data = all_tracks_data[:1000]

    return all_tracks_data

def sort_by(tree, col, descending):
    """ Sort tree contents when a column header is clicked on. """
    def convert_to_numeric(val):
        try:
            return float(val) if '.' in val else int(val)
        except ValueError:
            return val

    data = [(convert_to_numeric(tree.set(child, col)), child) for child in tree.get_children('')]
    numeric_data = [(val, child) for val, child in data if isinstance(val, (int, float))]
    non_numeric_data = [(val, child) for val, child in data if not isinstance(val, (int, float))]

    numeric_data.sort(reverse=descending)
    non_numeric_data.sort(key=lambda x: x[0].lower() if isinstance(x[0], str) else x[0], reverse=descending)

    sorted_data = numeric_data + non_numeric_data if descending else non_numeric_data + numeric_data

    for i, (_, child) in enumerate(sorted_data):
        tree.move(child, '', i)

    tree.heading(col, command=lambda c=col: sort_by(tree, c, not descending))

def create_table(parent, data):
    """ Create and return a table with the given data. """
    tree = ttk.Treeview(parent)

    column_proportions = {
        'SongID': 5,
        'Title': 21,
        'Album': 14,
        'Artist': 16,
        'Duration': 5,
        'Popularity': 5,
        'ReleaseDate': 6,
        'Genre': 12,
        'Key': 5,
        'Tempo': 6
    }

    total_proportions = sum(column_proportions.values())
    desired_total_width = 800
    base_width_unit = desired_total_width / total_proportions

    tree['columns'] = list(data[0].keys()) if data else []

    tree.column("#0", width=0, stretch=tk.NO)

    for col in tree['columns']:
        tree.heading(col, text=col, anchor='w', command=lambda c=col: sort_by(tree, c, False))
        col_width = int(column_proportions.get(col, 10) * base_width_unit)
        tree.column(col, anchor='w', width=col_width)

    for item in data[:1000]:
        values = [item[col] for col in tree['columns']]
        tree.insert('', 'end', values=values)

    return tree

def apply_search(table, query, all_data, search_field):
    """ Apply search on the table based on the query and selected field. """
    for item in table.get_children():
        table.delete(item)

    filtered_data = [item for item in all_data if query.lower() in str(item.get(search_field, '')).lower()]

    for item in filtered_data:
        values = [item.get(col, '') for col in table['columns']]
        table.insert('', 'end', values=values)

def get_data():
    """ Fetch data using the main function. """
    return main()

# Main execution
if __name__ == "__main__":
    data = main()
    for track in data:
        print(track)
