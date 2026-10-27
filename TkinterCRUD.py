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
conn.commit()


def predict(biologi, fisika, inggris):
    if inggris > biologi and inggris > fisika:
        return "Bahasa"
    elif biologi > inggris and biologi > fisika:
        return "Kedokteran"
    elif fisika > inggris and fisika > biologi:
        return "Teknik"
    return "Gausah Kuliah"


def submit():
    nama = entry_nama.get().strip()
    bio = entry_bio.get().strip()
    fis = entry_fis.get().strip()
    ing = entry_ing.get().strip()

    if nama == "" or bio == "" or fis == "" or ing == "":
        msg.showerror("Error", "Semua nilai harus diisi!")
        return
    if not (bio.isdigit() and fis.isdigit() and ing.isdigit()):
        msg.showerror("Error", "Nilai harus angka!")
        return

    bio, fis, ing = int(bio), int(fis), int(ing)
    if not all(0 <= n <= 100 for n in (bio, fis, ing)):
        msg.showerror("Error", "Nilai harus antara 0 - 100!")
        return

    hasil = predict(bio, fis, ing)

    conn.execute(
        "INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
        "VALUES (?, ?, ?, ?, ?)",
        (nama, bio, fis, ing, hasil),
    )
    conn.commit()

    lbl.config(text=f"Prediksi: {hasil}")
    for ent in (entry_nama, entry_bio, entry_fis, entry_ing):
        ent.delete(0, tk.END)


root = tk.Tk()
root.geometry("1080x720")
root.title("Prediksi Fakultas")

e = []
for teks in ["Nama Siswa", "Biologi", "Fisika", "Inggris"]:
    tk.Label(root, text=teks).pack()
    ent = tk.Entry(root, width=25, justify="center")
    ent.pack()
    e.append(ent)

entry_nama, entry_bio, entry_fis, entry_ing = e

tk.Button(root, text="Submit", command=submit).pack(pady=8)
lbl = tk.Label(root, text="Prediksi: -")
lbl.pack(pady=(0, 10))


def on_close():
    conn.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()