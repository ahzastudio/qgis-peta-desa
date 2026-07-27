# -*- coding: utf-8 -*-
"""
CRS & UTM HELPER UNTUK PETA DESA INDONESIA (SRGI 2013)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
"""

import math
from qgis.core import QgsCoordinateReferenceSystem, QgsRectangle

class CRSHelper:
    """Modul pembantu deteksi Zona UTM dan CRS SRGI 2013 di Indonesia."""

    @staticmethod
    def get_utm_zone_from_lon_lat(lon, lat):
        """Menghitung nomor Zona UTM dan belahan bumi (N/S) dari koordinat lon, lat."""
        zone_number = int(math.floor((lon + 180) / 6)) + 1
        is_northern = lat >= 0
        return zone_number, is_northern

    @staticmethod
    def get_epsg_for_utm(zone_number, is_northern):
        """Mengembalikan EPSG Code WGS 84 / UTM zone (326xx untuk utara, 327xx untuk selatan)."""
        if is_northern:
            return 32600 + zone_number
        else:
            return 32700 + zone_number

    @classmethod
    def auto_detect_utm_crs(cls, extent, crs_in):
        """
        Mendeteksi CRS UTM terbaik untuk extent yang diberikan.
        Mengembalikan QgsCoordinateReferenceSystem.
        """
        try:
            # Transform extent center to WGS84 (EPSG:4326) if needed
            wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
            center = extent.center()
            
            if crs_in != wgs84:
                from qgis.core import QgsCoordinateTransform, QgsProject
                transform = QgsCoordinateTransform(crs_in, wgs84, QgsProject.instance())
                center_geo = transform.transform(center)
            else:
                center_geo = center

            zone, is_north = cls.get_utm_zone_from_lon_lat(center_geo.x(), center_geo.y())
            epsg = cls.get_epsg_for_utm(zone, is_north)
            return QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
        except Exception as e:
            # Fallback ke EPSG:32748 (UTM Zone 48S - Jawa/Sumatra selatan)
            return QgsCoordinateReferenceSystem("EPSG:32748")
