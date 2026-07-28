# Template Peta Desa (Ahza Studio) for QGIS

![QGIS Plugin](https://img.shields.io/badge/QGIS-3.0+-brightgreen.svg)
![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)
![Version](https://img.shields.io/badge/Version-1.0.1-orange.svg)

**Template Peta Desa** adalah plugin QGIS profesional yang dirancang khusus untuk mengotomatisasi pembuatan Layout Peta Desa sesuai standar PerKa BIG No. 3 Tahun 2016 secara dinamis.

Plugin ini sangat membantu dan mempercepat kerja kartografer, perangkat desa, serta konsultan pemetaan dalam memproduksi Peta Citra, Peta Sarana & Prasarana, dan Peta Penutup Lahan dengan format penyajian (layout) yang berstandar nasional.

---

## 🌟 Fitur Utama (Key Features)

* **Otomatisasi Penuh (A1 & A0):** Hanya dengan sekali klik, layout peta Anda akan langsung terbangun lengkap dengan seluruh ornamen petanya, baik untuk ukuran kertas A1 (ISO) maupun A0 (Custom).
* **Standarisasi PerKa BIG No. 3 Tahun 2016:** Tata letak Muka Peta, Informasi Tepi Peta, Arah Utara, Skala (Angka & Grafis), Legenda (Keterangan), Riwayat Pembuatan, hingga Sistem Koordinat dikalkulasi dan ditempatkan secara presisi.
* **Smart Map Grids:** Secara otomatis membangun 2 jenis Grid presisi pada Peta Utama: 
    * *Graticul* (Grid Geografis DMS) berawarna biru cerah
    * *Measure* (Grid UTM) bersilang hitam
* **Auto Inset Map (Petunjuk Letak Peta):** Otomatis mendeteksi batas desa dan membangun dua peta inset (Inset Skala Regional dan Skala Lokal) yang tersnap ke derajat terdekat dan berpusat sempurna pada lokasi desa.
* **Dinamis & Tipografi Presisi:** Elemen teks dan atribut dinamis (seperti Nama Desa, Kecamatan, Kabupaten, Skala Peta, Catatan, Logo) di-render secara rapi dan selaras. Penempatan dan perataan vertikal (Vertical Center) dipastikan presisi dalam hitungan milimeter.

## 🛠️ Instalasi

1. Download atau *clone* repositori ini.
2. Salin *folder* kode ke dalam direktori plugin QGIS Anda:
   - **Windows:** `C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\qgis-peta-desa`
   - **Mac/Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qgis-peta-desa`
3. Buka QGIS.
4. Masuk ke **Plugins -> Manage and Install Plugins -> Installed**.
5. Centang **Template Peta Desa**.
6. Ikon khusus akan muncul di toolbar QGIS, siap digunakan!

## 🚀 Cara Penggunaan

1. Buka *project* QGIS yang berisi layer spasial Peta Desa Anda.
2. Pastikan Anda telah melakukan *Zoom to Layer* atau memusatkan tampilan kanvas peta (*map canvas*) pada batas administrasi (AOI) desa yang akan dicetak.
3. Klik tombol plugin **Peta Desa** pada toolbar.
4. Jendela dialog akan terbuka. Masukkan parameter atribut wilayah (Nama Desa, Kecamatan, Lokasi File Logo Pemda, dll).
5. **Cek Skala Otomatis (Auto-Scale to AOI):** Plugin akan mendeteksi *extent* (cakupan wilayah) pada layer atau kanvas Anda. Skala ideal akan otomatis dihitung agar pas (*fit*) di dalam bingkai (frame) peta utama berdasarkan ukuran kertas yang Anda pilih. Anda tetap bisa menyesuaikan angka skala ini secara manual (misalnya membulatkan dari 1:5320 menjadi 1:5000) pada kolom *Skala Utama*.
6. Tentukan opsi ukuran kertas Layout (A1 ISO atau A0 Custom).
7. Klik **Jalankan / Generate**.
8. QGIS *Print Layout* baru akan otomatis tersusun dengan hasil akhir yang siap diekspor ke PDF/Image.

## 🤝 Dukungan & Isu (Contact & Support)

* **Author:** Ahza Studio
* **Email:** admin@ahzastudio.web.id
* **Issue Tracker:** [Report a Bug](https://github.com/ahzastudio/qgis-peta-desa/issues)

Jika Anda menemukan celah (*bug*) atau mempunyai ide fantastis untuk pembaruan fitur, silakan buat *New Issue* pada tautan di atas.

---

## 📄 License

This plugin is licensed under the **GNU General Public License v3.0 (GPL-3.0)** - see the [LICENSE](LICENSE) file for details.

**© 2026 Ahza Studio** - Solusi Pemetaan Spasial Profesional
