# Eksperimen Preprocessing Data Asuransi

## Untuk Apa Proyek Ini?

Singkatnya, notebook ini adalah **tahap persiapan data sebelum membuat model machine learning**. Dataset biaya asuransi kesehatan dianalisis untuk memahami pola datanya, kemudian dibersihkan dan diubah ke format numerik agar siap digunakan pada model regresi untuk memprediksi `charges` atau biaya asuransi berdasarkan karakteristik peserta.

Notebook ini belum membuat model prediksi final. Fokusnya adalah:

- memahami isi dan pola dataset melalui Exploratory Data Analysis (EDA),
- memeriksa masalah data seperti duplikat, missing value, dan outlier,
- mengubah data kategorikal menjadi angka,
- menstandardisasi fitur, dan
- menghasilkan file dataset yang siap digunakan pada tahap training.

Dataset yang digunakan adalah **US Health Insurance Dataset** dari Kaggle. Dataset berisi 1.338 data individu dengan atribut:

- `age`: usia peserta
- `sex`: jenis kelamin
- `bmi`: indeks massa tubuh
- `children`: jumlah anak
- `smoker`: status merokok
- `region`: wilayah tempat tinggal
- `charges`: biaya asuransi sebagai target

Notebook `preprocessing/Eksperimen_RizqiFathurrohman.ipynb` dan script `preprocessing/automate_RizqiFathurrohman.py` memiliki tujuan yang sama, yaitu membersihkan dan mengubah data mentah menjadi dataset numerik yang siap dipakai untuk training model.

## Alur Analisis

1. Dataset dimuat dari `insurance_raw/insurance.csv`.
2. Struktur data, statistik deskriptif, missing value, distribusi fitur, distribusi kategori, biaya berdasarkan status perokok, dan korelasi fitur numerik diperiksa melalui EDA.
3. Satu baris duplikat dihapus sehingga tersisa 1.337 baris.
4. Outlier disaring dengan metode IQR pada `age`, `bmi`, `children`, dan `charges`. Karena penyaringan dilakukan pada semua kolom numerik sekaligus, data berkurang menjadi 1.192 baris.
5. Kolom kategorikal diubah menggunakan one-hot encoding dengan `drop_first=True`:
   - `sex` menjadi `sex_male`
   - `smoker` menjadi `smoker_yes`
   - `region` menjadi `region_northwest`, `region_southeast`, dan `region_southwest`
6. `charges` dipisahkan sebagai target, sedangkan delapan kolom lainnya digunakan sebagai fitur.
7. Fitur distandardisasi menggunakan `StandardScaler` sehingga setiap fitur memiliki skala yang sebanding.
8. Hasil disimpan ke `preprocessing/insurance_preprocessing/insurance_preprocessed.csv`.

## Analisis dan Temuan

- Dataset awal tidak memiliki missing value pada seluruh tujuh kolom.
- Nilai `charges` memiliki rentang yang lebar, dari sekitar 1.121,87 hingga 63.770,43. Median biaya sekitar 9.382,03, sedangkan rata-ratanya sekitar 13.270,42. Perbedaan ini menunjukkan distribusi target cenderung miring ke kanan dan memiliki nilai biaya tinggi.
- Status merokok merupakan faktor yang terlihat paling menonjol dalam EDA. Kelompok perokok memiliki sebaran biaya yang jauh lebih tinggi dibandingkan kelompok bukan perokok.
- `age` dan `bmi` dapat digunakan sebagai faktor numerik untuk menjelaskan variasi biaya. Korelasi antarfitur numerik perlu dibaca sebagai hubungan awal, bukan bukti sebab-akibat.
- Fitur `sex` dan `region` tetap dipertahankan melalui encoding karena dapat memberikan informasi tambahan bagi model, walaupun pengaruhnya harus dibuktikan melalui evaluasi model.
- Penyaringan IQR membuang sekitar 10,8% data setelah duplikat dihapus. Ini dapat mengurangi pengaruh nilai ekstrem, tetapi juga berisiko menghapus kasus biaya tinggi yang valid. Keputusan ini sebaiknya dibandingkan dengan eksperimen yang mempertahankan outlier atau hanya mentransformasi target.
- Notebook mengimpor `LinearRegression`, `train_test_split`, `Pipeline`, dan metrik regresi, tetapi belum menjalankan pembagian data, training, prediksi, maupun evaluasi. Jadi, hasil proyek saat ini adalah **dataset hasil preprocessing**, bukan model prediksi yang sudah terbukti akurat.

