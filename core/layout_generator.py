# -*- coding: utf-8 -*-
"""
LAYOUT GENERATOR ENGINE – QGIS 3.x (PERKABIG NO. 3 TAHUN 2016)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
Deskripsi  : PyQGIS Engine presisi tinggi:
             - Inset Peta (Index Peta): EXACT 8 x 8 cm (80 x 80 mm)
             - North Arrow & Skala : Berada di Header Sidebar / Peta Utama
             - ScaleBar Safety     : Mencegah 'Invalid scale!'
----------------------------------------------------------------------
"""

import os
from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont, QColor

from qgis.core import (
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsFillSymbol,
    QgsLineSymbol,
    QgsLayoutItem,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsLayoutItemMap,
    QgsLayoutItemMapGrid,
    QgsLayoutItemPage,
    QgsLayoutItemPicture,
    QgsLayoutItemScaleBar,
    QgsScaleBarSettings,
    QgsLayoutItemShape,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsPrintLayout,
    QgsProject,
    QgsReadWriteContext,
    QgsRectangle,
    QgsUnitTypes,
)

from .perka_big_spec import PerKaBIGSpec

class PetaDesaLayoutGenerator:
    """Engine pembuat layout cetak QGIS 3.x persis Inset 8x8 cm & North Arrow sempurna."""

    def __init__(self, project=None, iface=None):
        self.project = project or QgsProject.instance()
        self.iface = iface

    def mm_point(self, x, y):
        return QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)

    def mm_size(self, w, h):
        return QgsLayoutSize(w, h, QgsUnitTypes.LayoutMillimeters)

    def add_box(self, layout, x, y, w, h, outline_width=0.35, fill="255,255,255,0", stroke_color="0,0,0,255", item_id=None):
        x += getattr(self, 'dx', 0)
        y += getattr(self, 'dy', 0)
        item = QgsLayoutItemShape(layout)
        item.setShapeType(QgsLayoutItemShape.Rectangle)
        stroke_rgba = [int(c) for c in stroke_color.split(",")]
        symbol = QgsFillSymbol.createSimple({
            "color": fill,
            "outline_color": f"{stroke_rgba[0]},{stroke_rgba[1]},{stroke_rgba[2]},{stroke_rgba[3] if len(stroke_rgba)>3 else 255}",
            "outline_width": str(outline_width),
            "outline_width_unit": "MM",
        })
        item.setSymbol(symbol)
        layout.addLayoutItem(item)
        item.attemptMove(self.mm_point(x, y))
        item.attemptResize(self.mm_size(w, h))
        if item_id:
            item.setId(item_id)
        return item

    def add_line(self, layout, x1, y1, x2, y2, stroke_width=0.5, stroke_color="0,169,230,255", item_id=None):
        x1 += getattr(self, 'dx', 0)
        y1 += getattr(self, 'dy', 0)
        x2 += getattr(self, 'dx', 0)
        y2 += getattr(self, 'dy', 0)
        w = max(abs(x2 - x1), 0.1)
        h = max(abs(y2 - y1), 0.1)
        item = QgsLayoutItemShape(layout)
        item.setShapeType(QgsLayoutItemShape.Rectangle)
        cols = [int(c) for c in stroke_color.split(",")]
        symbol = QgsFillSymbol.createSimple({
            "color": f"{cols[0]},{cols[1]},{cols[2]},{cols[3] if len(cols)>3 else 255}",
            "outline_style": "no",
            "outline_width": "0"
        })
        item.setSymbol(symbol)
        layout.addLayoutItem(item)
        item.attemptMove(self.mm_point(min(x1, x2), min(y1, y2)))
        item.attemptResize(self.mm_size(w, h if h > 0.1 else stroke_width))
        if item_id:
            item.setId(item_id)
        return item

    def add_picture(self, layout, picture_path, x, y, w, h, item_id=None):
        x += getattr(self, 'dx', 0)
        y += getattr(self, 'dy', 0)
        item = QgsLayoutItemPicture(layout)
        item.setPicturePath(picture_path)
        item.setResizeMode(QgsLayoutItemPicture.Zoom)
        item.setPictureAnchor(QgsLayoutItem.Middle)
        layout.addLayoutItem(item)
        item.attemptMove(self.mm_point(x, y))
        item.attemptResize(self.mm_size(w, h))
        if item_id:
            item.setId(item_id)
        return item

    def add_label(self, layout, text, x, y, w, h, size=9, bold=False,
                  font_family="Arial", color="0,0,0", h_align=Qt.AlignLeft, v_align=Qt.AlignVCenter,
                  frame=False, bg_color=None, item_id=None):
        x += getattr(self, 'dx', 0)
        y += getattr(self, 'dy', 0)
        item = QgsLayoutItemLabel(layout)
        item.setText(text)
        item.setMarginX(1.0)
        item.setMarginY(0.5)
        font = QFont(font_family, int(size))
        font.setBold(bold)
        item.setFont(font)
        
        rgb = [int(c) for c in color.split(",")]
        item.setFontColor(QColor(rgb[0], rgb[1], rgb[2]))

        item.setHAlign(h_align)
        item.setVAlign(v_align)
        item.setFrameEnabled(frame)
        
        if bg_color:
            item.setBackgroundEnabled(True)
            cols = [int(c) for c in bg_color.split(",")]
            item.setBackgroundColor(QColor(cols[0], cols[1], cols[2], cols[3] if len(cols)>3 else 255))
        else:
            item.setBackgroundEnabled(False)

        try:
            item.setMarginX(1.0)
            item.setMarginY(0.5)
        except Exception:
            pass

        layout.addLayoutItem(item)
        item.attemptMove(self.mm_point(x, y))
        item.attemptResize(self.mm_size(w, h))
        if item_id:
            item.setId(item_id)
        return item

    def get_project_extent(self):
        if self.iface:
            try:
                ext = self.iface.mapCanvas().extent()
                if ext and not ext.isEmpty():
                    return QgsRectangle(ext)
            except Exception:
                pass

        combined = None
        for lyr in self.project.mapLayers().values():
            try:
                if not lyr.isValid():
                    continue
                e = lyr.extent()
                if e.isEmpty():
                    continue
                if combined is None:
                    combined = QgsRectangle(e)
                else:
                    combined.combineExtentWith(e)
            except Exception:
                continue

        if combined is not None and not combined.isEmpty():
            return combined

        return QgsRectangle(0, 0, 10000, 10000)

    def find_north_arrow_svg(self):
        # 1. Mengutamakan SVG Arah Utara kompas PerKa BIG resmi di folder resources plugin
        plugin_dir = os.path.dirname(os.path.dirname(__file__))
        custom_svg = os.path.join(plugin_dir, "resources", "NorthArrow_12.svg")
        if os.path.exists(custom_svg):
            return custom_svg

        # 2. Candidate fallback dari SVG QGIS system (menghindari default.svg yang berupa lingkaran polos)
        candidates = [
            "north_arrows/NorthArrow_01.svg",
            "north_arrows/NorthArrow_02.svg",
            "north_arrows/NorthArrow_04.svg",
            "arrows/NorthArrow_01.svg"
        ]
        for root in QgsApplication.svgPaths():
            for rel in candidates:
                p = os.path.join(root, rel)
                if os.path.exists(p):
                    return p
            for sub in ["north_arrows", "arrows"]:
                d = os.path.join(root, sub)
                if os.path.exists(d):
                    try:
                        for f in os.listdir(d):
                            if f.lower().endswith(".svg") and f.lower() != "default.svg" and ("north" in f.lower() or "arrow" in f.lower()):
                                return os.path.join(d, f)
                    except Exception:
                        pass
        return None

    def setup_main_map_grids(self, map_item, skala, is_a0=False):
        """Membuat 2 Grid pada Peta Utama: Grid 1 Geografis (DMS) & Grid 2 UTM (Meter)."""
        try:

            # 1. Grid Graticul (Geografis DMS: 10 detik = 0.002777777778)
            grid1 = QgsLayoutItemMapGrid("Graticul", map_item)
            map_item.grids().addGrid(grid1)
            grid1.setEnabled(True)
            grid1.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
            grid1.setIntervalX(0.002777777778)
            grid1.setIntervalY(0.002777777778)
            grid1.setAnnotationEnabled(True)
            grid1.setAnnotationFormat(QgsLayoutItemMapGrid.CustomFormat)
            grid1.setAnnotationExpression(
                "replace("
                "replace("
                "replace("
                "replace("
                "to_dms(@grid_number, @grid_axis, 0, 'aligned'), "
                "'E', ' BT'), "
                "'W', ' BB'), "
                "'N', ' LU'), "
                "'S', ' LS')"
            )
            
            grid1.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Top)
            grid1.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Bottom)
            grid1.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Left)
            grid1.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Right)
            
            grid1.setAnnotationDirection(QgsLayoutItemMapGrid.Horizontal, QgsLayoutItemMapGrid.Top)
            grid1.setAnnotationDirection(QgsLayoutItemMapGrid.Horizontal, QgsLayoutItemMapGrid.Bottom)
            grid1.setAnnotationDirection(QgsLayoutItemMapGrid.Vertical, QgsLayoutItemMapGrid.Left)
            grid1.setAnnotationDirection(QgsLayoutItemMapGrid.Vertical, QgsLayoutItemMapGrid.Right)
            
            grid1.setAnnotationFrameDistance(1.0 if is_a0 else 0.5)

            grid1.setFrameStyle(QgsLayoutItemMapGrid.ExteriorTicks)
            grid1.setFrameWidth(1.2)
            # Warna biru azure (#0070ff) untuk Grid Geografis (Graticul)
            azure_color = QColor(0, 112, 255)
            grid1.setAnnotationFontColor(azure_color)
            line_symbol1 = QgsLineSymbol.createSimple({'color': '115,223,255,255', 'width': '0.3'})
            grid1.setLineSymbol(line_symbol1)
            try:
                txt_fmt = grid1.annotationTextFormat()
                txt_fmt.setFont(QFont("Arial"))
                txt_fmt.setSize(10.0 if is_a0 else 7.0)
                grid1.setAnnotationTextFormat(txt_fmt)
            except Exception as e:
                with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                    f.write(f"Error Font Grid 1: {e}\n")

            # 2. Grid Measure (UTM Meter: 500m)
            grid2 = QgsLayoutItemMapGrid("Measure", map_item)
            map_item.grids().addGrid(grid2)
            grid2.setEnabled(True)
            
            # Deteksi CRS UTM yang sesuai jika project CRS adalah WGS84
            utm_crs = self.project.crs()
            if utm_crs.authid() == 'EPSG:4326':
                extent = map_item.extent()
                lon = extent.center().x()
                zone = int((lon + 180) / 6) + 1
                epsg_code = 32600 + zone if extent.center().y() >= 0 else 32700 + zone
                utm_crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg_code}")
                
            grid2.setCrs(utm_crs)
            grid2.setIntervalX(500.0)
            grid2.setIntervalY(500.0)
            grid2.setAnnotationEnabled(True)
            grid2.setAnnotationFormat(QgsLayoutItemMapGrid.CustomFormat)
            grid2.setAnnotationExpression(
                "CASE\n"
                "  WHEN @grid_axis = 'x' THEN format_number(@grid_number, 0) || ' mT'\n"
                "  WHEN @grid_axis = 'y' THEN format_number(@grid_number, 0) || ' mU'\n"
                "END"
            )
            grid2.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Top)
            grid2.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Bottom)
            grid2.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Left)
            grid2.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Right)

            grid2.setAnnotationDirection(QgsLayoutItemMapGrid.Horizontal, QgsLayoutItemMapGrid.Top)
            grid2.setAnnotationDirection(QgsLayoutItemMapGrid.Horizontal, QgsLayoutItemMapGrid.Bottom)
            grid2.setAnnotationDirection(QgsLayoutItemMapGrid.Vertical, QgsLayoutItemMapGrid.Left)
            grid2.setAnnotationDirection(QgsLayoutItemMapGrid.Vertical, QgsLayoutItemMapGrid.Right)
            
            # Beri offset/jarak agar label UTM tidak menabrak label DMS
            grid2.setAnnotationFrameDistance(7.0 if is_a0 else 5.0)

            grid2.setStyle(QgsLayoutItemMapGrid.Cross)
            grid2.setCrossLength(2.0)
            grid2.setFrameStyle(QgsLayoutItemMapGrid.ExteriorTicks)
            grid2.setFrameWidth(1.2)
            # Warna hitam untuk Grid UTM (Measure)
            black_color = QColor(0, 0, 0)
            grid2.setAnnotationFontColor(black_color)
            line_symbol2 = QgsLineSymbol.createSimple({'color': '0,0,0,255', 'width': '0.1'})
            grid2.setLineSymbol(line_symbol2)
            try:
                txt_fmt = grid2.annotationTextFormat()
                txt_fmt.setFont(QFont("Arial"))
                txt_fmt.setSize(12.0 if is_a0 else 8.0)
                grid2.setAnnotationTextFormat(txt_fmt)
            except Exception as e:
                with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                    f.write(f"Error Font Grid 2: {e}\n")

        except Exception as exc:
            import traceback
            with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                f.write(f"Error Grid Utama: {exc}\n{traceback.format_exc()}\n")

    def setup_inset1_grid(self, inset_item, is_a0=False):
        """Membuat Grid 10 Menit pada Inset 1 (Petunjuk Letak Peta)."""
        try:
            grid = QgsLayoutItemMapGrid("Grid 1", inset_item)
            inset_item.grids().addGrid(grid)
            grid.setEnabled(True)
            grid.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
            grid.setIntervalX(0.166666666667)
            grid.setIntervalY(0.166666666667)
            
            # Warna biru azure (#0070ff) untuk Grid Inset agar seragam dengan Juknis BIG
            azure_color = QColor(0, 112, 255)
            grid.setAnnotationFontColor(azure_color)
            line_symbol = QgsLineSymbol.createSimple({'color': '115,223,255,255', 'width': '0.1'})
            grid.setLineSymbol(line_symbol)
            
            grid.setAnnotationEnabled(True)
            grid.setAnnotationFormat(QgsLayoutItemMapGrid.CustomFormat)
            grid.setAnnotationExpression("to_dms(abs(coalesce(@grid_number, 0)), 'x', 0, '')")
            
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.HideAll, QgsLayoutItemMapGrid.Top)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.HideAll, QgsLayoutItemMapGrid.Left)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.ShowAll, QgsLayoutItemMapGrid.Bottom)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.ShowAll, QgsLayoutItemMapGrid.Right)
            
            try:
                txt_fmt = grid.annotationTextFormat()
                txt_fmt.setFont(QFont("Arial"))
                txt_fmt.setSize(10.0 if is_a0 else 6.0)
                grid.setAnnotationTextFormat(txt_fmt)
            except Exception as e:
                with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                    f.write(f"Error Font Inset 1: {e}\n")
        except Exception as exc:
            import traceback
            with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                f.write(f"Error Grid Inset 1: {exc}\n{traceback.format_exc()}\n")

    def setup_inset2_grid(self, inset_item, main_map, config, is_a0=False):
        """Membuat Grid & Overview Cakupan Peta Utama pada Inset 2 (Diagram Lokasi)."""
        try:
            from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem
            
            grid = QgsLayoutItemMapGrid("Grid 1", inset_item)
            inset_item.grids().addGrid(grid)
            grid.setEnabled(True)
            
            crsDest = QgsCoordinateReferenceSystem("EPSG:4326")
            grid.setCrs(crsDest)
            
            if config.get("grid_simetris", True):
                # Mode Simetris (Relatif)
                crsSrc = main_map.layout().project().crs()
                transform = QgsCoordinateTransform(crsSrc, crsDest, main_map.layout().project())
                main_ext_wgs = transform.transformBoundingBox(main_map.extent())
                
                grid.setIntervalX(main_ext_wgs.width())
                grid.setIntervalY(main_ext_wgs.height())
                grid.setOffsetX(main_ext_wgs.xMinimum())
                grid.setOffsetY(main_ext_wgs.yMinimum())
            else:
                # Mode Standar (Absolut 1-Menit)
                grid.setIntervalX(0.016666666667)
                grid.setIntervalY(0.016666666667)
            
            # Warna biru azure (#0070ff) untuk teks dan garis grid agar seragam dengan Juknis BIG
            azure_color = QColor(0, 112, 255)
            grid.setAnnotationFontColor(azure_color)
            line_symbol = QgsLineSymbol.createSimple({'color': '115,223,255,255', 'width': '0.4'})
            grid.setLineSymbol(line_symbol)
            
            grid.setAnnotationEnabled(True)
            grid.setAnnotationFormat(QgsLayoutItemMapGrid.CustomFormat)
            grid.setAnnotationExpression("to_dms(abs(coalesce(@grid_number, 0)), 'x', 0, '')")
            
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.HideAll, QgsLayoutItemMapGrid.Top)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.HideAll, QgsLayoutItemMapGrid.Left)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.ShowAll, QgsLayoutItemMapGrid.Bottom)
            grid.setAnnotationDisplay(QgsLayoutItemMapGrid.ShowAll, QgsLayoutItemMapGrid.Right)
            
            try:
                txt_fmt = grid.annotationTextFormat()
                txt_fmt.setFont(QFont("Arial"))
                txt_fmt.setSize(10.0 if is_a0 else 6.0)
                grid.setAnnotationTextFormat(txt_fmt)
            except Exception as e:
                with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                    f.write(f"Error Font Inset 2: {e}\n")

            # Hapus overview lama dengan removeOverview jika ada, atau buat yang baru
            try:
                if inset_item.overviews().overview("Overview 1"):
                    inset_item.overviews().removeOverview("Overview 1")
            except Exception:
                pass
                
            from qgis.core import QgsLayoutItemMapOverview
            overview = QgsLayoutItemMapOverview("Overview 1", inset_item)
            inset_item.overviews().addOverview(overview)
            
            overview.setLinkedMap(main_map)
            overview.setEnabled(True)
            symbol = QgsFillSymbol.createSimple({'color': '255,0,0,50', 'outline_color': '255,0,0,255', 'outline_width': '0.5'})
            overview.setFrameSymbol(symbol)
        except Exception as exc:
            import traceback
            with open(r"d:\TOOLBOX\TEMPLATE PETA DESA\error_log.txt", "a") as f:
                f.write(f"Error Grid Inset 2: {exc}\n{traceback.format_exc()}\n")

    def generate_layout(self, config):
        """Membuat Layout Peta Desa presisi tinggi dengan Inset 8x8 cm dan North Arrow sempurna."""
        layout_name = f"PETA_DESA_{config['nama_desa'].upper()}"
        manager = self.project.layoutManager()

        for old in list(manager.printLayouts()):
            if old.name() == layout_name:
                manager.removeLayout(old)

        layout = QgsPrintLayout(self.project)
        layout.initializeDefaults()
        layout.setName(layout_name)

        ukuran_kertas = config.get("ukuran_kertas", "A1 Landscape (Custom 660x520 mm)")
        is_a0 = "A0" in ukuran_kertas
        is_real = "Real" in ukuran_kertas

        if is_a0:
            content_w, content_h = 1080.0, 810.0
            page_w, page_h = (1189.0, 841.0) if is_real else (1080.0, 810.0)
            self.dx = (page_w - content_w) / 2.0
            self.dy = (page_h - content_h) / 2.0
            
            # Custom A0 Presisi Matrik
            neat_luar_x, neat_luar_y, neat_luar_w, neat_luar_h = 15.0, 15.0, 1050.0, 780.0
            neat_dalam_x, neat_dalam_y, neat_dalam_w, neat_dalam_h = 25.0, 25.0, 760.0, 760.0
            map_x, map_y, map_w, map_h = 30.0, 30.0, 750.0, 750.0
            panel_x, panel_y, panel_w, panel_h = 795.0, 25.0, 260.0, 760.0
            font_desa_sz = 26
            font_sub_sz = 11
            box_inset_w, box_inset_h = 122.0, 92.0
            inset_w, inset_h = 90.0, 80.0
            inset_x_off1, inset_x_off2 = 22.0, 148.0
            logo_w, logo_h = 30.0, 18.0
        else:
            content_w, content_h = 660.0, 520.0
            page_w, page_h = (841.0, 594.0) if is_real else (660.0, 520.0)
            self.dx = (page_w - content_w) / 2.0
            self.dy = (page_h - content_h) / 2.0
            
            # Standar Presisi A1 Custom: Lebar 660 mm, Tinggi 520 mm (Sesuai Spesifikasi Pengguna)
            neat_luar_x, neat_luar_y, neat_luar_w, neat_luar_h = 15.0, 15.0, 630.0, 490.0
            neat_dalam_x, neat_dalam_y, neat_dalam_w, neat_dalam_h = 25.0, 25.0, 470.0, 470.0 
            map_x, map_y, map_w, map_h = 30.0, 30.0, 460.0, 460.0 
            panel_x, panel_y, panel_w, panel_h = 505.0, 25.0, 130.0, 470.0 
            font_desa_sz = 14
            font_sub_sz = 8
            box_inset_w, box_inset_h = 57.0, 52.0
            inset_w, inset_h = 40.0, 40.0 # EXACT 40 x 40 mm!
            inset_x_off1, inset_x_off2 = 14.5, 77.5
            logo_w, logo_h = 15.0, 15.0 # EXACT 15 x 15 mm!

        # Halaman Kertas
        pages = layout.pageCollection()
        while pages.pageCount() > 0:
            pages.deletePage(0)

        page = QgsLayoutItemPage(layout)
        page.setPageSize(self.mm_size(page_w, page_h))
        pages.addPage(page)

        # 0. NEATLINE BINGKAI LUAR & DALAM
        self.add_box(layout, neat_luar_x, neat_luar_y, neat_luar_w, neat_luar_h, outline_width=0.70, item_id="NEATLINE_LUAR")
        self.add_box(layout, neat_dalam_x, neat_dalam_y, neat_dalam_w, neat_dalam_h, outline_width=0.50, item_id="NEATLINE_DALAM")

        # 1. PETA UTAMA (ISI PETA GRID: 460 x 460 mm)
        main_map = QgsLayoutItemMap(layout)
        main_map.setId("PETA_UTAMA")
        main_map.setFrameEnabled(True)
        layout.addLayoutItem(main_map)

        main_map.attemptMove(self.mm_point(map_x + getattr(self, 'dx', 0), map_y + getattr(self, 'dy', 0)))
        main_map.attemptResize(self.mm_size(map_w, map_h))

        ext = self.get_project_extent()
        main_map.setExtent(ext)
        # setExtent automatically resizes the layout item to match the extent's aspect ratio!
        # We MUST restore the square size (460x460) before setting the scale!
        main_map.attemptResize(self.mm_size(map_w, map_h))
        
        skala = int(config.get("skala_utama", 5000))
        try:
            main_map.setScale(skala)
        except Exception:
            pass

        self.setup_main_map_grids(main_map, skala, is_a0=is_a0)

        # 2. SIDEBAR PANEL INFORMASI KANAN (130 x 470 mm)
        self.add_box(layout, panel_x, panel_y, panel_w, panel_h, outline_width=0.50, item_id="PANEL_INFORMASI")

        # A. Header Judul Peta Desa (Ekstrak Presisi QPT)
        jenis_peta = config.get('jenis_peta', 'PETA ADMINISTRASI').upper()
        lembar_txt = f"LEMBAR : {config.get('nomor_lembar', '..................')}"
        nama_desa = config.get('nama_desa', '').strip()
        desa_txt = f"DESA {nama_desa.upper()}" if nama_desa else "DESA ................................."
        nama_kecamatan = config.get('nama_kecamatan', '').strip()
        kec_txt = f"KECAMATAN {nama_kecamatan.upper()}" if nama_kecamatan else "KECAMATAN ....................."
        nama_kabupaten = config.get('nama_kabupaten', '').strip()
        kab_txt = f"KABUPATEN {nama_kabupaten.upper()}" if nama_kabupaten else "KABUPATEN ....................."
        
        if is_a0:
            self.add_label(layout, jenis_peta, panel_x + 12, 35.0, 230.0, 10.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_JENIS")
            self.add_label(layout, lembar_txt, panel_x + 12, 48.0, 230.0, 8.0, size=20, bold=True, color="0,112,192", h_align=Qt.AlignLeft, item_id="JUDUL_LEMBAR")
            self.add_label(layout, desa_txt, panel_x + 12, 60.0, 236.0, 15.0, size=40, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_DESA")
            self.add_label(layout, kec_txt, panel_x + 12, 80.0, 236.0, 12.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KEC")
            self.add_label(layout, kab_txt, panel_x + 12, 95.0, 236.0, 12.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KAB")
        else:
            self.add_label(layout, jenis_peta, panel_x + 6, 29.0, 90.0, 6.0, size=14, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_JENIS")
            self.add_label(layout, lembar_txt, panel_x + 6, 36.0, 90.0, 5.0, size=13, bold=True, color="0,112,192", h_align=Qt.AlignLeft, item_id="JUDUL_LEMBAR")
            self.add_label(layout, desa_txt, panel_x + 6, 42.0, 118.0, 10.0, size=25, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_DESA")
            self.add_label(layout, kec_txt, panel_x + 6, 52.0, 118.0, 7.0, size=14, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KEC")
            self.add_label(layout, kab_txt, panel_x + 6, 59.0, 118.0, 7.0, size=14, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KAB")

        # B. Orientasi Utara (North Arrow) & Skala (Ekstrak Presisi QPT)
        north_svg = self.find_north_arrow_svg()

        if is_a0:
            north_w, north_h = 40.0, 40.0
            north_x, north_y = panel_x + 15.0, 115.0
            
            if north_svg:
                north = QgsLayoutItemPicture(layout)
                north.setId("ARAH_UTARA")
                north.setPicturePath(north_svg)
                north.setFrameEnabled(False)
                north.setBackgroundEnabled(False)
                layout.addLayoutItem(north)
                north.attemptMove(self.mm_point(north_x + getattr(self, 'dx', 0), north_y + getattr(self, 'dy', 0)))
                north.attemptResize(self.mm_size(north_w, north_h))
            else:
                self.add_label(layout, "U\n↑", north_x, north_y, north_w, north_h, size=20, bold=True, h_align=Qt.AlignCenter, frame=False, item_id="ARAH_UTARA")
                
            self.add_label(layout, f"SKALA 1 : {skala:,}".replace(",", "."), panel_x + 65.0, 120.0, 150.0, 10.0, size=22, bold=True, h_align=Qt.AlignLeft, item_id="SKALA_ANGKA")
            
            scale_bar = QgsLayoutItemScaleBar(layout)
            scale_bar.setId("SKALA_GRAFIS")
            scale_bar.setLinkedMap(main_map)
            scale_bar.setStyle("Double Box")
            scale_bar.setUnits(QgsUnitTypes.DistanceMeters)
            scale_bar.setUnitLabel("m")
            scale_bar.setNumberOfSegments(8)
            scale_bar.setNumberOfSegmentsLeft(0)
            try:
                scale_bar.setUnitsPerSegment(skala / 100.0)
                scale_bar.setHeight(6.0)
            except Exception:
                pass
            scale_bar.setFrameEnabled(False)
            scale_bar.setBackgroundEnabled(False)
            layout.addLayoutItem(scale_bar)
            scale_bar.attemptMove(self.mm_point(panel_x + 65.0 + getattr(self, 'dx', 0), 135.0 + getattr(self, 'dy', 0)))
            scale_bar.attemptResize(self.mm_size(160.0, 20.0))
            try:
                scale_bar.update()
            except Exception:
                pass
                
            self.add_line(layout, panel_x, 170.0, panel_x + panel_w, 170.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_1")

        else:
            north_w, north_h = 20.0, 20.0
            north_x = 504.75
            north_y = 67.67

            if north_svg:
                north = QgsLayoutItemPicture(layout)
                north.setId("ARAH_UTARA")
                north.setPicturePath(north_svg)
                north.setFrameEnabled(False)
                north.setBackgroundEnabled(False)
                layout.addLayoutItem(north)
                north.attemptMove(self.mm_point(north_x + getattr(self, 'dx', 0), north_y + getattr(self, 'dy', 0)))
                north.attemptResize(self.mm_size(north_w, north_h))
            else:
                self.add_label(layout, "U\n↑", north_x, north_y, north_w, north_h, size=11, bold=True, h_align=Qt.AlignCenter, frame=False, item_id="ARAH_UTARA")

            # Teks Skala Angka
            self.add_label(layout, f"SKALA 1 : {skala:,}".replace(",", "."), 521.32, 69.02, 85.0, 5.0, size=13, bold=True, h_align=Qt.AlignLeft, item_id="SKALA_ANGKA")

            # Skala Grafis (Scale Bar)
            scale_bar = QgsLayoutItemScaleBar(layout)
            scale_bar.setId("SKALA_GRAFIS")
            scale_bar.setLinkedMap(main_map)
            scale_bar.setStyle("Double Box")
            scale_bar.setUnits(QgsUnitTypes.DistanceMeters)
            scale_bar.setUnitLabel("m")
            scale_bar.setNumberOfSegments(8)
            scale_bar.setNumberOfSegmentsLeft(0)
            
            try:
                # 1 cm di kertas = skala / 100 meter di lapangan (contoh 1:5000 -> 50 meter per segmen)
                seg = skala / 100.0
                scale_bar.setUnitsPerSegment(seg)
                scale_bar.setHeight(3.0)
                try:
                    scale_bar.setSegmentSizeMode(QgsScaleBarSettings.SegmentSizeFixed)
                except Exception:
                    pass
            except Exception:
                pass

            scale_bar.setFrameEnabled(False)
            scale_bar.setBackgroundEnabled(False)
            layout.addLayoutItem(scale_bar)
            scale_bar.attemptMove(self.mm_point(521.32 + getattr(self, 'dx', 0), 74.02 + getattr(self, 'dy', 0)))
            scale_bar.attemptResize(self.mm_size(92.4, 13.2))
            try:
                scale_bar.update()
            except Exception:
                pass

            # Garis Pembatas Aksen Cyan (#00A9E6)
            self.add_line(layout, 509.0, 90.0, 631.0, 90.0, stroke_width=0.8, stroke_color="0,169,230,255", item_id="LINE_DIV_1")

        # D. Inset Ganda (Petunjuk Letak Peta & Diagram Lokasi) - Ekstrak Presisi QPT
        if is_a0:
            self.add_label(layout, "PETUNJUK LETAK PETA", panel_x + 10, 180.0, 110.0, 10.0, size=14, bold=True, h_align=Qt.AlignCenter, item_id="TXT_INSET_1")
            inset1 = QgsLayoutItemMap(layout)
            inset1.setId("PETA_INSET_1")
            inset1.setFrameEnabled(True)
            layout.addLayoutItem(inset1)
            inset1.attemptMove(self.mm_point(panel_x + 15 + getattr(self, 'dx', 0), 195.0 + getattr(self, 'dy', 0)))
            inset1.attemptResize(self.mm_size(100.0, 100.0))

            self.add_label(layout, "DIAGRAM LOKASI", panel_x + 140, 180.0, 110.0, 10.0, size=14, bold=True, color="0,112,255", h_align=Qt.AlignCenter, item_id="TXT_DIAGRAM_LOKASI")
            inset2 = QgsLayoutItemMap(layout)
            inset2.setId("DIAGRAM_LOKASI")
            inset2.setFrameEnabled(True)
            layout.addLayoutItem(inset2)
            inset2.attemptMove(self.mm_point(panel_x + 145 + getattr(self, 'dx', 0), 195.0 + getattr(self, 'dy', 0)))
            inset2.attemptResize(self.mm_size(100.0, 100.0))
        else:
            self.add_label(layout, "PETUNJUK LETAK PETA", 509.0, 95.0, 57.0, 6.0, size=7.0, bold=True, font_family="Arial Narrow", h_align=Qt.AlignCenter, item_id="TXT_INSET_1")
            
            inset1 = QgsLayoutItemMap(layout)
            inset1.setId("PETA_INSET_1")
            inset1.setFrameEnabled(True)
            layout.addLayoutItem(inset1)
            inset1.attemptMove(self.mm_point(517.5 + getattr(self, 'dx', 0), 104.0 + getattr(self, 'dy', 0)))
            inset1.attemptResize(self.mm_size(40.0, 40.0))

            # Kotak 2: Diagram Lokasi
            self.add_label(layout, "DIAGRAM LOKASI", 574.0, 95.0, 57.0, 6.0, size=7.0, bold=True, font_family="Arial Narrow", color="0,112,255", h_align=Qt.AlignCenter, item_id="TXT_DIAGRAM_LOKASI")

            inset2 = QgsLayoutItemMap(layout)
            inset2.setId("DIAGRAM_LOKASI")
            inset2.setFrameEnabled(True)
            layout.addLayoutItem(inset2)
            inset2.attemptMove(self.mm_point(582.5 + getattr(self, 'dx', 0), 104.0 + getattr(self, 'dy', 0)))
            inset2.attemptResize(self.mm_size(40.0, 40.0))

        inset_extent = QgsRectangle(ext)
        try:
            inset_extent.scale(4.0)
            # Buat extent bujursangkar presisi (rasio 1:1) untuk Inset 1
            cx = inset_extent.center().x()
            cy = inset_extent.center().y()
            side = max(inset_extent.width(), inset_extent.height())
            square_extent = QgsRectangle(cx - side/2.0, cy - side/2.0, cx + side/2.0, cy + side/2.0)
            
            inset1.setExtent(square_extent)
            if is_a0:
                inset1.attemptResize(self.mm_size(100.0, 100.0))
                inset1.setScale(1500000)
                
                from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem
                
                crsSrc = self.project.crs()
                crsDest = QgsCoordinateReferenceSystem("EPSG:4326")
                transform = QgsCoordinateTransform(crsSrc, crsDest, self.project)
                
                inset2.setCrs(crsDest)
                inset2.attemptResize(self.mm_size(100.0, 100.0))
            else:
                inset1.attemptResize(self.mm_size(40.0, 40.0))
                inset1.setScale(1500000)
                
                from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem
                
                crsSrc = self.project.crs()
                crsDest = QgsCoordinateReferenceSystem("EPSG:4326")
                transform = QgsCoordinateTransform(crsSrc, crsDest, self.project)
                
                inset2.setCrs(crsDest)
                inset2.attemptResize(self.mm_size(40.0, 40.0))
            
            if config.get("grid_simetris", True):
                # Extent selebar 3x3 dari Peta Utama, agar pas di tengah!
                main_ext_wgs = transform.transformBoundingBox(main_map.extent())
                w = main_ext_wgs.width()
                h = main_ext_wgs.height()
                extent_3x3 = QgsRectangle(
                    main_ext_wgs.xMinimum() - w,
                    main_ext_wgs.yMinimum() - h,
                    main_ext_wgs.xMaximum() + w,
                    main_ext_wgs.yMaximum() + h
                )
                inset2.zoomToExtent(extent_3x3)
            else:
                # Mode absolut: snap ke 1-menit terdekat
                import math
                center_wgs = transform.transform(main_map.extent().center())
                cx_wgs = center_wgs.x()
                cy_wgs = center_wgs.y()
                grid_interval = 1.0 / 60.0
                min_x = math.floor(cx_wgs / grid_interval) * grid_interval
                min_y = math.floor(cy_wgs / grid_interval) * grid_interval
                box_cx = min_x + (grid_interval / 2.0)
                box_cy = min_y + (grid_interval / 2.0)
                half_span = 1.5 * grid_interval
                extent_wgs = QgsRectangle(box_cx - half_span, box_cy - half_span, box_cx + half_span, box_cy + half_span)
                inset2.zoomToExtent(extent_wgs)
            
            # Pasang Grid 10 Menit untuk Inset 1 & Grid 1 Menit + Overview untuk Inset 2
            self.setup_inset1_grid(inset1, is_a0=is_a0)
            self.setup_inset2_grid(inset2, main_map, config, is_a0=is_a0)
        except Exception:
            pass

        # Metadata Koordinat di bawah Inset
        meta_srs_left = (
            "Proyeksi\n"
            "Sistem Grid\n"
            "Datum Horizontal"
        )
        meta_srs_right = (
            ":  Universal Transverse Mercator (UTM)\n"
            ":  Grid Geografi dan Grid UTM\n"
            ":  SRGI 2013 / WGS 1984"
        )
        if is_a0:
            self.add_label(layout, meta_srs_left, panel_x + 10, 305.0, 70.0, 20.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_SRS_LEFT")
            self.add_label(layout, meta_srs_right, panel_x + 85, 305.0, 160.0, 20.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_SRS_RIGHT")
            self.add_line(layout, panel_x, 335.0, panel_x + panel_w, 335.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_2")
        else:
            self.add_label(layout, meta_srs_left, 511.0, 148.0, 25.0, 14.0, size=7, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_SRS_LEFT")
            self.add_label(layout, meta_srs_right, 536.0, 148.0, 93.0, 14.0, size=7, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_SRS_RIGHT")
            self.add_line(layout, 509.0, 165.0, 631.0, 165.0, stroke_width=0.8, stroke_color="0,169,230,255", item_id="LINE_DIV_2")

        # E. Logo & Penerbit Block - Ekstrak Presisi QPT
        logo_path = config.get("logo_path", "").strip()
        if not logo_path or not os.path.isfile(logo_path):
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo-ahza.png")
            
        desa = config.get('nama_desa', '').strip() or "(NAMA DESA)"
        kecamatan = config.get('nama_kecamatan', '').strip() or "(NAMA KECAMATAN)"
        kabupaten = config.get('nama_kabupaten', '').strip() or "(NAMA KABUPATEN)"
        provinsi = config.get('nama_provinsi', '').strip() or "(NAMA PROVINSI)"
        kodepos = config.get('kode_pos', '').strip()
        tahun = config.get('tahun_peta', '2026').strip()
        
        kodepos_str = f" {kodepos}" if kodepos else ""
        
        penerbit_txt = (
            f"DICETAK DAN DITERBITKAN OLEH:\n"
            f"PEMERINTAH DESA {desa.upper()} TAHUN {tahun}\n"
            f"KECAMATAN {kecamatan.upper()}\n"
            f"KABUPATEN {kabupaten.upper()}{kodepos_str} - PROVINSI {provinsi.upper()}"
        )

        if is_a0:
            if os.path.isfile(logo_path):
                self.add_picture(layout, logo_path, panel_x + 15, 345.0, 25.0, 25.0, item_id="PIC_LOGO_PEMDA")
            else:
                self.add_box(layout, panel_x + 15, 345.0, 25.0, 25.0, item_id="BOX_LOGO_PEMDA")
                self.add_label(layout, "LOGO\nPEMDA", panel_x + 15, 345.0, 25.0, 25.0, size=8, bold=True, font_family="Arial Narrow", h_align=Qt.AlignCenter, item_id="TXT_LOGO_PEMDA")

            self.add_label(layout, penerbit_txt, panel_x + 45, 345.0, 200.0, 30.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_PENERBIT")
            self.add_line(layout, panel_x, 385.0, panel_x + panel_w, 385.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_3")
        else:
            if os.path.isfile(logo_path):
                self.add_picture(layout, logo_path, 511.0, 171.0, 15.0, 15.0, item_id="PIC_LOGO_PEMDA")
            else:
                self.add_box(layout, 511.0, 171.0, 15.0, 15.0, item_id="BOX_LOGO_PEMDA")
                self.add_label(layout, "LOGO\nPEMDA", 511.0, 171.0, 15.0, 15.0, size=5, bold=True, font_family="Arial Narrow", h_align=Qt.AlignCenter, item_id="TXT_LOGO_PEMDA")

            self.add_label(layout, penerbit_txt, 529.0, 170.0, 102.0, 18.0, size=7, font_family="Arial Narrow", h_align=Qt.AlignLeft, item_id="TXT_PENERBIT")
            self.add_line(layout, 509.0, 198.0, 631.0, 198.0, stroke_width=0.8, stroke_color="0,169,230,255", item_id="LINE_DIV_3")

        # F. Legenda (Keterangan) - Ekstrak Presisi QPT
        legend = QgsLayoutItemLegend(layout)
        legend.setId("LEGENDA")
        legend.setTitle("KETERANGAN")
        legend.setLinkedMap(main_map)
        legend.setFrameEnabled(False)
        legend.setBackgroundEnabled(False)
        
        # 1. Nonaktifkan Auto-Update agar kita bisa filter dan modifikasi node legenda
        legend.setAutoUpdateModel(False)
        try:
            model = legend.model()
            rootGroup = model.rootGroup()
            
            # Cari dan hapus layer basemap otomatis
            basemap_keywords = ['google', 'satellite', 'osm', 'bing', 'tile', 'basemap', 'hybrid', 'terrain']
            nodes_to_remove = []
            
            for layer_node in rootGroup.findLayers():
                lyr_name = layer_node.layerName().lower()
                if any(kw in lyr_name for kw in basemap_keywords):
                    nodes_to_remove.append(layer_node)
                else:
                    # Sembunyikan label nama layer utama agar tidak menghabiskan ruang
                    # Sehingga yang tampil hanya Grup atau langsung ke daftar Simbolnya
                    layer_node.setCustomProperty("legend/title-label", " ")
            
            for node in nodes_to_remove:
                rootGroup.removeChildNode(node)
        except Exception as e:
            print("Legend model error:", e)

        try:
            legend.setColumnCount(2)
            legend.setSplitLayer(True)
            legend.setEqualColumnWidth(False)
        except Exception:
            pass

        layout.addLayoutItem(legend)
        
        # Geser mepet ke garis cyan pinggir dan maksimalkan lebar
        if is_a0:
            legend.attemptMove(self.mm_point(panel_x + 5 + getattr(self, 'dx', 0), 395.0 + getattr(self, 'dy', 0)))
            legend.attemptResize(self.mm_size(250.0, 250.0))
            
            try:
                legend.setTitleFont(QFont("Arial Narrow", 16, QFont.Bold))
                legend.setStyleFont(legend.Title, QFont("Arial Narrow", 16, QFont.Bold))
                legend.setStyleFont(legend.GroupTitle, QFont("Arial Narrow", 12, QFont.Bold))
                legend.setStyleFont(legend.SubgroupTitle, QFont("Arial Narrow", 12, QFont.Bold))
                legend.setStyleFont(legend.SymbolLabel, QFont("Arial Narrow", 10))
            except Exception:
                pass
        else:
            legend.attemptMove(self.mm_point(509.0 + getattr(self, 'dx', 0), 201.0 + getattr(self, 'dy', 0)))
            legend.attemptResize(self.mm_size(120.0, 215.0))
            
            try:
                legend.setTitleFont(QFont("Arial Narrow", 10, QFont.Bold))
                legend.setStyleFont(legend.Title, QFont("Arial Narrow", 10, QFont.Bold))
                legend.setStyleFont(legend.GroupTitle, QFont("Arial Narrow", 8, QFont.Bold))
                legend.setStyleFont(legend.SubgroupTitle, QFont("Arial Narrow", 8, QFont.Bold))
                legend.setStyleFont(legend.SymbolLabel, QFont("Arial Narrow", 6.5))
                
                # Penyesuaian spasi margin agar rapat namun rapi
                legend.setStyleMargin(legend.Title, 3.0)
                legend.setStyleMargin(legend.GroupTitle, 2.0)
                legend.setStyleMargin(legend.SubgroupTitle, 1.5)
                legend.setStyleMargin(legend.SymbolLabel, 1.0)
            except Exception:
                pass

        # G. Footer Sidebar Block - Ekstrak Presisi QPT
        if is_a0:
            self.add_line(layout, panel_x, 650.0, panel_x + panel_w, 650.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_4")

            sumber_custom = config.get("sumber_data", "").strip()
            if not sumber_custom:
                sumber_custom = (
                    ":  1. Peta Rupa Bumi Indonesia (RBI) Tematik 1:25.000\n"
                    "   2. Citra Satelit Resolusi Tinggi (CSRT) SRGI 2013\n"
                    "   3. Batas Desa Delimitasi PerKa BIG 3/2016\n"
                    "   4. DEMNAS Badan Informasi Geospasial"
                )
            self.add_label(layout, "Sumber Data dan Riwayat Peta", panel_x + 5, 655.0, 70.0, 30.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_HEADER")
            self.add_label(layout, sumber_custom, panel_x + 75, 655.0, 175.0, 30.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_ISI")
            
            catatan_isi = ": Batas peta tidak dapat dijadikan acuan hukum sebenarnya di lapangan."
            self.add_label(layout, "Catatan", panel_x + 5, 690.0, 70.0, 15.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_HEADER")
            self.add_label(layout, catatan_isi, panel_x + 75, 690.0, 180.0, 15.0, size=12, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_ISI")
            
            pengesahan_txt = (
                f"Disahkan oleh:\n"
                f"{config.get('jabatan_pengesah', 'Kepala Desa')} {config['nama_desa'].upper()}\n\n\n\n\n\n"
                f"({config.get('nama_pengesah', '[NAMA KEPALA DESA]')})"
            )
            self.add_label(layout, pengesahan_txt, panel_x + 10, 725.0, 240.0, 45.0, size=12, bold=True, font_family="Arial Narrow", h_align=Qt.AlignCenter, v_align=Qt.AlignVCenter, item_id="TXT_PENGESAHAN_FOOTER")
        else:
            self.add_line(layout, 509.0, 419.0, 631.0, 419.0, stroke_width=0.8, stroke_color="0,169,230,255", item_id="LINE_DIV_4")

            # Judul Sumber Data (Kolom Kiri, x=508.88 mm)
            self.add_label(layout, "Sumber Data dan Riwayat Peta", 508.88, 422.0, 39.52, 22.0, size=9, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_HEADER")

            # Isi List Sumber Data (Kolom Kanan, x=546.91 mm)
            sumber_custom = config.get("sumber_data", "").strip()
            if not sumber_custom:
                sumber_custom = (
                    ":  1. Peta Rupa Bumi Indonesia (RBI) Tematik 1:25.000\n"
                    "   2. Citra Satelit Resolusi Tinggi (CSRT) SRGI 2013\n"
                    "   3. Batas Desa Delimitasi PerKa BIG 3/2016\n"
                    "   4. DEMNAS Badan Informasi Geospasial"
                )
            self.add_label(layout, sumber_custom, 546.91, 422.0, 86.56, 22.0, size=9, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_ISI")

            # Judul Catatan (Kolom Kiri, x=511.0 mm)
            self.add_label(layout, "Catatan", 511.0, 446.515, 37.39, 4.65, size=9, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_HEADER")

            # Isi Teks Catatan (Kolom Kanan, x=546.91 mm)
            catatan_isi = ": Batas peta tidak dapat dijadikan acuan hukum\n  sebenarnya di lapangan."
            self.add_label(layout, catatan_isi, 546.91, 446.515, 86.56, 7.66, size=9, font_family="Arial Narrow", h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_ISI")

            # Pengesahan Pejabat Kepala Desa
            pengesahan_txt = (
                f"Disahkan oleh:\n"
                f"{config.get('jabatan_pengesah', 'Kepala Desa')} {config['nama_desa'].upper()}\n\n\n\n\n\n"
                f"({config.get('nama_pengesah', '[NAMA KEPALA DESA]')})"
            )
            self.add_label(layout, pengesahan_txt, 511.0, 457.75, 118.0, 32.4, size=8, bold=True, font_family="Arial Narrow", h_align=Qt.AlignCenter, v_align=Qt.AlignVCenter, item_id="TXT_PENGESAHAN_FOOTER")

        # Tambahkan ke layout manager
        manager.addLayout(layout)

        # Simpan QPT jika dikonfigurasi
        if config.get("output_qpt"):
            try:
                Path(config["output_qpt"]).parent.mkdir(parents=True, exist_ok=True)
                layout.saveAsTemplate(config["output_qpt"], QgsReadWriteContext())
            except Exception as e:
                print("Peringatan QPT:", e)

        if self.iface:
            try:
                self.iface.openLayoutDesigner(layout)
            except Exception:
                pass

        return layout
