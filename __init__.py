# -*- coding: utf-8 -*-
"""
Plugin Generator Peta Desa PerKa BIG No. 3 Tahun 2016 – QGIS 3.x
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
"""

def classFactory(iface):
    """Entry point untuk memuat plugin ke QGIS."""
    from .plugin import PetaDesaPlugin
    return PetaDesaPlugin(iface)