## Grafik EDA

Grafik berikut adalah visualisasi yang dihasilkan dari notebook dan membantu menjelaskan alasan di balik preprocessing yang dilakukan.

### Distribusi Fitur Numerik

![Distribusi fitur numerik](preprocessing/figures/distribusi-numerik.png)

Grafik ini menunjukkan distribusi `age`, `bmi`, `children`, dan `charges`. Distribusi `charges` yang memiliki ekor panjang membantu menjelaskan mengapa terdapat nilai biaya ekstrem dan mengapa outlier perlu diperiksa.

### Distribusi Fitur Kategorikal

![Distribusi fitur kategorikal](preprocessing/figures/distribusi-kategorikal.png)

Grafik ini memperlihatkan jumlah data berdasarkan `sex`, `smoker`, dan `region`. Informasi ini berguna untuk memahami keseimbangan kategori sebelum melakukan one-hot encoding.

### Biaya Berdasarkan Status Perokok

![Biaya berdasarkan status perokok](preprocessing/figures/biaya-berdasarkan-perokok.png)

Perbandingan ini menunjukkan perbedaan sebaran `charges` antara perokok dan bukan perokok. Status `smoker` tampak sebagai salah satu pembeda biaya yang paling kuat dalam analisis awal.

### Korelasi Fitur Numerik

![Korelasi fitur numerik](preprocessing/figures/korelasi-fitur-numerik.png)

Heatmap ini menunjukkan hubungan linear antarfitur numerik. Korelasi membantu eksplorasi awal, tetapi tidak cukup untuk menyimpulkan hubungan sebab-akibat.

## Output

File `insurance_preprocessed.csv` berisi 1.192 baris dan 9 kolom:

```text
age,bmi,children,sex_male,smoker_yes,
region_northwest,region_southeast,region_southwest,charges
```

Delapan kolom fitur sudah distandardisasi. Kolom `charges` tetap berada pada nilai asli agar dapat digunakan sebagai target regresi dan dibandingkan langsung dengan nilai biaya sebenarnya.

## Kesimpulan

Notebook ini digunakan untuk melakukan EDA dan preprocessing dataset biaya asuransi kesehatan. Prosesnya berhasil menghasilkan data yang lebih bersih, bebas missing value, tanpa duplikat, telah disaring dari outlier berdasarkan IQR, dan seluruh fitur kategorikal telah diubah menjadi bentuk numerik. File output siap digunakan untuk tahap pemodelan regresi, misalnya memprediksi biaya asuransi berdasarkan usia, BMI, jumlah anak, status merokok, jenis kelamin, dan wilayah.

Namun, notebook belum menjawab seberapa baik biaya tersebut dapat diprediksi karena belum ada proses training dan evaluasi model. Tahap lanjutan yang paling relevan adalah membagi data menjadi train/test, melatih model regresi, mengukur MAE atau RMSE dan `R²`, lalu membandingkan hasil dengan dan tanpa penghapusan outlier.

## Menjalankan Preprocessing

Dari folder `preprocessing`, jalankan:

```bash
python automate_RizqiFathurrohman.py
```

Script akan membaca dataset mentah dan menulis ulang file hasil preprocessing ke `preprocessing/insurance_preprocessing/insurance_preprocessed.csv`.

## Referensi Dataset

https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset
