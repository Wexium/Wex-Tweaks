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
        self.create_service_button.setText(self.tr("Create New Service"))
        self.delete_service_button.setText(self.tr("Delete Selected Service"))

    def run_command(self, command):
        """
        Run a command with polkit for administrative privileges
        """
        try:
            command = f'pkexec {command}'
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            error_message = f"An error occurred: {e.stderr.decode('utf-8')}"
            QMessageBox.critical(self, "Error", error_message)
            return error_message

    def update_mirrorlist(self):
        result = self.run_command("reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist")
        self.repo_label.setText(result or "Mirrorlist updated successfully")

    def update_system(self):
        result = self.run_command("pacman -Syu")
        self.repo_label.setText(result or "System updated successfully")

    def install_package(self):
        package_name, ok = QInputDialog.getText(self, self.tr("Install Package"), self.tr("Enter the package name:"))
        if ok and package_name:
            result = self.run_command(f"pacman -S {package_name}")
            self.repo_label.setText(result or f"{package_name} installed successfully")

    def install_aur_helpers(self):
        selected_helpers = [item.text() for item in self.aur_helpers_list.selectedItems()]
        if not selected_helpers:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No AUR helper selected"))
            return
        for helper in selected_helpers:
            result = self.run_command(f"pacman -S {helper}")
            self.aur_helpers_label.setText(result or f"{helper} installed successfully")

    def install_selected_programs(self):
        selected_programs = [item.text().lower() for item in self.popular_programs_list.selectedItems()]
        if not selected_programs:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No program selected"))
            return
        for program in selected_programs:
            package_name = {
                "steam": "steam",
                "proton": "proton-ge-custom-bin",
                "discord": "discord",
                "visual studio code": "visual-studio-code-bin",
                "gimp": "gimp",
                "blender": "blender",
                "lutris": "lutris",
                "obs studio": "obs-studio",
                "krita": "krita",
                # Add more mappings as required
            }.get(program, program)
            result = self.run_command(f"pacman -S {package_name}")
            self.popular_programs_label.setText(result or f"{program} installed successfully")

    def refresh_services_list(self):
        self.services_list.clear()
        services = self.get_services()
        for service in services:
            QListWidgetItem(service, self.services_list)

    def get_services(self):
        """
        Get the list of all systemd services
        """
        result = self.run_command("systemctl list-units --type=service --all --no-pager")
        services = []
        for line in result.split("\n"):
            if ".service" in line:
                service_name = line.split()[0]
                services.append(service_name)
        return services

    def manage_service(self, action):
        selected_items = self.services_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No service selected"))
            return
        service = selected_items[0].text()
        result = self.run_command(f'systemctl {action} {service}')
        self.services_label.setText(result or f"{service} {action}ed successfully")
        self.refresh_services_list()

    def start_service(self):
        self.manage_service('start')

    def stop_service(self):
        self.manage_service('stop')

    def restart_service(self):
        self.manage_service('restart')

    def enable_service(self):
        self.manage_service('enable')

    def disable_service(self):
        self.manage_service('disable')

    def create_service(self):
        service_name, ok = QInputDialog.getText(self, self.tr("Create Service"), self.tr("Enter the service name:"))
        if ok and service_name:
            service_content, ok2 = QInputDialog.getMultiLineText(self, self.tr("Create Service"), self.tr("Enter the service configuration:"))
            if ok2 and service_content:
                with open(f"/etc/systemd/system/{service_name}.service", "w") as f:
                    f.write(service_content)
                result = self.run_command(f"systemctl daemon-reload && systemctl enable {service_name}")
                self.services_label.setText(result or f"{service_name} created and enabled successfully")
                self.refresh_services_list()

    def delete_service(self):
        selected_items = self.services_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No service selected"))
            return
        service = selected_items[0].text()
        result = self.run_command(f'systemctl disable {service} && rm /etc/systemd/system/{service}')
        self.services_label.setText(result or f"{service} deleted successfully")
        self.refresh_services_list()

    def load_settings(self):
        repo = self.settings.value("repository", "core")
        self.repo_combobox.setCurrentText(repo)
        chaotic_aur = self.settings.value("chaotic_aur", False, type=bool)
        self.chaotic_aur_checkbox.setChecked(chaotic_aur)

    def closeEvent(self, event):
        self.settings.setValue("repository", self.repo_combobox.currentText())
        self.settings.setValue("chaotic_aur", self.chaotic_aur_checkbox.isChecked())
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load the default language based on the locale
    translator = QTranslator()
    locale = QLocale.system().name()
    
    if "ru" in locale:
        translator.load("wex_tweaks_ru.qm")
    else:
        translator.load("wex_tweaks_en.qm")
        
    app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())