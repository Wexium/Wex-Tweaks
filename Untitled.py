import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QLabel, QComboBox, QCheckBox, QMessageBox, QInputDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QSettings, QTranslator, QLocale


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = QTranslator()
        self.current_language = "en"

        self.setWindowTitle("Wex Tweaks")
        self.setGeometry(100, 100, 800, 600)

        # Language selector
        self.language_selector = QComboBox(self)
        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("Русский", "ru")
        self.language_selector.currentIndexChanged.connect(self.switch_language)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.language_selector)

        # Welcome message
        self.welcome_label = QLabel(self.tr("Welcome to Wex Tweaks"), self)
        main_layout.addWidget(self.welcome_label)

        # Add repository selection
        self.repo_label = QLabel(self.tr("Select Repository:"), self)
        main_layout.addWidget(self.repo_label)

        self.repo_combobox = QComboBox(self)
        self.repo_combobox.addItems(["core", "extra", "community", "multilib", "chaotic-aur"])
        main_layout.addWidget(self.repo_combobox)

        # Add chaotic aur checkbox
        self.chaotic_aur_checkbox = QCheckBox(self.tr("Enable Chaotic AUR"), self)
        main_layout.addWidget(self.chaotic_aur_checkbox)

        # Update Mirrorlist button
        self.update_mirrorlist_button = QPushButton(self.tr("Update Mirrorlist"), self)
        self.update_mirrorlist_button.clicked.connect(self.update_mirrorlist)
        main_layout.addWidget(self.update_mirrorlist_button)

        # Update System button
        self.update_system_button = QPushButton(self.tr("Update System"), self)
        self.update_system_button.clicked.connect(self.update_system)
        main_layout.addWidget(self.update_system_button)

        # Install package button
        self.install_package_button = QPushButton(self.tr("Install Package"), self)
        self.install_package_button.clicked.connect(self.install_package)
        main_layout.addWidget(self.install_package_button)

        # AUR helpers
        self.aur_helpers_label = QLabel(self.tr("Install AUR Helpers:"), self)
        main_layout.addWidget(self.aur_helpers_label)

        self.aur_helpers_list = QListWidget(self)
        self.aur_helpers_list.addItems(["yay", "paru", "trizen", "pamac-aur", "auracle-git"])
        self.aur_helpers_list.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(self.aur_helpers_list)

        self.install_aur_helper_button = QPushButton(self.tr("Install Selected AUR Helpers"), self)
        self.install_aur_helper_button.clicked.connect(self.install_aur_helpers)
        main_layout.addWidget(self.install_aur_helper_button)

        # Popular programs installation
        self.popular_programs_label = QLabel(self.tr("Install Popular Programs:"), self)
        main_layout.addWidget(self.popular_programs_label)

        # Adding popular programs and games
        self.popular_programs_list = QListWidget(self)
        self.popular_programs_list.addItems([
            "Steam", "Proton", "Discord", "Visual Studio Code", "GIMP", "Blender", "Lutris",
            "OBS Studio", "Krita", "Godot", "UnityHub", "Unreal Engine", "Battle.net",
            "Heroic Games Launcher", "Wine", "Vulkan-tools", "DXVK", "Epic Games Launcher",
            "Twitch", "RetroArch", "PCSX2", "PPSSPP", "Dolphin Emulator", "yuzu", "RPCS3",
            "Cemu", "PlayOnLinux", "q4wine", "Teamspeak", "Mumble", "Skype", "Zoom", "Slack",
            "Telegram", "VLC", "Kodi", "HandBrake", "Kdenlive", "Audacity", "Spotify", "mpv",
            "SMPlayer", "MakeMKV", "JDownloader2", "Stremio", "qBittorrent", "Deluge", "Transmission",
            "FileZilla", "GParted", "BleachBit", "VirtualBox", "VMware Workstation", "qemu",
            "gnome-boxes", "NoMachine", "Remmina", "VNC Viewer", "ethtool", "iperf", "Wireshark",
            "nmap", "Inkscape", "Darktable", "RawTherapee", "MyPaint", "Pencil2D", "Synfig Studio",
            "Tux Paint", "Tux Typing", "LibreOffice", "FreeOffice", "OnlyOffice", "WPS Office",
            "Atom", "Sublime Text", "Brackets", "Clion", "PyCharm", "Geany", "Bluefish",
            "NetBeans", "Eclipse", "IntelliJ IDEA", "Android Studio", "GitKraken", "SmartGit",
            "SourceTree", "Fork"
        ])
        self.popular_programs_list.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(self.popular_programs_list)

        self.install_selected_program_button = QPushButton(self.tr("Install Selected Programs"), self)
        self.install_selected_program_button.clicked.connect(self.install_selected_programs)
        main_layout.addWidget(self.install_selected_program_button)

        # Systemd services management layout
        systemd_layout = QHBoxLayout()

        self.services_label = QLabel(self.tr("Manage Systemd Services:"), self)
        main_layout.addWidget(self.services_label)

        self.services_list = QListWidget(self)
        systemd_layout.addWidget(self.services_list)
        self.refresh_services_list()

        systemd_buttons_layout = QVBoxLayout()

        self.start_service_button = QPushButton(self.tr("Start Selected Service"), self)
        self.start_service_button.clicked.connect(self.start_service)
        systemd_buttons_layout.addWidget(self.start_service_button)

        self.stop_service_button = QPushButton(self.tr("Stop Selected Service"), self)
        self.stop_service_button.clicked.connect(self.stop_service)
        systemd_buttons_layout.addWidget(self.stop_service_button)

        self.restart_service_button = QPushButton(self.tr("Restart Selected Service"), self)
        self.restart_service_button.clicked.connect(self.restart_service)
        systemd_buttons_layout.addWidget(self.restart_service_button)

        self.enable_service_button = QPushButton(self.tr("Enable Selected Service"), self)
        self.enable_service_button.clicked.connect(self.enable_service)
        systemd_buttons_layout.addWidget(self.enable_service_button)

        self.disable_service_button = QPushButton(self.tr("Disable Selected Service"), self)
        self.disable_service_button.clicked.connect(self.disable_service)
        systemd_buttons_layout.addWidget(self.disable_service_button)

        self.create_service_button = QPushButton(self.tr("Create New Service"), self)
        self.create_service_button.clicked.connect(self.create_service)
        systemd_buttons_layout.addWidget(self.create_service_button)

        self.delete_service_button = QPushButton(self.tr("Delete Selected Service"), self)
        self.delete_service_button.clicked.connect(self.delete_service)
        systemd_buttons_layout.addWidget(self.delete_service_button)

        systemd_layout.addLayout(systemd_buttons_layout)
        main_layout.addLayout(systemd_layout)

        # Layout setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load settings
        self.settings = QSettings("WexTweaks", "AppSettings")
        self.load_settings()

    def switch_language(self, index):
        language = self.language_selector.itemData(index)
        if language == self.current_language:
            return

        if language == "ru":
            self.translator.load("wex_tweaks_ru.qm")
            self.current_language = "ru"
        else:
            self.translator.load("wex_tweaks_en.qm")
            self.current_language = "en"

        QApplication.instance().installTranslator(self.translator)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Wex Tweaks"))
        self.welcome_label.setText(self.tr("Welcome to Wex Tweaks"))
        self.repo_label.setText(self.tr("Select Repository:"))
        self.chaotic_aur_checkbox.setText(self.tr("Enable Chaotic AUR"))
        self.update_mirrorlist_button.setText(self.tr("Update Mirrorlist"))
        self.update_system_button.setText(self.tr("Update System"))
        self.install_package_button.setText(self.tr("Install Package"))
        self.aur_helpers_label.setText(self.tr("Install AUR Helpers:"))
        self.install_aur_helper_button.setText(self.tr("Install Selected AUR Helpers"))
        self.popular_programs_label.setText(self.tr("Install Popular Programs:"))
        self.install_selected_program_button.setText(self.tr("Install Selected Programs"))
        self.services_label.setText(self.tr("Manage Systemd Services:"))
        self.start_service_button.setText(self.tr("Start Selected Service"))
        self.stop_service_button.setText(self.tr("Stop Selected Service"))
        self.restart_service_button.setText(self.tr("Restart Selected Service"))
        self.enable_service_button.setText(self.tr("Enable Selected Service"))
        self.disable_service_button.setText(self.tr("Disable Selected Service"))
        self.create_service_button.setText(self.tr("Create New Service"))
        self.delete_service_button.setText(self.tr("Delete Selected Service"))

    def load_settings(self):
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", self.size()))
        self.move(self.settings.value("pos", self.pos()))
        self.settings.endGroup()

    def closeEvent(self, event):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

    def update_mirrorlist(self):
        try:
            subprocess.run(["sudo", "reflector", "--verbose", "--latest", "5", "--sort", "rate", "--save", "/etc/pacman.d/mirrorlist"], check=True)
            QMessageBox.information(self, "Success", "Mirrorlist updated successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to update mirrorlist")

    def update_system(self):
        try:
            subprocess.run(["sudo", "pacman", "-Syu"], check=True)
            QMessageBox.information(self, "Success", "System updated successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to update system")

    def install_package(self):
        package, ok = QInputDialog.getText(self, "Install Package", "Enter package name:")
        if ok and package:
            try:
                subprocess.run(["yay", "-S", package], check=True)
                QMessageBox.information(self, "Success", f"Package '{package}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install package '{package}'")


    def install_aur_helpers(self):
        selected_helpers = [item.text() for item in self.aur_helpers_list.selectedItems()]
        for helper in selected_helpers:
            try:
                subprocess.run(["git", "clone", f"https://aur.archlinux.org/{helper}.git"], check=True)
                subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=f"./{helper}", check=True)
                QMessageBox.information(self, "Success", f"AUR helper '{helper}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install AUR helper '{helper}'")

    def install_selected_programs(self):
        selected_programs = [item.text() for item in self.popular_programs_list.selectedItems()]
        for program in selected_programs:
            try:
                subprocess.run(["sudo", "pacman", "-S", program.lower().replace(" ", "-")], check=True)
                QMessageBox.information(self, "Success", f"Program '{program}' installed successfully")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to install program '{program}'")

    def refresh_services_list(self):
        self.services_list.clear()
        try:
            result = subprocess.run(["systemctl", "list-unit-files", "--type=service", "--state=enabled,disabled"], capture_output=True, text=True, check=True)
            for line in result.stdout.split("\n")[1:]:
                if line:
                    service_name = line.split()[0]
                    item = QListWidgetItem(service_name)
                    self.services_list.addItem(item)
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to retrieve services list")

    def start_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "start", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' started successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to start service '{service}'")

    def stop_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "stop", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' stopped successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to stop service '{service}'")

    def restart_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "restart", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' restarted successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to restart service '{service}'")

    def enable_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "enable", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' enabled successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to enable service '{service}'")

    def disable_service(self):
        service = self.services_list.currentItem().text()
        try:
            subprocess.run(["sudo", "systemctl", "disable", service], check=True)
            QMessageBox.information(self, "Success", f"Service '{service}' disabled successfully")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"Failed to disable service '{service}'")

    def create_service(self):
        service_name, ok = QInputDialog.getText(self, "Create New Service", "Enter service name (e.g., my_service):")
        if ok and service_name:
            service_content, ok = QInputDialog.getMultiLineText(self, "Create New Service", "Enter service file content:", 
            "[Unit]\nDescription=My custom service\n\n[Service]\nExecStart=/path/to/executable\n\n[Install]\nWantedBy=multi-user.target")
        if ok and service_content:
            service_path = f"/etc/systemd/system/{service_name}.service"
            try:
                with open(service_path, "w") as service_file:
                    service_file.write(service_content)
                subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
                self.refresh_services_list()
                QMessageBox.information(self, "Success", f"Service '{service_name}' created successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create service '{service_name}': {e}")


    def delete_service(self):
        service = self.services_list.currentItem().text()
        confirm = QMessageBox.question(self, "Delete Service", f"Are you sure you want to delete the service '{service}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                subprocess.run(["sudo", "systemctl", "disable", service], check=True)
                subprocess.run(["sudo", "rm", f"/etc/systemd/system/{service}"], check=True)
                QMessageBox.information(self, "Success", f"Service '{service}' deleted successfully")
                self.refresh_services_list()
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Error", f"Failed to delete service '{service}'")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
