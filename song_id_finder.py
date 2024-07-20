import json
import os
import subprocess

def find_and_open_song_json(song_id):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Databases')
    song_index_prefix = "Song_Index_"

    song_index_files = [f for f in os.listdir(base_path) if f.startswith(song_index_prefix) and f.endswith(".json")]
    song_index_files.sort()

    song_found = False
    for filename in song_index_files:
        full_path = os.path.join(base_path, filename)
        try:
            with open(full_path, "r") as file:
                songs = json.load(file)
                for song in songs:
                    if str(song["SongID"]) == str(song_id):
                        print(f"Track is found in {filename}")
                        song_found = True

                        try:
                            if os.name == 'nt':  # Windows
                                os.startfile(full_path)
                            elif os.name == 'posix':  # macOS and Linux
                                subprocess.run(['open', full_path], check=True)
                        except Exception as e:
                            print(f"Failed to open file: {e}")
                        return

        except FileNotFoundError:
            print(f"File not found: {full_path}")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {full_path}")
            continue

    if not song_found:
        print(f"Song ID {song_id} not found in any {song_index_prefix} file.")

if __name__ == "__main__":
    song_id = int(input("Enter the Song ID: "))
    find_and_open_song_json(song_id)
