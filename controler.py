import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from MainWindow import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtPrintSupport import *
import os
import importlib.util
import json
import socket
import subprocess
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


APP_ID = "portable.learning.environment"


def configure_windows_taskbar_icon():
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except Exception:
        pass


class Controller:
    def __init__(self):
        configure_windows_taskbar_icon()
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Portable Learning Environment")
        self.app.setOrganizationName("Portable Learning Environment")
        self.app.setWindowIcon(QtGui.QIcon(asset_path("ico.png")))
        self.MainWindow = QtWidgets.QMainWindow()
        self.main = Main()
        self.main.shutdown_callback = self.shutdown_jupyter
        self.local_jupyter_port = None
        self.jupyter_url = os.environ.get("PLE_JUPYTER_URL", "http://localhost:8899/tree?")
        self.jupyter_process = None
        self.repo_url = None
        self.dirName = None
        self.current_assignment_path = None
        self.assignment_status = {
            "cloned": False,
            "opened": False,
            "submitted": False,
            "pushed": False,
        }
        self.connect_event()

    def exec(self):
        self.main.show()
        return self.app.exec()

    def start_local_jupyter(self):
        if not self.jupyter_url.startswith("http://localhost:"):
            return
        if self.jupyter_process and self.jupyter_process.poll() is None:
            return
        self.local_jupyter_port = self.find_free_port(8899)
        self.jupyter_url = f"http://localhost:{self.local_jupyter_port}/tree?"
        try:
            self.jupyter_process = subprocess.Popen(
                [
                    "jupyter",
                    "notebook",
                    "--no-browser",
                    "--ServerApp.open_browser=False",
                    "--NotebookApp.open_browser=False",
                    f"--port={self.local_jupyter_port}",
                    f"--notebook-dir={Path.home()}",
                    "--IdentityProvider.token=",
                    "--ServerApp.token=",
                    "--ServerApp.password=",
                    "--NotebookApp.token=",
                    "--NotebookApp.password=",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.main.statusBar().showMessage("Starting Jupyter in the app...")
        except FileNotFoundError:
            self.main.statusBar().showMessage("Jupyter command not found")

    def find_free_port(self, preferred_port):
        for port in range(preferred_port, preferred_port + 100):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.2)
                if sock.connect_ex(("127.0.0.1", port)) != 0:
                    return port
        return preferred_port

    def local_tree_url(self, assignment_path=None):
        parsed = urlparse(self.jupyter_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if assignment_path is None:
            return f"{base}/tree?"
        return f"{base}/tree/" + quote(Path(assignment_path).resolve().as_posix())

    def shutdown_jupyter(self):
        if self.jupyter_process and self.jupyter_process.poll() is None:
            self.jupyter_process.terminate()

    def connect_event(self):
        self.main.reload.triggered.connect(self.reload)
        self.main.back.triggered.connect(self.back)
        self.main.forward.triggered.connect(self.forward)
        self.main.plus.triggered.connect(self.plus_home)
        self.main.home.triggered.connect(self.main.navigate_home)
        self.main.pushButton.clicked.connect(self.open_jupyter)
        self.main.startLessonButton.clicked.connect(self.start_lesson)
        self.main.preflightButton.clicked.connect(self.run_preflight_check)
        self.main.stuckHelpButton.clicked.connect(self.open_stuck_help)
        self.main.actionOpen.triggered.connect(self.open_file)
        self.main.actionexit.triggered.connect(self.exit)
        self.main.actionHelp.triggered.connect(self.open_help)
        self.main.actionStuckHelp.triggered.connect(self.open_stuck_help)
        self.main.actionAbout_Us.triggered.connect(self.about_us)
        self.main.actionHelpJup.triggered.connect(self.jupyter_help)
        self.main.actionPush_To_Github.triggered.connect(self.push_to_github)
        self.main.actionClone_from_Github.triggered.connect(self.clone_from_github)

        # self.main.pushButton_2.clicked.connect(self.open_github)
        # self.main.pushButton_3.clicked.connect(self.plus_home)
        # self.main.pushButton_4.clicked.connect(self.open_github_classroom)
        self.main.jupyter.triggered.connect(self.open_jupyter)
        self.main.github.triggered.connect(self.open_github)
        self.main.github_class.triggered.connect(self.open_github_classroom)
        self.main.actionCreate_2.triggered.connect(self.clone_from_github)
        self.main.actionUpdate_2.triggered.connect(self.push_to_github)
        self.main.actionPreflight.triggered.connect(self.run_preflight_check)
        self.main.actionStartLesson.triggered.connect(self.start_lesson)
        self.main.actionInfo.triggered.connect(self.info)
        self.main.actionExport.triggered.connect(self.export)

    def set_assignment_status(self, key, value=True, detail=None):
        self.assignment_status[key] = value
        self.main.set_assignment_status(self.assignment_status, detail)
        if detail:
            self.main.statusBar().showMessage(detail)

    def check_command(self, command, success_text):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=8,
            )
        except FileNotFoundError:
            return ("Fail", "Command not found", f"Install {command[0]} and make sure it is on PATH.")
        except subprocess.TimeoutExpired:
            return ("Warn", "Command timed out", "Try running the command manually from a terminal.")
        if result.returncode == 0:
            detail = (result.stdout or result.stderr or success_text).strip().splitlines()
            return ("Pass", detail[0] if detail else success_text, "")
        detail = (result.stderr or result.stdout or "Command failed").strip()
        return ("Fail", detail, f"Fix {command[0]} before class starts.")

    def package_check(self, package_name, import_name=None):
        import_name = import_name or package_name
        if importlib.util.find_spec(import_name) is None:
            return ("Fail", f"{package_name} is not importable", f"Install requirements or add {package_name}.")
        return ("Pass", f"{package_name} is available", "")

    def run_preflight_check(self):
        preferences = self.main.lesson_preferences()
        checks = [
            ("Python", *self.check_command([sys.executable, "--version"], "Python is available")),
            ("Git", *self.check_command(["git", "--version"], "Git is available")),
            ("Jupyter", *self.check_command(["jupyter", "--version"], "Jupyter is available")),
            ("Git user.name", *self.git_config_check("user.name")),
            ("Git user.email", *self.git_config_check("user.email")),
        ]

        package_map = [
            ("NumPy", "numpy"),
            ("Pandas", "pandas"),
            ("Matplotlib", "matplotlib"),
            ("OpenCV", "cv2"),
            ("scikit-learn", "sklearn"),
        ]
        if preferences["course"] == "AI / machine learning":
            package_map.append(("TensorFlow", "tensorflow"))
        for package_name, import_name in package_map:
            checks.append((package_name, *self.package_check(package_name, import_name)))

        if preferences["delivery"] == "Teacher controlled - JupyterHub":
            checks.append(("JupyterHub URL", *self.jupyterhub_url_check()))
        else:
            checks.append(("Local Jupyter port", "Pass", "A free local port will be selected starting at 8899.", ""))

        self.show_check_results("Pre-flight environment check", checks)

    def git_config_check(self, key):
        try:
            result = subprocess.run(
                ["git", "config", "--global", key],
                capture_output=True,
                text=True,
                check=False,
                timeout=8,
            )
        except FileNotFoundError:
            return ("Fail", "Git command not found", "Install Git and make sure it is on PATH.")
        value = result.stdout.strip()
        if value:
            return ("Pass", value, "")
        return ("Warn", f"{key} is not configured", f"Run: git config --global {key} \"your value\"")

    def jupyterhub_url_check(self):
        url = self.jupyter_url
        if not url.startswith(("http://", "https://")):
            return ("Warn", "No JupyterHub URL configured", "Set PLE_JUPYTER_URL or enter it during Start lesson.")
        if url.startswith("http://localhost:"):
            return ("Warn", "Dashboard still points to local Jupyter", "Enter the institution JupyterHub URL during Start lesson.")
        try:
            request = Request(url, headers={"User-Agent": "Portable Learning Environment"})
            with urlopen(request, timeout=6) as response:
                return ("Pass", f"Reachable: HTTP {response.status}", "")
        except Exception as error:
            return ("Warn", f"Could not verify URL: {error}", "Check network access or ask IT to confirm the hub URL.")

    def show_check_results(self, title, checks):
        dialog = QtWidgets.QDialog(self.main)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(760, 420)
        layout = QtWidgets.QVBoxLayout(dialog)

        summary = QtWidgets.QLabel(self.check_summary(checks))
        summary.setWordWrap(True)
        layout.addWidget(summary)

        table = QtWidgets.QTableWidget(len(checks), 4)
        table.setHorizontalHeaderLabels(["Check", "Status", "Result", "Fix / Next action"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setWordWrap(True)
        for row, (name, status, result, fix) in enumerate(checks):
            values = [name, status, result, fix]
            for column, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                if status == "Pass":
                    item.setBackground(QtGui.QColor("#e8f5ee"))
                elif status == "Warn":
                    item.setBackground(QtGui.QColor("#fff7df"))
                else:
                    item.setBackground(QtGui.QColor("#fdecec"))
                table.setItem(row, column, item)
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)

        close = QtWidgets.QPushButton("Close")
        close.clicked.connect(dialog.accept)
        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(close)
        layout.addLayout(button_row)
        dialog.exec()

    def check_summary(self, checks):
        fails = sum(1 for _, status, _, _ in checks if status == "Fail")
        warnings = sum(1 for _, status, _, _ in checks if status == "Warn")
        if fails:
            return f"{fails} required check(s) failed and {warnings} warning(s) need attention before class."
        if warnings:
            return f"Environment can start, but {warnings} warning(s) should be reviewed before class."
        return "All checks passed. The environment is ready for class."

    def assignment_folder_name(self, repo_url):
        name = repo_url.rstrip("/").rstrip(os.sep)
        name = os.path.basename(name)
        if name.endswith(".git"):
            name = name[:-4]
        return name

    def open_assignment_in_jupyter(self, assignment_path):
        self.current_assignment_path = str(Path(assignment_path).resolve())
        if self.jupyter_url.startswith("http://localhost:"):
            self.start_local_jupyter()
            folder_url = self.local_tree_url(self.current_assignment_path)
            self.main.add_new_tab(QtCore.QUrl(folder_url), "Assignment")
            self.main.urlbar.setText(folder_url)
        else:
            self.open_jupyter()
        self.set_assignment_status(
            "opened",
            True,
            f"Opened assignment folder: {self.current_assignment_path}",
        )

    def open_file(self):
        options = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        path = str(Path.home())
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main,
            "All files",
            path,
            "All Files (*);;Python Files (*.py);;Notebook Files (*.ipynb)",
            options=options,
        )
        if fileName:
            self.main.add_new_tab(QUrl.fromLocalFile(fileName))

    def info(self):
        QMessageBox.warning(self.main, 'Warning !!', "\nUnder Development !!")

    def export(self):
        QMessageBox.warning(self.main, 'Warning !!', "\nUnder Development !!")

    def start_lesson(self):
        dialog = QtWidgets.QDialog(self.main)
        dialog.setWindowTitle("Start lesson")
        dialog.setMinimumWidth(620)
        preferences = self.main.lesson_preferences()

        layout = QtWidgets.QVBoxLayout(dialog)
        intro = QtWidgets.QLabel(
            "Guide students through the class flow: start JupyterHub, clone the "
            "GitHub Classroom assignment, open the folder, and show a checklist."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        form = QtWidgets.QFormLayout()
        course_mode = QtWidgets.QComboBox()
        course_mode.addItems(
            [
                "General lecture",
                "Programming language",
                "Digital image processing",
                "AI / machine learning",
                "General lab",
            ]
        )
        course_mode.setCurrentText(preferences["course"])
        delivery_mode = QtWidgets.QComboBox()
        delivery_mode.addItems(
            [
                "Student practice - local Jupyter Notebook",
                "Teacher controlled - JupyterHub",
            ]
        )
        delivery_mode.setCurrentText(preferences["delivery"])
        repo_input = QtWidgets.QLineEdit()
        repo_input.setPlaceholderText("https://github.com/classroom-org/assignment-repo.git")
        folder_input = QtWidgets.QLineEdit(str(Path.home()))
        hub_input = QtWidgets.QLineEdit(self.jupyter_url)
        hub_input.setPlaceholderText("https://your-jupyterhub.example.edu/hub/login")
        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(
            lambda: self._select_dialog_folder(folder_input, "Select lesson folder")
        )

        folder_row = QtWidgets.QHBoxLayout()
        folder_row.addWidget(folder_input)
        folder_row.addWidget(browse)

        checklist = QtWidgets.QPlainTextEdit()
        checklist.setPlaceholderText("Add lesson goals, rubric items, or checkpoints.")
        checklist.setPlainText(self.lesson_template(course_mode.currentText()))
        checklist.setMinimumHeight(130)
        course_mode.currentTextChanged.connect(
            lambda value: checklist.setPlainText(self.lesson_template(value))
        )

        form.addRow("Course type", course_mode)
        form.addRow("Delivery", delivery_mode)
        form.addRow("JupyterHub URL", hub_input)
        form.addRow("Assignment URL", repo_input)
        form.addRow("Work folder", folder_row)
        form.addRow("Checklist", checklist)
        layout.addLayout(form)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Start")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        if delivery_mode.currentIndex() == 0:
            self.jupyter_url = "http://localhost:8899/tree?"
        else:
            self.jupyter_url = hub_input.text().strip() or self.jupyter_url

        repo_url = repo_input.text().strip()
        work_dir = Path(folder_input.text()).expanduser()
        if repo_url:
            assignment_path = self.clone_repository(repo_url, work_dir)
            if assignment_path is None:
                return
            self.open_assignment_in_jupyter(assignment_path)
        else:
            self.open_jupyter()

        self.show_lesson_checklist(checklist.toPlainText())

    def lesson_template(self, course_mode):
        templates = {
            "General lecture": (
                "1. State the learning objective in one sentence.\n"
                "2. Show one worked example.\n"
                "3. Ask students to predict the next result.\n"
                "4. Run a short practice task.\n"
                "5. Collect one reflection or exit-ticket answer."
            ),
            "Programming language": (
                "1. Open the starter notebook.\n"
                "2. Run setup cells from top to bottom.\n"
                "3. Complete syntax and variable exercises.\n"
                "4. Complete function or control-flow checkpoints.\n"
                "5. Explain one bug and how it was fixed.\n"
                "6. Save and upload the assignment."
            ),
            "Digital image processing": (
                "1. Load and display the sample image.\n"
                "2. Convert color spaces or grayscale.\n"
                "3. Apply enhancement, thresholding, filtering, or edge detection.\n"
                "4. Compare before and after results.\n"
                "5. Save output images and explain the parameter choices.\n"
                "6. Save and upload the assignment."
            ),
            "AI / machine learning": (
                "1. Load the dataset and inspect samples.\n"
                "2. Split data into training and testing sets.\n"
                "3. Train a baseline model.\n"
                "4. Evaluate accuracy, loss, or relevant metrics.\n"
                "5. Improve one model setting and explain the result.\n"
                "6. Save and upload the assignment."
            ),
            "General lab": (
                "1. Open the lab notebook or instructions.\n"
                "2. Run all setup checks.\n"
                "3. Complete each checkpoint in order.\n"
                "4. Save evidence of results.\n"
                "5. Submit work and confirm the pushed status."
            ),
        }
        return templates.get(course_mode, templates["General lecture"])

    def _select_dialog_folder(self, line_edit, title):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self.main,
            title,
            line_edit.text() or str(Path.home()),
            QtWidgets.QFileDialog.Option.ShowDirsOnly,
        )
        if folder:
            line_edit.setText(folder)

    def show_lesson_checklist(self, checklist_text):
        dialog = QtWidgets.QDialog(self.main)
        dialog.setWindowTitle("Lesson checklist")
        dialog.setMinimumWidth(520)
        layout = QtWidgets.QVBoxLayout(dialog)
        label = QtWidgets.QLabel(
            "Keep this checklist visible while students work. Mark the assignment "
            "submitted when students have saved and are ready to upload."
        )
        label.setWordWrap(True)
        layout.addWidget(label)

        checklist = QtWidgets.QPlainTextEdit()
        checklist.setPlainText(checklist_text.strip())
        checklist.setReadOnly(True)
        checklist.setMinimumHeight(180)
        layout.addWidget(checklist)

        submitted = QtWidgets.QPushButton("Mark submitted")
        submitted.clicked.connect(
            lambda: (
                self.set_assignment_status(
                    "submitted",
                    True,
                    "Assignment marked submitted. Use Upload assignment to push it to GitHub.",
                ),
                dialog.accept(),
            )
        )
        close = QtWidgets.QPushButton("Close")
        close.clicked.connect(dialog.accept)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(submitted)
        button_row.addWidget(close)
        layout.addLayout(button_row)
        dialog.exec()

    def open_folder(self):
        path = str(Path.home())
        self.dirName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', path,
                                                                  QtWidgets.QFileDialog.Option.ShowDirsOnly)
        if self.dirName:
            self.dir_select.setText(self.dirName)

    def push_to_github(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Upload repository to GitHub")
        self.dialog.setMinimumWidth(500)
        self.dialog.setFixedHeight(150)

        VLayout = QtWidgets.QVBoxLayout()
        Hlayout1 = QtWidgets.QHBoxLayout()
        Hlayout3 = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(self.dialog)
        label.setText(" WorkDir      : ")

        button = QtWidgets.QPushButton()
        button.setText("Open")
        button.setObjectName("button")
        button.clicked.connect(self.open_folder)

        self.dir_select = QtWidgets.QLineEdit()
        self.dir_select.setObjectName("dir_select")
        path = self.current_assignment_path or str(Path.home())
        self.dir_select.setText(path)

        add = QtWidgets.QPushButton()
        add.setObjectName("add_link")
        add.setText('Push')
        add.clicked.connect(self.push_submit)

        cancel = QtWidgets.QPushButton()
        cancel.setObjectName("cancel_link")
        cancel.setText('Cancel')
        cancel.clicked.connect(self.dialog.reject)

        Hlayout1.addWidget(label)
        Hlayout1.addWidget(self.dir_select)
        Hlayout1.addWidget(button)

        Hlayout3.addStretch()
        Hlayout3.addWidget(add, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        Hlayout3.addWidget(cancel, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        VLayout.addLayout(Hlayout1, 1)
        VLayout.addLayout(Hlayout3, 2)
        self.dialog.setLayout(VLayout)
        self.dialog.exec()

    def push_submit(self):
        self.dirName = self.dir_select.text()
        if not self.dirName:
            QMessageBox.warning(self.main, 'Warning !!', "\nSelect folder you want to push to github repository !!")
            return

        path = Path(self.dirName).expanduser()
        if not (path / ".git").exists():
            QMessageBox.warning(
                self.main,
                "Not a Git repository",
                "Select the cloned assignment folder that contains a .git directory.",
            )
            return

        quality_checks = self.submission_quality_checks(path)
        self.show_check_results("Submission quality check", quality_checks)
        if any(status == "Fail" for _, status, _, _ in quality_checks):
            reply = QMessageBox.question(
                self.main,
                "Continue with failed checks?",
                "Some required submission checks failed. Continue upload anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        dialog = QtWidgets.QDialog(self.main)
        dialog.setWindowTitle("Upload assignment with GitHub token")
        dialog.setMinimumWidth(520)

        layout = QtWidgets.QVBoxLayout(dialog)
        note = QtWidgets.QLabel(
            "Use a GitHub personal access token instead of your account password. "
            "For GitHub Classroom, the token needs permission to push to this repository."
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        form = QtWidgets.QFormLayout()
        token_input = QtWidgets.QLineEdit()
        token_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        token_input.setPlaceholderText("ghp_... or github_pat_...")
        message_input = QtWidgets.QLineEdit("Submit assignment")
        form.addRow("GitHub token", token_input)
        form.addRow("Commit message", message_input)
        layout.addLayout(form)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Upload")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        self.current_assignment_path = str(path.resolve())
        self.set_assignment_status(
            "submitted",
            True,
            "Assignment marked submitted. Uploading to GitHub...",
        )
        self.upload_assignment(path, token_input.text().strip(), message_input.text().strip())

    def submission_quality_checks(self, path):
        checks = [
            ("Repository", "Pass", f"Git repository found: {path}", ""),
            ("Git user.name", *self.git_config_check("user.name")),
            ("Git user.email", *self.git_config_check("user.email")),
        ]

        notebooks = sorted(path.rglob("*.ipynb"))
        if not notebooks:
            checks.append(("Notebook files", "Warn", "No .ipynb notebook files found", "Confirm this assignment does not require a notebook."))
        else:
            checks.append(("Notebook files", "Pass", f"Found {len(notebooks)} notebook file(s)", ""))
            invalid = []
            empty_code_cells = 0
            no_outputs = 0
            for notebook in notebooks:
                try:
                    data = json.loads(notebook.read_text(encoding="utf-8"))
                except Exception as error:
                    invalid.append(f"{notebook.name}: {error}")
                    continue
                cells = data.get("cells", [])
                code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
                empty_code_cells += sum(
                    1 for cell in code_cells if not "".join(cell.get("source", [])).strip()
                )
                if code_cells and not any(cell.get("outputs") for cell in code_cells):
                    no_outputs += 1
            if invalid:
                checks.append(("Notebook validity", "Fail", "; ".join(invalid[:3]), "Open the notebook and save it again."))
            else:
                checks.append(("Notebook validity", "Pass", "Notebook JSON files are readable", ""))
            if empty_code_cells:
                checks.append(("Empty code cells", "Warn", f"{empty_code_cells} empty code cell(s) found", "Remove unused cells or confirm they are intentional."))
            else:
                checks.append(("Empty code cells", "Pass", "No empty code cells found", ""))
            if no_outputs:
                checks.append(("Notebook outputs", "Warn", f"{no_outputs} notebook(s) have no saved outputs", "Run notebooks from top to bottom and save before upload."))
            else:
                checks.append(("Notebook outputs", "Pass", "Saved outputs are present or no code cells require output", ""))

        artifact_patterns = ("*.png", "*.jpg", "*.jpeg", "*.csv", "*.txt", "*.pdf", "*.h5", "*.keras", "*.pkl")
        artifacts = []
        for pattern in artifact_patterns:
            artifacts.extend(path.rglob(pattern))
        if artifacts:
            checks.append(("Evidence artifacts", "Pass", f"Found {len(artifacts)} output/data artifact(s)", ""))
        else:
            checks.append(("Evidence artifacts", "Warn", "No common output artifacts found", "For image processing or AI, confirm required outputs are saved."))

        status_result = self.run_git(["status", "--porcelain"], path)
        if status_result.returncode != 0:
            checks.append(("Git status", "Fail", status_result.stderr or status_result.stdout, "Fix Git repository status before upload."))
        elif status_result.stdout.strip():
            changed = len(status_result.stdout.strip().splitlines())
            checks.append(("Git changes", "Pass", f"{changed} changed file(s) ready to stage", ""))
        else:
            checks.append(("Git changes", "Warn", "No changed files detected", "If you already committed, this may be okay. Otherwise save your notebook first."))

        return checks

    def run_git(self, args, path):
        try:
            return subprocess.run(
                ["git", *args],
                cwd=str(path),
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except FileNotFoundError:
            result = subprocess.CompletedProcess(["git", *args], 1)
            result.stdout = ""
            result.stderr = "Git command not found. Install Git and make sure it is on PATH."
            return result
        except subprocess.TimeoutExpired:
            result = subprocess.CompletedProcess(["git", *args], 1)
            result.stdout = ""
            result.stderr = "Git command timed out."
            return result

    def upload_assignment(self, path, token, commit_message):
        add_result = self.run_git(["add", "-A"], path)
        if add_result.returncode != 0:
            QMessageBox.warning(self.main, "Git add failed", add_result.stderr or add_result.stdout)
            return

        has_changes = self.run_git(["diff", "--cached", "--quiet"], path).returncode != 0
        if has_changes:
            commit_result = self.run_git(
                ["commit", "-m", commit_message or "Submit assignment"],
                path,
            )
            if commit_result.returncode != 0:
                QMessageBox.warning(
                    self.main,
                    "Git commit failed",
                    "Could not create a commit. Check Git user.name and user.email.\n\n"
                    f"{commit_result.stderr or commit_result.stdout}",
                )
                return

        push_command = ["push"]
        if token:
            push_command = [
                "-c",
                f"http.extraHeader=AUTHORIZATION: bearer {token}",
                "push",
            ]
        push_result = self.run_git(push_command, path)
        if push_result.returncode != 0:
            QMessageBox.warning(
                self.main,
                "Git push failed",
                "Could not push to GitHub. Check the token permission and repository access.\n\n"
                f"{push_result.stderr or push_result.stdout}",
            )
            return

        self.set_assignment_status(
            "pushed",
            True,
            f"Assignment pushed to GitHub: {path}",
        )
        QMessageBox.information(
            self.main,
            "Upload complete",
            "Assignment was committed and pushed to GitHub successfully.",
        )

    def clone(self):
        self.repo_url = self.repo_link.text()
        self.dirName = self.dir_select.text()
        if self.dirName is None:
            QMessageBox.warning(self.main, 'Warning !!', "\nSelect folder you want to push to github repository !!")
        elif self.repo_url == "":
            QMessageBox.warning(self.main, 'Warning !!', "\nPlease write GitHub repository URL !!")
        else:
            self.dialog_2.accept()
            assignment_path = self.clone_repository(self.repo_url, Path(self.dirName))
            if assignment_path is None:
                return
            buttonReply = QMessageBox.question(
                self.main,
                'Clone complete',
                "Assignment is ready. Open it in JupyterHub now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if buttonReply == QMessageBox.StandardButton.Yes:
                self.open_assignment_in_jupyter(assignment_path)

    def clone_repository(self, repo_url, work_dir):
        work_dir = Path(work_dir).expanduser()
        repo_name = self.assignment_folder_name(repo_url)
        assignment_path = work_dir / repo_name
        try:
            work_dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            QMessageBox.warning(self.main, "Folder error", f"Could not create work folder:\n{error}")
            return None

        if assignment_path.exists():
            self.current_assignment_path = str(assignment_path.resolve())
            self.set_assignment_status(
                "cloned",
                True,
                f"Assignment already exists: {self.current_assignment_path}",
            )
            return assignment_path

        result = subprocess.run(
            ["git", "clone", repo_url, str(assignment_path)],
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            QMessageBox.warning(
                self.main,
                "Clone failed",
                "Could not clone the GitHub Classroom repository.\n\n"
                f"{result.stderr or result.stdout}",
            )
            return None

        self.current_assignment_path = str(assignment_path.resolve())
        self.set_assignment_status(
            "cloned",
            True,
            f"Cloned assignment: {self.current_assignment_path}",
        )
        return assignment_path

    def clone_from_github(self):
        self.dialog_2 = QtWidgets.QDialog()
        self.dialog_2.setWindowTitle("Clone repository from GitHub")
        self.dialog_2.setMinimumWidth(550)
        self.dialog_2.setFixedHeight(180)

        VLayout = QtWidgets.QVBoxLayout()
        Hlayout1 = QtWidgets.QHBoxLayout()
        Hlayout2 = QtWidgets.QHBoxLayout()
        Hlayout3 = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(self.dialog_2)
        label.setText(" WorkDir      : ")
        label_1 = QtWidgets.QLabel(self.dialog_2)
        label_1.setText("GitHub URL : ")

        button = QtWidgets.QPushButton()
        button.setText("Open")
        button.setObjectName("button")
        button.clicked.connect(self.open_folder)

        self.dir_select = QtWidgets.QLineEdit()
        self.dir_select.setObjectName("dir_select")
        path = str(Path.home())
        self.dir_select.setText(path)

        self.repo_link = QtWidgets.QLineEdit()

        add = QtWidgets.QPushButton()
        add.setObjectName("add_link")
        add.setText('clone')
        add.clicked.connect(self.clone)

        cancel = QtWidgets.QPushButton()
        cancel.setObjectName("cancel_link")
        cancel.setText('Cancel')
        cancel.clicked.connect(self.dialog_2.reject)

        Hlayout1.addWidget(label)
        Hlayout1.addWidget(self.dir_select)
        Hlayout1.addWidget(button)

        Hlayout2.addWidget(label_1)
        Hlayout2.addWidget(self.repo_link)

        Hlayout3.addStretch()
        Hlayout3.addWidget(add, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        Hlayout3.addWidget(cancel, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        VLayout.addLayout(Hlayout1, 1)
        VLayout.addLayout(Hlayout2, 2)
        VLayout.addLayout(Hlayout3, 3)
        self.dialog_2.setLayout(VLayout)
        self.dialog_2.exec()

    def open_jupyter(self):
        self.start_local_jupyter()
        self.main.add_new_tab(QtCore.QUrl(self.jupyter_url), 'Loading ...')
        self.main.urlbar.setText(self.jupyter_url)

    def plus_home(self):
        self.main.add_new_tab(QtCore.QUrl('https://www.google.com'), 'Google')

    def jupyter_help(self):
        self.main.add_new_tab(QtCore.QUrl("https://jupyter-notebook.readthedocs.io/en/stable/notebook.html"))

    def reload(self):
        if self.main.tabs.count() < 1:
            pass
        else:
            self.main.tabs.currentWidget().reload()

    def back(self):
        if self.main.tabs.count() < 1:
            pass
        else:
            self.main.tabs.currentWidget().back()

    def forward(self):
        if self.main.tabs.count() < 1:
            pass
        else:
            self.main.tabs.currentWidget().forward()

    def open_github(self):
        self.main.add_new_tab(QtCore.QUrl("https://github.com/"), 'Loading ...')

    def open_github_classroom(self):
        self.main.add_new_tab(QtCore.QUrl("https://classroom.github.com/"), 'Loading ...')

    def about_us(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("About Us")
        msgbox.setText("Portable Learning Environment\n\n"
                       "Contact: haryanto462@gmail.com")
        about_icon = QtGui.QPixmap(asset_path("ico.png")).scaled(
            96,
            96,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        msgbox.setIconPixmap(about_icon)
        msgbox.exec()

    def open_help(self):
        help_path = Path(__file__).resolve().parent / "assets" / "help.html"
        self.main.add_new_tab(QUrl.fromLocalFile(str(help_path)))

    def open_stuck_help(self):
        help_path = Path(__file__).resolve().parent / "assets" / "stuck.html"
        self.main.add_new_tab(QUrl.fromLocalFile(str(help_path)), "Help stuck students")

    def exit(self):
        self.shutdown_jupyter()
        self.main.close()
