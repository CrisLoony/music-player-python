import os
import time
import tkinter as tk
from tkinter import filedialog

import pygame
import ttkbootstrap as ttk
from mutagen.mp3 import MP3

pygame.mixer.init()


playlist = []
playing = False


def load_playlist():
    global playlist, current_song, directory
    directory = filedialog.askdirectory(title="Choose a directory")
    directory = directory.replace("/", "\\")

    for song in os.listdir(directory):
        song_name, ext = os.path.splitext(song)
        if ext == ".mp3":
            playlist.append(song)

    for song in playlist:
        playlist_box.insert("end", song[0:-4])

    playlist_box.selection_set(0)


def play_song():
    global current_song, playing, directory, music_index, load, song_length
    music_index = playlist_box.curselection()[0]
    current_song = playlist[music_index]
    title = current_song[0:-4]
    name_var.set(title)

    if playing == None:
        pygame.mixer.music.unpause()
        play_btn.configure(image=pause)
        playing = True

    elif playing == False:
        load = f'{directory}\\{current_song}'
        pygame.mixer.music.load(load)
        pygame.mixer.music.play()
        playing = True

        play_btn.configure(image=pause)
        slider.configure(value=0)

    elif playing:
        pygame.mixer.music.pause()
        play_btn.configure(image=play)
        playing = None

    song_time()


def stop_song():
    global playing
    pygame.mixer.music.unload()
    play_btn.configure(image=play)
    playing = False


def next_song():
    global current_song, playing, directory, music_index
    try:
        playlist_box.selection_clear(0, 'end')
        playlist_box.selection_set(music_index + 1)

        music_index = playlist_box.curselection()[0]
        current_song = playlist[music_index]
        playing = False
        play_song()

    except:
        pass


def previous_song():
    global current_song, playing, directory, music_index

    try:
        playlist_box.selection_clear(0, 'end')
        playlist_box.selection_set(music_index - 1)

        music_index = playlist_box.curselection()[0]
        current_song = playlist[music_index]
        playing = False
        play_song()

    except:
        pass


def song_time():
    global load, song_length, playing

    if playing or playing == None:
        current_time = pygame.mixer.music.get_pos() / 1000
        current_time_converted = time.strftime(
            '%M:%S', time.gmtime(current_time))
        cronometer.configure(text=current_time_converted)

        song_mut = MP3(load)
        song_length = song_mut.info.length
        total_song_time = time.strftime('%M:%S', time.gmtime(song_length))
        total_time.configure(text=total_song_time)

        slider_position = int(song_length)
        slider.configure(to=slider_position, value=current_time)

        cronometer.after(1000, song_time)

    elif not playing:
        slider.configure(value=0)
        cronometer.configure(text='')
        total_time.configure(text='')


window = ttk.Window(title='Music Player',
                    themename='morph',
                    resizable=(True, False),
                    size=(700, 700))
window.place_window_center()

menubar = tk.Menu(master=window)
window.config(menu=menubar)
organise_menu = tk.Menu(master=menubar, tearoff=False)
organise_menu.add_command(label="Select Folder", command=load_playlist)
menubar.add_cascade(label="Menu", menu=organise_menu)

name_var = tk.StringVar()
name_label = ttk.Label(master=window,
                       textvariable=name_var,
                       font='bahnschrift 18',
                       anchor='center')
name_label.pack()

album_photo = tk.PhotoImage(file=r'images\music_icon.png')
album_label = ttk.Label(master=window,
                        image=album_photo,
                        anchor='center')
album_label.pack(pady=5)

slider = ttk.Scale(master=window, bootstyle='info', length=250,
                   from_=0, to=100, value=0)
slider.pack()

time_frame = ttk.Frame(master=window)
time_frame.pack()

cronometer = ttk.Label(master=time_frame, text='00:00', font='bahnschrift 12')
cronometer.grid(row=0, column=0, padx=110)

total_time = ttk.Label(master=time_frame, text='00:00', font='bahnschrift 12')
total_time.grid(row=0, column=1, padx=110)

play = tk.PhotoImage(file=r'images\play.png')
pause = tk.PhotoImage(file=r'images\pause.png')
stop = tk.PhotoImage(file=r'images\stop.png')
next = tk.PhotoImage(file=r'images\next.png')
previous = tk.PhotoImage(file=r'images\previous.png')

controls_frame = ttk.Frame(master=window, width=380, height=200)
controls_frame.pack(pady=15)

play_btn = ttk.Button(master=controls_frame, bootstyle='light',
                      image=play, command=play_song)
stop_btn = ttk.Button(master=controls_frame, bootstyle='light',
                      image=stop, command=stop_song)
next_btn = ttk.Button(master=controls_frame, bootstyle='light',
                      image=next, command=next_song)
previous_btn = ttk.Button(master=controls_frame, bootstyle='light',
                          image=previous, command=previous_song)

previous_btn.grid(row=0, column=0, padx=0, pady=10)
play_btn.grid(row=0, column=1, padx=0, pady=10)
stop_btn.grid(row=0, column=2, padx=0, pady=10)
next_btn.grid(row=0, column=3, padx=0, pady=10)

playlist_box = tk.Listbox(master=window,
                          width=70,
                          height=10)
playlist_box.pack(pady=10)

window.mainloop()
