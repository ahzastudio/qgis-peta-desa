# -*- coding: utf-8 -*-
"""
DIALOG WIZARD GUI – PLUGIN QGIS (PERKABIG NO. 3 TAHUN 2016)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
"""

import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'peta_desa_dialog_base.ui'))

class PetaDesaDialog(QDialog, FORM_CLASS):
    """Class dialog GUI wizard untuk mengumpulkan parameter Peta Desa."""

    def __init__(self, parent=None):
        super(PetaDesaDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Tambahkan opsi Grid Simetris 3x3
        from qgis.PyQt.QtWidgets import QCheckBox
        self.chkSimetris = QCheckBox("Gunakan Grid Diagram Lokasi Simetris 3x3 (Relatif)", self)
        self.chkSimetris.setChecked(True)
        self.layout().addWidget(self.chkSimetris)
        
        # Sinyal tombol
        self.btnBrowseLogo.clicked.connect(self.select_logo)
        if hasattr(self, 'btnCekSkala'):
            self.btnCekSkala.clicked.connect(self.cek_skala_optimal)

    def select_logo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.txtLogoPath.setText(file_name)

    def get_config(self):
        """Mengambil konfigurasi pilihan pengguna dari form dialog."""
        skala_str = self.cmbSkala.currentText().replace("1:", "").replace(".", "")
        try:
            skala_val = int(skala_str)
        except ValueError:
            skala_val = 5000

        return {
            "nama_desa": self.txtDesa.text().strip(),
            "nama_kecamatan": self.txtKecamatan.text().strip(),
            "nama_kabupaten": self.txtKabupaten.text().strip(),
            "nama_provinsi": self.txtProvinsi.text().strip(),
            "kode_pos": self.txtKodePos.text().strip(),
            "nomor_lembar": self.txtNoLembar.text().strip(),
            "tahun_peta": self.txtTahun.text().strip(),
            "jenis_peta": self.cmbJenisPeta.currentText(),
            "ukuran_kertas": self.cmbUkuranKertas.currentText(),
            "skala_utama": skala_val,
            "instansi_penyusun": self.txtPenyusun.text().strip(),
            "jabatan_pengesah": self.txtJabatanPengesah.text().strip(),
            "nama_pengesah": self.txtNamaPengesah.text().strip(),
            "sumber_data": self.txtSumberData.toPlainText().strip(),
            "logo_path": self.txtLogoPath.text().strip(),
            "grid_simetris": self.chkSimetris.isChecked(),
        }

    def cek_skala_optimal(self):
        from qgis.core import QgsProject, QgsDistanceArea
        from qgis.PyQt.QtWidgets import QMessageBox
        from qgis.utils import iface

        canvas = iface.mapCanvas()
        layers = canvas.layers()
        if not layers:
            QMessageBox.warning(self, "Peringatan", "Peta masih kosong! Harap tambahkan layer Batas Desa terlebih dahulu dan Zoom ke layernya.")
            return
            
        ext = canvas.extent()
        
        # Inisialisasi QgsDistanceArea untuk pengukuran elipsoid akurat
        da = QgsDistanceArea()
        da.setSourceCrs(canvas.mapSettings().destinationCrs(), QgsProject.instance().transformContext())
        da.setEllipsoid(QgsProject.instance().ellipsoid())
        
        from qgis.core import QgsPointXY
        width_m = da.measureLine(QgsPointXY(ext.xMinimum(), ext.yMinimum()), QgsPointXY(ext.xMaximum(), ext.yMinimum()))
        height_m = da.measureLine(QgsPointXY(ext.xMinimum(), ext.yMinimum()), QgsPointXY(ext.xMinimum(), ext.yMaximum()))
        
        w_km = width_m / 1000.0
        h_km = height_m / 1000.0
        max_dim = max(w_km, h_km)
        
        # Hitung untuk A0
        if max_dim <= 2.5:
            skala_a0 = "1:2.500"
        elif max_dim <= 3.5:
            skala_a0 = "1:5.000"
        elif max_dim <= 7.0:
            skala_a0 = "1:10.000"
        else:
            skala_a0 = "1:10.000 indeks"
            
        # Hitung untuk A1
        if max_dim <= 1.125:
            skala_a1 = "1:2.500"
        elif max_dim <= 2.25:
            skala_a1 = "1:5.000"
        elif max_dim <= 4.5:
            skala_a1 = "1:10.000"
        else:
            skala_a1 = "1:10.000 indeks"
            
        msg = f"<b>Dimensi Area Peta di Layar (Bounding Box):</b><br>"
        msg += f"Barat - Timur: {w_km:.3f} km<br>"
        msg += f"Utara - Selatan: {h_km:.3f} km<br><br>"
        msg += f"Berdasarkan <i>PerKa BIG No. 3/2016</i>, berikut rekomendasi skalanya:<br>"
        msg += f"<ul>"
        msg += f"<li>Untuk kertas <b>A1</b>: Skala Optimal <b>{skala_a1}</b></li>"
        msg += f"<li>Untuk kertas <b>A0</b>: Skala Optimal <b>{skala_a0}</b></li>"
        msg += f"</ul><br>"
        msg += "Catatan: Pastikan Anda telah <b>Zoom to Layer</b> pada batas desa sebelum mengeklik tombol ini agar hasilnya akurat."
        
        QMessageBox.information(self, "Rekomendasi Skala BIG", msg)

