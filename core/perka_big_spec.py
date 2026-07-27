# -*- coding: utf-8 -*-
"""
SPESIFIKASI KARTOGRAFI PERKABIG NO. 3 TAHUN 2016 (EXACT GEOMETRI MATEMATIS)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
Formula Presisi Custom A0:
- Lebar  : 1 cm (Margin Kiri) + 76 cm (Neatline Peta) + 1 cm (Gap) + 26 cm (Sidebar) + 1 cm (Margin Kanan) = 105 cm (1050 mm)
- Tinggi : 1 cm (Margin Atas) + 76 cm (Tinggi Peta/Sidebar) + 1 cm (Margin Bawah) = 78 cm (780 mm)
- Isi Peta (Grid) : 75 cm x 75 cm (750 x 750 mm) centered di dalam Neatline 76 x 76 cm
----------------------------------------------------------------------
"""

class PerKaBIGSpec:
    """Spesifikasi teknis resmi PerKa BIG No. 3 Tahun 2016."""

    JENIS_PETA = [
        "PETA CITRA",
        "PETA SARANA DAN PRASARANA",
        "PETA PENUTUP LAHAN DAN PENGGUNAAN LAHAN",
        "PETA ADMINISTRASI"
    ]

    UKURAN_KERTAS = {
        "A1 Custom (660x520 mm)": {"width_mm": 660.0, "height_mm": 520.0},
        "A0 Custom Landscape": {"width_mm": 1050.0, "height_mm": 780.0}
    }

    # Font Specs Exact dari Tabel D-1 PerKa BIG 3/2016
    FONT_SPECS_A1 = {
        "NAMA_DESA": {"family": "Arial", "size": 18, "bold": True, "color": "0,0,0"},
        "JUDUL_PETA": {"family": "Arial", "size": 12, "bold": True, "color": "0,0,0"},
        "NOMOR_LEMBAR": {"family": "Arial", "size": 10, "bold": True, "color": "0,112,192"}, # Blue
        "SKALA_ANGKA": {"family": "Arial", "size": 10, "bold": True, "color": "0,0,0"},
        "LEGENDA": {"family": "Arial Narrow", "size": 8, "bold": False, "color": "0,0,0"},
        "SUMBER_DATA": {"family": "Arial Narrow", "size": 7, "bold": False, "color": "0,0,0"},
        "CATATAN": {"family": "Arial Narrow", "size": 7, "bold": False, "color": "0,0,0"}
    }

    FONT_SPECS_A0 = {
        "NAMA_DESA": {"family": "Arial", "size": 35, "bold": True, "color": "0,0,0"},
        "JUDUL_PETA": {"family": "Arial", "size": 22, "bold": True, "color": "0,0,0"},
        "NOMOR_LEMBAR": {"family": "Arial", "size": 18, "bold": True, "color": "0,112,192"},
        "SKALA_ANGKA": {"family": "Arial", "size": 18, "bold": True, "color": "0,0,0"},
        "LEGENDA": {"family": "Arial Narrow", "size": 14, "bold": False, "color": "0,0,0"},
        "SUMBER_DATA": {"family": "Arial Narrow", "size": 12, "bold": False, "color": "0,0,0"},
        "CATATAN": {"family": "Arial Narrow", "size": 12, "bold": False, "color": "0,0,0"}
    }

    # Dimensi Presisi Custom A1 (Sesuai Permintaan Spesifik Pengguna)
    LAYOUT_DIMENSI_A1 = {
        "kertas": {"w": 660.0, "h": 520.0},
        "neatline_luar": {"x": 15.0, "y": 15.0, "w": 630.0, "h": 490.0, "stroke": 0.70},
        "neatline_dalam": {"x": 25.0, "y": 25.0, "w": 470.0, "h": 470.0, "stroke": 0.50},
        "peta_utama": {"x": 30.0, "y": 30.0, "w": 460.0, "h": 460.0, "stroke": 0.50},
        "panel_info": {"x": 505.0, "y": 25.0, "w": 130.0, "h": 470.0, "stroke": 0.50},
        "inset_1": {"w": 40.0, "h": 40.0},
        "inset_2": {"w": 40.0, "h": 40.0},
        "logo": {"w": 15.0, "h": 15.0},
        "arah_utara": {"w": 28.0, "h": 36.0}
    }

    # Custom A0 Dimensi Matrik Sempurna 1050 x 780 mm
    LAYOUT_DIMENSI_A0 = {
        "neatline_dalam": {"x": 10.0, "y": 10.0, "w": 760.0, "h": 760.0, "stroke": 0.50}, # 76 x 76 cm
        "peta_utama": {"x": 15.0, "y": 15.0, "w": 750.0, "h": 750.0, "stroke": 0.50}, # 75 x 75 cm
        "panel_info": {"x": 780.0, "y": 10.0, "w": 260.0, "h": 760.0, "stroke": 0.50}, # 26 x 76 cm
        "arah_utara": {"w": 50.0, "h": 65.0}
    }

    WARNA_STANDAR = {
        "HITAM": {"rgb": (0, 0, 0), "cmyk": (0, 0, 0, 100)},
        "TEKS_BIRU": {"rgb": (0, 112, 192), "cmyk": (100, 42, 0, 0)},
        "GARIS_CYAN": {"rgb": (0, 169, 230), "cmyk": (100, 0, 0, 0)},
        "BATAS_KECAMATAN": {"rgb": (255, 128, 0), "cmyk": (0, 17, 50, 0)},
        "BATAS_DESA": {"rgb": (255, 255, 0), "cmyk": (0, 0, 100, 0)},
        "PERAIRAN_SUNGAI": {"rgb": (0, 169, 230), "cmyk": (100, 0, 0, 0)}
    }
