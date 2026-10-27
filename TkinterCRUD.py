import sqlite3
import tkinter as tk
import tkinter.messagebox as msg

conn = sqlite3.connect("nilai_siswa.db")
conn.execute("""CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi INTEGER NOT NULL,
    fisika INTEGER NOT NULL,
    inggris INTEGER NOT NULL,
    prediksi_fakultas TEXT NOT NULL)""")


def predict(biologi, fisika, inggris):
    if inggris > biologi and inggris > fisika:
        return "Bahasa"
    elif biologi > inggris and biologi > fisika:
        return "Kedokteran"
    elif fisika > inggris and fisika > biologi:
        return "Teknik"
    return "Gausah Kuliah"


def submit():
    try:
        nama = e[0].get().strip()
        bio, fis, ing = (int(x.get()) for x in e[1:])
        assert nama
    except (ValueError, AssertionError):
        return msg.showwarning("Peringatan", "Isi nama dan nilai (angka) dengan benar!")
    hasil = predict(bio, fis, ing)
    conn.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
                 "VALUES (?, ?, ?, ?, ?)", (nama, bio, fis, ing, hasil))
    conn.commit()
    lbl.config(text="Prediksi: " + hasil)


root = tk.Tk()
root.geometry("1080x720")
root.title("Prediksi Fakultas")
e = []
for teks in ["Nama Siswa", "Biologi", "Fisika", "Inggris"]:
    tk.Label(root, text=teks).pack()
    e.append(tk.Entry(root, width=25, justify="center"))
    e[-1].pack()
tk.Button(root, text="Submit", command=submit).pack(pady=8)
lbl = tk.Label(root, text="Prediksi: -")
lbl.pack(pady=(0, 10))
root.mainloop()