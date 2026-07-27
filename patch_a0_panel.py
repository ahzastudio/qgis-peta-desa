import os

file_path = r"d:\TOOLBOX\TEMPLATE PETA DESA\QGIS_Plugin_Peta_Desa\core\layout_generator.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

with open(r"d:\TOOLBOX\TEMPLATE_PETA_DESA_TARGET.txt", "r", encoding="utf-8") as f:
    old_target = f.read()

new_target = """        jenis_peta = config.get('jenis_peta', 'PETA ADMINISTRASI').upper()
        lembar_txt = f"LEMBAR : {config.get('nomor_lembar', '..................')}"
        nama_desa = config.get('nama_desa', '').strip()
        desa_txt = f"DESA {nama_desa.upper()}" if nama_desa else "DESA ................................."
        nama_kecamatan = config.get('nama_kecamatan', '').strip()
        kec_txt = f"KECAMATAN {nama_kecamatan.upper()}" if nama_kecamatan else "KECAMATAN ....................."
        nama_kabupaten = config.get('nama_kabupaten', '').strip()
        kab_txt = f"KABUPATEN {nama_kabupaten.upper()}" if nama_kabupaten else "KABUPATEN ....................."
        
        north_svg = self.find_north_arrow_svg()

        if is_a0:
            # ======================= A0 PANEL =======================
            self.add_label(layout, jenis_peta, panel_x + 12, 35.0, 230.0, 10.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_JENIS")
            self.add_label(layout, lembar_txt, panel_x + 12, 48.0, 230.0, 8.0, size=20, bold=True, color="0,112,192", h_align=Qt.AlignLeft, item_id="JUDUL_LEMBAR")
            self.add_label(layout, desa_txt, panel_x + 12, 60.0, 236.0, 15.0, size=40, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_DESA")
            self.add_label(layout, kec_txt, panel_x + 12, 80.0, 236.0, 12.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KEC")
            self.add_label(layout, kab_txt, panel_x + 12, 95.0, 236.0, 12.0, size=24, bold=True, h_align=Qt.AlignLeft, item_id="JUDUL_KAB")

            north_w, north_h = 40.0, 40.0
            north_x = panel_x + 15
            north_y = 115.0
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
                self.add_label(layout, "U\\n↑", north_x, north_y, north_w, north_h, size=20, bold=True, h_align=Qt.AlignCenter, frame=False, item_id="ARAH_UTARA")

            self.add_label(layout, f"SKALA 1 : {skala:,}".replace(",", "."), panel_x + 65, 120.0, 150.0, 10.0, size=22, bold=True, h_align=Qt.AlignLeft, item_id="SKALA_ANGKA")

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
            scale_bar.attemptMove(self.mm_point(panel_x + 65 + getattr(self, 'dx', 0), 135.0 + getattr(self, 'dy', 0)))
            scale_bar.attemptResize(self.mm_size(160.0, 20.0))
            try:
                scale_bar.update()
            except Exception:
                pass

            self.add_line(layout, panel_x, 170.0, panel_x + panel_w, 170.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_1")

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

            inset_extent = QgsRectangle(ext)
            try:
                inset_extent.scale(4.0)
                cx = inset_extent.center().x()
                cy = inset_extent.center().y()
                side = max(inset_extent.width(), inset_extent.height())
                inset1.setExtent(QgsRectangle(cx - side/2.0, cy - side/2.0, cx + side/2.0, cy + side/2.0))
                inset1.attemptResize(self.mm_size(100.0, 100.0))
                inset1.setScale(1500000)
                
                from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem
                crsSrc = self.project.crs()
                crsDest = QgsCoordinateReferenceSystem("EPSG:4326")
                transform = QgsCoordinateTransform(crsSrc, crsDest, self.project)
                inset2.setCrs(crsDest)
                inset2.attemptResize(self.mm_size(100.0, 100.0))
                
                if config.get("grid_simetris", True):
                    main_ext_wgs = transform.transformBoundingBox(main_map.extent())
                    w = main_ext_wgs.width()
                    h = main_ext_wgs.height()
                    inset2.zoomToExtent(QgsRectangle(main_ext_wgs.xMinimum() - w, main_ext_wgs.yMinimum() - h, main_ext_wgs.xMaximum() + w, main_ext_wgs.yMaximum() + h))
                else:
                    import math
                    center_wgs = transform.transform(main_map.extent().center())
                    cx_wgs, cy_wgs = center_wgs.x(), center_wgs.y()
                    grid_interval = 1.0 / 60.0
                    box_cx = math.floor(cx_wgs / grid_interval) * grid_interval + (grid_interval / 2.0)
                    box_cy = math.floor(cy_wgs / grid_interval) * grid_interval + (grid_interval / 2.0)
                    half_span = 1.5 * grid_interval
                    inset2.zoomToExtent(QgsRectangle(box_cx - half_span, box_cy - half_span, box_cx + half_span, box_cy + half_span))
                
                self.setup_inset1_grid(inset1)
                self.setup_inset2_grid(inset2, main_map, config)
            except Exception:
                pass

            self.add_label(layout, "Proyeksi\\nSistem Grid\\nDatum Horizontal", panel_x + 10, 305.0, 70.0, 20.0, size=12, h_align=Qt.AlignLeft, item_id="TXT_SRS_LEFT")
            self.add_label(layout, ":  Universal Transverse Mercator (UTM)\\n:  Grid Geografi dan Grid UTM\\n:  SRGI 2013 / WGS 1984", panel_x + 85, 305.0, 160.0, 20.0, size=12, h_align=Qt.AlignLeft, item_id="TXT_SRS_RIGHT")
            self.add_line(layout, panel_x, 335.0, panel_x + panel_w, 335.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_2")

            logo_path = config.get("logo_path", "").strip()
            if not logo_path or not os.path.isfile(logo_path):
                logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo-ahza.png")
            if os.path.isfile(logo_path):
                self.add_picture(layout, logo_path, panel_x + 15, 345.0, 25.0, 25.0, item_id="PIC_LOGO_PEMDA")
            
            desa = config.get('nama_desa', '').strip() or "(NAMA DESA)"
            kecamatan = config.get('nama_kecamatan', '').strip() or "(NAMA KECAMATAN)"
            kabupaten = config.get('nama_kabupaten', '').strip() or "(NAMA KABUPATEN)"
            provinsi = config.get('nama_provinsi', '').strip() or "(NAMA PROVINSI)"
            kodepos = config.get('kode_pos', '').strip()
            tahun = config.get('tahun_peta', '2026').strip()
            kodepos_str = f" {kodepos}" if kodepos else ""
            penerbit_txt = f"DICETAK DAN DITERBITKAN OLEH:\\nPEMERINTAH DESA {desa.upper()} TAHUN {tahun}\\nKECAMATAN {kecamatan.upper()}\\nKABUPATEN {kabupaten.upper()}{kodepos_str} - PROVINSI {provinsi.upper()}"
            self.add_label(layout, penerbit_txt, panel_x + 45, 345.0, 200.0, 30.0, size=12, h_align=Qt.AlignLeft, item_id="TXT_PENERBIT")
            
            self.add_line(layout, panel_x, 385.0, panel_x + panel_w, 385.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_3")

            legend = QgsLayoutItemLegend(layout)
            legend.setId("LEGENDA")
            legend.setTitle("KETERANGAN")
            legend.setLinkedMap(main_map)
            legend.setFrameEnabled(False)
            legend.setBackgroundEnabled(False)
            legend.setAutoUpdateModel(False)
            try:
                model = legend.model()
                rootGroup = model.rootGroup()
                nodes_to_remove = []
                for layer_node in rootGroup.findLayers():
                    lyr_name = layer_node.layerName().lower()
                    if any(kw in lyr_name for kw in ['google', 'satellite', 'osm', 'bing', 'tile', 'basemap', 'hybrid', 'terrain']):
                        nodes_to_remove.append(layer_node)
                    else:
                        layer_node.setCustomProperty("legend/title-label", " ")
                for node in nodes_to_remove:
                    rootGroup.removeChildNode(node)
                legend.setColumnCount(2)
                legend.setSplitLayer(True)
                legend.setEqualColumnWidth(False)
            except Exception as e:
                pass

            layout.addLayoutItem(legend)
            legend.attemptMove(self.mm_point(panel_x + 5 + getattr(self, 'dx', 0), 395.0 + getattr(self, 'dy', 0)))
            legend.attemptResize(self.mm_size(250.0, 250.0))
            
            try:
                legend.setTitleFont(QFont("Arial", 16, QFont.Bold))
                legend.setStyleFont(legend.Title, QFont("Arial", 16, QFont.Bold))
                legend.setStyleFont(legend.GroupTitle, QFont("Arial", 12, QFont.Bold))
                legend.setStyleFont(legend.SubgroupTitle, QFont("Arial", 12, QFont.Bold))
                legend.setStyleFont(legend.SymbolLabel, QFont("Arial", 10))
            except Exception:
                pass

            self.add_line(layout, panel_x, 650.0, panel_x + panel_w, 650.0, stroke_width=1.5, stroke_color="0,169,230,255", item_id="LINE_DIV_4")

            sumber_custom = config.get("sumber_data", "").strip()
            if not sumber_custom:
                sumber_custom = ":  1. Peta Rupa Bumi Indonesia (RBI) Tematik 1:25.000\\n   2. Citra Satelit Resolusi Tinggi (CSRT) BIG\\n   3. Batas Desa Delimitasi PerKa BIG 3/2016\\n   4. DEMNAS Badan Informasi Geospasial"
            self.add_label(layout, "Sumber Data dan Riwayat Peta", panel_x + 5, 655.0, 70.0, 30.0, size=12, h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_HEADER")
            self.add_label(layout, sumber_custom, panel_x + 75, 655.0, 175.0, 30.0, size=12, h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_SUMBER_ISI")

            catatan_isi = ": Batas peta tidak dapat dijadikan acuan hukum\\n  sebenarnya di lapangan."
            self.add_label(layout, "Catatan", panel_x + 5, 690.0, 70.0, 15.0, size=12, h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_HEADER")
            self.add_label(layout, catatan_isi, panel_x + 75, 690.0, 175.0, 15.0, size=12, h_align=Qt.AlignLeft, v_align=Qt.AlignTop, item_id="TXT_CATATAN_ISI")

            pengesahan_txt = f"Disahkan oleh:\\n{config.get('jabatan_pengesah', 'Kepala Desa')} {config['nama_desa'].upper()}\\n\\n\\n\\n\\n\\n({config.get('nama_pengesah', '[NAMA KEPALA DESA]')})"
            self.add_label(layout, pengesahan_txt, panel_x + 10, 710.0, 240.0, 45.0, size=12, bold=True, h_align=Qt.AlignCenter, v_align=Qt.AlignVCenter, item_id="TXT_PENGESAHAN_FOOTER")

        else:
""" + "\n".join(["    " + line for line in old_target.split("\n")])

new_code = code.replace(old_target, new_target)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_code)
