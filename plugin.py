# -*- coding: utf-8 -*-
"""
MAIN PLUGIN LOGIC – QGIS 3.x (PERKABIG NO. 3 TAHUN 2016)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
"""

import os
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from qgis.PyQt.QtWidgets import (QAction, QMessageBox, QDialog, QVBoxLayout, 
                                 QHBoxLayout, QLabel, QPushButton)

from .peta_desa_dialog import PetaDesaDialog
from .core.layout_generator import PetaDesaLayoutGenerator

class AboutDialog(QDialog):
    def __init__(self, parent=None, plugin_dir=""):
        super().__init__(parent)
        self.setWindowTitle("Tentang Template Peta Desa")
        self.setFixedSize(550, 250)
        self.setWindowIcon(QIcon(os.path.join(plugin_dir, 'icon.png')))
        self.setStyleSheet("QDialog { background-color: #f8f9fa; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(plugin_dir, 'icon.png'))
        logo_label.setPixmap(logo_pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignTop)
        
        info_layout = QVBoxLayout()
        
        title = QLabel("Template Peta Desa PerKa BIG 3/2016")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #2c3e50;")
        
        desc = QLabel(
            "Plugin QGIS resmi untuk otomatisasi pembuatan layout Peta Desa "
            "berdasarkan standar Badan Informasi Geospasial (BIG).<br><br>"
            "Dirancang khusus untuk menghadirkan kualitas kartografi profesional "
            "secara cepat, presisi, dan <i>Zero Topology Errors!</i>"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #34495e; font-size: 13px; line-height: 1.4;")
        
        dev_info = QLabel(
            "<b>Pengembang:</b> Ahza Studio (CAT Spatial Specialist)<br>"
            "<b>Versi:</b> 1.0.7<br>"
            "<b>Kontak:</b> admin@ahzastudio.web.id"
        )
        dev_info.setStyleSheet("color: #2c3e50; font-size: 13px;")
        
        btn_close = QPushButton("Tutup")
        btn_close.setFixedWidth(100)
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; border-radius: 4px; padding: 7px; font-weight: bold; }"
            "QPushButton:hover { background-color: #2ecc71; }"
        )
        btn_close.clicked.connect(self.accept)
        
        info_layout.addWidget(title)
        info_layout.addWidget(desc)
        info_layout.addWidget(dev_info)
        info_layout.addSpacing(10)
        info_layout.addWidget(btn_close, alignment=Qt.AlignRight)
        
        layout.addWidget(logo_label)
        layout.addSpacing(20)
        layout.addLayout(info_layout)

class PetaDesaPlugin:
    """Plugin QGIS resmi Template Peta Desa PerKa BIG 3/2016."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = '&Template Peta Desa PerKa BIG'
        self.dialog = None

    def tr(self, message):
        return QCoreApplication.translate('PetaDesaPlugin', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        action = QAction(icon, text, parent or self.iface.mainWindow())
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip:
            action.setStatusTip(status_tip)
        if whats_this:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addVectorToolBarIcon(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Membuat action menu dan tombol toolbar di QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr('Buat Template Peta Desa PerKa BIG'),
            callback=self.run,
            parent=self.iface.mainWindow()
        )
        self.add_action(
            icon_path,
            text=self.tr('Tentang Plugin'),
            callback=self.show_about,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False
        )

        # Set icon for the main menu folder dynamically
        for action in self.iface.pluginMenu().actions():
            if action.menu() and action.text().replace('&', '') == 'Template Peta Desa PerKa BIG':
                action.setIcon(QIcon(icon_path))
                break
    def unload(self):
        """Removes plugin menu and toolbar icons upon unload."""
        for action in self.actions:
            self.iface.removePluginMenu('&Template Peta Desa PerKa BIG', action)
            self.iface.removeVectorToolBarIcon(action)

    def show_about(self):
        """Menampilkan kotak dialog Tentang Plugin custom."""
        dlg = AboutDialog(self.iface.mainWindow(), self.plugin_dir)
        dlg.exec_()

    def run(self):
        """Memunculkan dialog wizard dan mengeksekusi pembuatan layout."""
        if not self.dialog:
            self.dialog = PetaDesaDialog(self.iface.mainWindow())

        result = self.dialog.exec_()
        if result:
            config = self.dialog.get_config()
            try:
                generator = PetaDesaLayoutGenerator(iface=self.iface)
                layout = generator.generate_layout(config)
                QMessageBox.information(
                    self.iface.mainWindow(),
                    "Berhasil!",
                    f"Layout Peta Desa PerKa BIG 3/2016 ({config['jenis_peta']}) untuk "
                    f"Desa {config['nama_desa']} berhasil dibuat di Layout Manager!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self.iface.mainWindow(),
                    "Error!",
                    f"Gagal membuat layout Peta Desa: {str(e)}"
                )
