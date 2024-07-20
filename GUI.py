import tkinter as tk
from tkinter import ttk
from Table_Data import create_table, get_data, apply_search
import Spotifytrick
import youtubetrick
import playlist_creator_GUI
import SharedData
from song_id_finder import find_and_open_song_json


table = None
current_search_filter = None
music_keys = ["Any Key", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
              "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m", "Am", "A#m", "Bm"]


def main_gui():
    global table
    root = tk.Tk()
    root.title("Custom GUI Layout")
    root.geometry("1200x800")



    primary_color = '#a3b18a'
    secondary_color = '#588157'
    text_color = '#ffffff'
    text_color2 = '#ffffff'
    background_color = '#dad7cd'
    accent_color = '#588157'

    # Banner
    banner_frame = tk.Frame(root, height=50, bg=primary_color)
    banner_frame.pack(side='top', fill='x')
    banner_frame.pack_propagate(False)


    def switch_to_playlist_creator_gui():
        root.destroy()
        playlist_creator_GUI.playlist_creator_gui()


    playlist_creator_button = tk.Button(banner_frame, text="playlist_creator", bg=secondary_color, fg=text_color2, command=switch_to_playlist_creator_gui)
    playlist_creator_button.pack(side='left', padx=20, pady=10)

    # Search bar
    search_section = tk.Frame(root, height=50, bg=primary_color)
    search_section.pack(side='top', fill='x')
    search_section.pack_propagate(False)
    search_options = ["Title", "Artist", "Album", "Year", "Genre"]
    combobox = ttk.Combobox(search_section, values=search_options, state="readonly")
    combobox.set(search_options[0])  # Set the first option as default
    combobox.pack(side='left', padx=(10, 0), pady=10)
    search_entry = tk.Entry(search_section, bg=text_color, fg=primary_color)
    search_entry.pack(side='left', padx=(10, 0), pady=10, expand=True, fill='x')
    all_data = get_data()

    def handle_search():
        global table, current_search_filter
        query = search_entry.get()
        selected_field = combobox.get()
        current_search_filter = (query, selected_field)
        reset_table()
        if query:
            apply_search(table, query, all_data, selected_field)
        filter_by_key()

    def reset_table():
        global table
        for item in table.get_children():
            table.delete(item)
        for item in all_data[:1000]:
            values = [item[col] for col in table['columns']]
            table.insert('', 'end', values=values)

    def search_by_song_id():
        song_id = song_id_entry.get()
        try:
            song_id_int = int(song_id)
            song_index = None

            for i, item in enumerate(all_data):
                if int(item['SongID']) == song_id_int:
                    song_index = i
                    break

            if song_index is None:
                raise ValueError("Song ID not found")
            start_index = song_index
            end_index = min(start_index + 1000, len(all_data))
            table.delete(*table.get_children())

            for item in all_data[start_index:end_index]:
                values = [item[col] for col in table['columns']]
                table.insert('', 'end', values=values)

        except ValueError as e:
            print(str(e))

    search_button = tk.Button(search_section, text="Search", bg=secondary_color, fg=text_color2, command=lambda: handle_search())
    search_button.pack(side='left', padx=(0, 10), pady=10)

    frame1 = tk.Frame(root, width=200, height=650, bg=background_color)
    frame1.pack(side='left', fill='y')
    frame1.pack_propagate(False)

    frame2 = tk.Frame(root, width=800, height=650, bg=accent_color)
    frame2.pack(side='left', fill='both', expand=True)
    frame2.pack_propagate(False)

    frame3 = tk.Frame(root, width=200, height=650, bg=background_color)
    frame3.pack(side='left', fill='y')
    frame3.pack_propagate(False)

    table_container = tk.Frame(frame2, bg=background_color)
    table_container.pack(fill='both', expand=True)
    table = create_table(table_container, all_data)

    # POP SLIDER
    min_slider_label = tk.Label(frame1, text="Min Popularity")
    min_slider_label.pack(padx=10, pady=2)
    min_slider = tk.Scale(frame1, from_=0, to=100, orient='horizontal')
    min_slider.set(0)
    min_slider.pack(padx=10, pady=5)
    max_slider_label = tk.Label(frame1, text="Max Popularity")
    max_slider_label.pack(padx=10, pady=2)
    max_slider = tk.Scale(frame1, from_=0, to=100, orient='horizontal')
    max_slider.set(100)
    max_slider.pack(padx=10, pady=5)

    # YEAR SLIDER
    min_year_label = tk.Label(frame1, text="Min Release Year")
    min_year_label.pack(padx=10, pady=2)
    min_year_slider = tk.Scale(frame1, from_=1950, to=2024, orient='horizontal')
    min_year_slider.set(1950)
    min_year_slider.pack(padx=10, pady=5)
    max_year_label = tk.Label(frame1, text="Max Release Year")
    max_year_label.pack(padx=10, pady=2)
    max_year_slider = tk.Scale(frame1, from_=1950, to=2024, orient='horizontal')
    max_year_slider.set(2024)
    max_year_slider.pack(padx=10, pady=5)

    # KEY SELECTOR
    key_selector_label = tk.Label(frame1, text="Select Key")
    key_selector_label.pack(padx=10, pady=2)
    key_selector = ttk.Combobox(frame1, values=music_keys, state="readonly")
    key_selector.current(0)
    key_selector.pack(padx=10, pady=5)

    # SONG ID FINDER
    song_id_label = tk.Label(frame1, text="Enter Song ID:")
    song_id_label.pack(padx=10, pady=(20, 2))
    song_id_entry = tk.Entry(frame1)
    song_id_entry.pack(padx=10, pady=2)
    search_song_id_button = tk.Button(frame1, text="Search by Song ID", command=search_by_song_id)
    search_song_id_button.pack(padx=10, pady=10)


    def add_to_playlist_creator_list():
        selected_items = table.selection()
        for item_id in selected_items:
            track_data = table.item(item_id, 'values')
            if track_data not in SharedData.shared_tracks:
                SharedData.shared_tracks.append(track_data)

    def search_on_spotify(row_id):
        track_title = table.item(row_id, 'values')[1]
        artist_name = table.item(row_id, 'values')[2]
        Spotifytrick.open_spotify_link(track_title, artist_name)

    def search_on_youtube(row_id):
        track_title = table.item(row_id, 'values')[1]
        artist_name = table.item(row_id, 'values')[2]
        youtubetrick.open_first_youtube_result(track_title, artist_name)

    def on_right_click(event):
        row_id = table.identify_row(event.y)
        if row_id:
            item = table.item(row_id)
            song_id = item['values'][0]

            menu = tk.Menu(root, tearoff=0)
            menu.add_command(label="Send to playlist_creator List", command=add_to_playlist_creator_list)
            menu.add_command(label="Search on Youtube", command=lambda: search_on_youtube(row_id))
            menu.add_command(label="Search on Spotify", command=lambda: search_on_spotify(row_id))
            menu.add_command(label="Copy Cell",
                             command=lambda: copy_cell_content(row_id, table.identify_column(event.x)))
            menu.add_command(label="Open Song JSON", command=lambda: find_and_open_song_json(song_id))
            menu.tk_popup(event.x_root, event.y_root)

    def copy_cell_content(row_id, column_id):
        cell_value = table.item(row_id, 'values')[int(column_id.replace('#', '')) - 1]
        root.clipboard_clear()
        root.clipboard_append(cell_value)

    table.bind("<Button-3>", on_right_click)

    def filter_by_key():
        global table, current_search_filter
        selected_key = key_selector.get()
        reset_table()

        if current_search_filter and current_search_filter[0]:
            apply_search(table, current_search_filter[0], all_data, current_search_filter[1])

        if selected_key != "Any Key":
            for item in table.get_children():
                item_data = table.item(item, 'values')
                key = item_data[8]
                if key != selected_key:
                    table.detach(item)

    key_selector.bind("<<ComboboxSelected>>", lambda event: filter_by_key())

    def apply_filter():
        global table
        min_popularity = min_slider.get()
        max_popularity = max_slider.get()
        min_year = min_year_slider.get()
        max_year = max_year_slider.get()

        for item in table.get_children():
            item_data = table.item(item, 'values')
            popularity = int(item_data[5])
            release_year = int(item_data[6])

            if (min_popularity <= popularity <= max_popularity) and (min_year <= release_year <= max_year):
                table.reattach(item, '', table.index(item))
            else:
                table.detach(item)

    # Filter
    filter_button = tk.Button(frame1, text="Filter", command=apply_filter, bg=secondary_color, fg=text_color2,)
    filter_button.pack(padx=10, pady=5)


    scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side='left', fill='both', expand=True)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
