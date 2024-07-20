import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import SharedData
import GUI

def playlist_creator_gui():
    root = tk.Tk()
    root.title("Playlist Creator GUI")
    root.geometry("1200x800")

    primary_color = '#344e41'
    secondary_color = '#3a5a40'
    background_color = '#dad7cd'
    secondary_color2 = '#A3B18A'
    accent_color = '#a3b18a'
    text_color = '#ffffff'
    text_color2 = '#000000'

    root.configure(bg=background_color)

    def switch_to_main_gui():
        try:
            root.destroy()
            GUI.main_gui()
        except Exception as e:
            print("Error switching to main GUI:", e)

    def get_sorted_table_data():
        sorted_data = []
        for item in table.get_children():
            sorted_data.append(table.item(item)['values'])
        return sorted_data

    def save_as_csv():
        filename = filedialog.asksaveasfilename(
            title="Save as CSV",
            filetypes=[("CSV files", "*.csv")],
            defaultextension=".csv"
        )
        if filename:
            sorted_data = get_sorted_table_data()
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(
                    ['SongID', 'Title', 'Album', 'Artist', 'Duration', 'Popularity', 'ReleaseDate', 'Genre', 'Key',
                     'Tempo'])
                for item in sorted_data:
                    csvwriter.writerow(item)
            print(f"Data saved to {filename}")

    def clear_table():
        response = messagebox.askyesno("Confirm", "Do you want to erase the list?")
        if response:
            for item in table.get_children():
                table.delete(item)

    def erase_selected_from_list():
        response = messagebox.askyesno("Confirm", "Do you want to delete the selected track(s)?")
        if response:
            selected_items = table.selection()
            for item in selected_items:
                table.delete(item)

    def move_up():
        selected_items = table.selection()
        for selected_item in selected_items:
            table.move(selected_item, table.parent(selected_item), table.index(selected_item) - 1)

    def move_down():
        selected_items = table.selection()
        for selected_item in selected_items:
            table.move(selected_item, table.parent(selected_item), table.index(selected_item) + 1)

    def save_playlist():
        playlist_name = simpledialog.askstring("Playlist Name", "Enter the name of the new playlist:")
        if not playlist_name:
            return

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
                                                       client_secret='your_client_secret',
                                                       redirect_uri='http://localhost:5000/callback',
                                                       scope='playlist-modify-public'))
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, playlist_name)

        sorted_data = get_sorted_table_data()
        total_tracks = len(sorted_data)
        batch_size = 100
        total_added = 0
        not_added_tracks = []

        for start in range(0, total_tracks, batch_size):
            track_ids = []
            batch_tracks = sorted_data[start:start + batch_size]
            for track in batch_tracks:
                if len(track) >= 3:
                    title, artist = track[1], track[2]
                    query = 'artist:"{}" track:"{}"'.format(artist, title)
                    results = sp.search(q=query, type='track')
                    tracks = results['tracks']['items']
                    if tracks:
                        track_ids.append(tracks[0]['uri'])
                    else:
                        not_added_tracks.append((title, artist))

            if track_ids:
                sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
                total_added += len(track_ids)
                print(f"{total_added} of {total_tracks} tracks added to '{playlist_name}'")

        print(f"Completed: Playlist '{playlist_name}' created with {total_added} tracks.")
        if not_added_tracks:
            print("The following tracks were not added:")
            for track in not_added_tracks:
                print(f"Title: {track[0]}, Artist: {track[1]}")

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    banner_frame = tk.Frame(root, height=50, bg=primary_color)
    banner_frame.pack(side='top', fill='x')
    banner_frame.pack_propagate(False)

    index_button = tk.Button(banner_frame, text="Index", bg='#DAD7CD', fg=text_color2, command=switch_to_main_gui)
    index_button.pack(side='left', padx=20, pady=10)

    frame1 = tk.Frame(root, width=200, height=650, bg=secondary_color)
    frame1.pack(side='left', fill='y')
    frame1.pack_propagate(False)
    frame2 = tk.Frame(root, width=800, height=650, bg=background_color)
    frame2.pack(side='left', fill='both', expand=True)
    frame2.pack_propagate(False)
    frame3 = tk.Frame(root, width=200, height=650, bg=secondary_color)
    frame3.pack(side='left', fill='y')
    frame3.pack_propagate(False)


    erase_list_button = tk.Button(frame1, text="Erase List", command=clear_table, bg=secondary_color2, fg=text_color2,)
    erase_list_button.pack(pady=10)
    erase_selected_button = tk.Button(frame1, text="Erase Selected", command=erase_selected_from_list, bg=secondary_color2, fg=text_color2,)
    erase_selected_button.pack(pady=10)

    move_up_button = tk.Button(frame1, text="Move Up", command=move_up, bg=secondary_color2, fg=text_color2,)
    move_up_button.pack(pady=5)
    move_down_button = tk.Button(frame1, text="Move Down", command=move_down, bg=secondary_color2, fg=text_color2,)
    move_down_button.pack(pady=5)

    save_csv_button = tk.Button(frame3, text="Save as CSV", command=save_as_csv, bg=secondary_color2, fg=text_color2,)
    save_csv_button.pack(pady=10)
    load_csv_button = tk.Button(frame3, text="Load CSV Playlist", bg=secondary_color2, fg=text_color2,)
    load_csv_button.pack(pady=10)
    save_playlist_button = tk.Button(frame3, text="Save Playlist", command=save_playlist, bg='#1DB954', fg=text_color2,)
    save_playlist_button.pack(pady=10)

    table_container = tk.Frame(frame2, bg='#fc8eac')
    table_container.pack(fill='both', expand=True)

    table = ttk.Treeview(table_container, columns=(
    "SongID", "Title", "Artist", "Album", "Duration", "Popularity", "ReleaseDate", "Genre", "Key", "Tempo"), show="headings")
    for col in table['columns']:
        table.heading(col, text=col, command=lambda _col=col: treeview_sort_column(table, _col, False))
        table.column(col, anchor='w', width=100)

    def load_csv():
        filename = filedialog.askopenfilename(
            title="Open CSV file",
            filetypes=[("CSV files", "*.csv")],
            defaultextension=".csv"
        )

        if filename:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for item in table.get_children():
                    table.delete(item)

                for row in csvreader:
                    if len(row) == 10:
                        table.insert('', 'end', values=row)

    load_csv_button.config(command=load_csv)

    def update_playlist_creator_table():
        for item in SharedData.shared_tracks:
            table.insert('', 'end', values=item)

    update_playlist_creator_table()

    scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side='left', fill='both', expand=True)

    root.mainloop()

if __name__ == "__main__":
    playlist_creator_gui()
