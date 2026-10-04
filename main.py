import tkinter as tk
from tkinter import messagebox
import pyodbc


# 1. Veritabanından kitapları çeken fonksiyon
def kitaplari_getir():
  try:
    baglanti = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=.\SQLEXPRESS;'
        r'DATABASE=MiniKutuphane;'
        r'Trusted_Connection=yes;'
    )
    cursor = baglanti.cursor()
    cursor.execute('SELECT KitapAdi, Yazar FROM Kitaplar')
    kayitlar = cursor.fetchall()
    baglanti.close()

    liste_kutusu.delete(0, tk.END)
    for kitap in kayitlar:
      liste_kutusu.insert(tk.END, f'Kitap: {kitap[0]}  ---  Yazar: {kitap[1]}')

  except Exception as e:
    messagebox.showerror('Hata', f'Bir hata oluştu: {e}')


# 2. Yeni kitap ekleyen fonksiyon (INSERT INTO SQL)
def kitap_ekle():
  kitap_adi = entry_kitap.get()
  yazar_adi = entry_yazar.get()

  # Boşluk kontrolü
  if kitap_adi == '' or yazar_adi == '':
    messagebox.showwarning(
        'Uyarı', 'Lütfen kitap adı ve yazar alanlarını boş bırakmayın!'
    )
    return

  try:
    baglanti = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=.\SQLEXPRESS;'
        r'DATABASE=MiniKutuphane;'
        r'Trusted_Connection=yes;'
    )
    cursor = baglanti.cursor()

    # Senin öğrendiğin INSERT INTO komutunun Python hali!
    sorgu = (
        'INSERT INTO Kitaplar (KitapAdi, Yazar, BasimYili, StokAdedi) VALUES'
        ' (?, ?, 2024, 1)'
    )
    cursor.execute(sorgu, (kitap_adi, yazar_adi))

    baglanti.commit()  # Veritabanına kaydetmeyi onaylıyoruz
    baglanti.close()

    messagebox.showinfo('Başarılı', 'Kitap başarıyla veritabanına eklendi!')

    # Kutucukları temizle
    entry_kitap.delete(0, tk.END)
    entry_yazar.delete(0, tk.END)

    # Listeyi otomatik güncelle ki yeni eklenen kitap görünsün
    kitaplari_getir()

  except Exception as e:
    messagebox.showerror('Hata', f'Kitap eklenirken bir hata oluştu: {e}')


# --- ARAYÜZ TASARIMI (TKINTER) ---
pencere = tk.Tk()
pencere.title('Mini Kütüphane Otomasyonu')
pencere.geometry('480x525')

# Başlık
baslik = tk.Label(
    pencere, text='Kütüphane Yönetim Paneli', font=('Arial', 14, 'bold')
)
baslik.pack(pady=10)

# --- KİTAP EKLEME ÇERÇEVESİ ---
frame_ekle = tk.LabelFrame(
    pencere, text=' Yeni Kitap Ekle ', font=('Arial', 10, 'bold'), padx=10, pady=10
)
frame_ekle.pack(pady=5, fill='x', padx=20)

lbl_kitap = tk.Label(frame_ekle, text='Kitap Adı:', font=('Arial', 10))
lbl_kitap.grid(row=0, column=0, sticky='w', pady=5)
entry_kitap = tk.Entry(frame_ekle, width=28, font=('Arial', 10))
entry_kitap.grid(row=0, column=1, pady=5)

lbl_yazar = tk.Label(frame_ekle, text='Yazar:', font=('Arial', 10))
lbl_yazar.grid(row=1, column=0, sticky='w', pady=5)
entry_yazar = tk.Entry(frame_ekle, width=28, font=('Arial', 10))
entry_yazar.grid(row=1, column=1, pady=5)

btn_ekle = tk.Button(
    frame_ekle,
    text='Kitabı Kaydet',
    command=kitap_ekle,
    bg='#2196F3',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=10,
    pady=3,
)
btn_ekle.grid(row=2, column=1, pady=5, sticky='e')

# --- LİSTELEME ALANI ---
btn_listele = tk.Button(
    pencere,
    text='Kitapları Yenile / Listele',
    command=kitaplari_getir,
    bg='#4CAF50',
    fg='white',
    font=('Arial', 10, 'bold'),
    padx=10,
    pady=5,
)
btn_listele.pack(pady=10)

liste_kutusu = tk.Listbox(pencere, width=58, height=10, font=('Arial', 9))
liste_kutusu.pack(pady=5)

# Program açıldığı an listeyi doldursun
kitaplari_getir()

pencere.mainloop()