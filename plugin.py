# -*- coding: utf-8 -*-
"""
MAIN PLUGIN LOGIC – QGIS 3.x (PERKABIG NO. 3 TAHUN 2016)
----------------------------------------------------------------------
Pengembang: CAT Spatial Specialist
"""

import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from .peta_desa_dialog import PetaDesaDialog
from .core.layout_generator import PetaDesaLayoutGenerator

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

    def unload(self):
        """Removes plugin menu and toolbar icons upon unload."""
        for action in self.actions:
            self.iface.removePluginMenu('&Template Peta Desa PerKa BIG', action)
            self.iface.removeVectorToolBarIcon(action)

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
