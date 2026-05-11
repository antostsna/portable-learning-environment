from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QMetaObject, QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QFont, QIcon, QPixmap
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


ASSET_DIR = Path(__file__).resolve().parent / "assets"


def asset_path(name):
    return str(ASSET_DIR / name)


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab = self.parent()

    def createWindow(self, windowType):
        if windowType == QWebEnginePage.WebWindowType.WebBrowserTab:
            webView = HtmlView(self.tab)
            i = self.tab.addTab(webView, "Loading ...")
            self.tab.setCurrentIndex(i)
            webView.urlChanged.connect(
                lambda url, browser=webView: self.update_urlbar(url, browser)
            )
            webView.loadFinished.connect(
                lambda _, i=i, browser=webView: self.tab.setTabText(
                    i, browser.page().title() or "New tab"
                )
            )
            return webView
        return super().createWindow(windowType)

    def update_urlbar(self, q, browser=None):
        if browser != self.tab.currentWidget():
            return


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shutdown_callback = None
        self.tabs = TabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setObjectName("tabs")
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.init_Ui()

    def init_Ui(self):
        self.statusBar().showMessage("Ready")
        self.setMinimumSize(760, 560)
        self.resize(1180, 780)
        self.setWindowIcon(QIcon(asset_path("ico.png")))

        self.stack = QStackedWidget(self)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("home")
        self.homeScroll = QScrollArea(self)
        self.homeScroll.setWidgetResizable(True)
        self.homeScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.homeScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.homeScroll.setWidget(self.centralwidget)
        self.stack.addWidget(self.homeScroll)
        self.stack.addWidget(self.tabs)
        self.setCentralWidget(self.stack)

        page_layout = QVBoxLayout(self.centralwidget)
        page_layout.setContentsMargins(28, 28, 28, 28)
        page_layout.setSpacing(22)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(22)

        logo = QLabel()
        logo.setFixedSize(72, 72)
        logo.setPixmap(QPixmap(asset_path("ico.png")))
        logo.setScaledContents(True)
        header_layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignTop)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)
        self.label = QLabel()
        self.label.setObjectName("title")
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        title_font = QFont()
        title_font.setPointSize(26)
        title_font.setBold(True)
        self.label.setFont(title_font)

        self.label_2 = QLabel()
        self.label_2.setObjectName("subtitle")
        self.label_2.setWordWrap(True)
        self.label_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        self.label_2.setFont(subtitle_font)

        title_layout.addWidget(self.label)
        title_layout.addWidget(self.label_2)
        header_layout.addLayout(title_layout, 1)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("primaryButton")
        self.pushButton.setIcon(QIcon(asset_path("jupyter.png")))
        self.pushButton.setIconSize(QSize(42, 42))
        self.pushButton.setMinimumHeight(58)
        self.pushButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.startLessonButton = QPushButton()
        self.startLessonButton.setObjectName("secondaryButton")
        self.startLessonButton.setIcon(QIcon(asset_path("github_class_2.png")))
        self.startLessonButton.setIconSize(QSize(32, 32))
        self.startLessonButton.setMinimumHeight(58)
        self.startLessonButton.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self.startLessonButton)
        button_layout.addWidget(self.pushButton)
        header_layout.addLayout(button_layout, 0)

        page_layout.addLayout(header_layout)

        self.quick_grid = QGridLayout()
        self.quick_grid.setHorizontalSpacing(18)
        self.quick_grid.setVerticalSpacing(18)
        self.jupyterCard = self._build_info_panel(
            "JupyterHub workspace",
            "Open notebooks, labs, datasets, and student assignment folders.",
        )
        self.classroomCard = self._build_info_panel(
            "GitHub Classroom",
            "Clone starter repositories and review submitted work from one place.",
        )
        self.practiceCard = self._build_info_panel(
            "Teaching flow",
            "Choose lecture mode, notebook practice, or teacher-controlled JupyterHub.",
        )
        self.quickCards = [self.jupyterCard, self.classroomCard, self.practiceCard]
        page_layout.addLayout(self.quick_grid)

        self.lessonPanel = QFrame()
        self.lessonPanel.setObjectName("lessonPanel")
        self.lesson_layout = QGridLayout(self.lessonPanel)
        self.lesson_layout.setContentsMargins(20, 16, 20, 16)
        self.lesson_layout.setHorizontalSpacing(16)
        self.lesson_layout.setVerticalSpacing(10)

        lesson_title = QLabel("Lesson setup")
        lesson_title.setObjectName("panelTitle")
        self.lessonTitle = lesson_title

        self.courseLabel = QLabel("Course type")
        self.courseLabel.setObjectName("fieldLabel")
        self.courseModeSelect = QComboBox()
        self.courseModeSelect.addItems(
            [
                "General lecture",
                "Programming language",
                "Digital image processing",
                "AI / machine learning",
                "General lab",
            ]
        )

        self.deliveryLabel = QLabel("Delivery")
        self.deliveryLabel.setObjectName("fieldLabel")
        self.deliveryModeSelect = QComboBox()
        self.deliveryModeSelect.addItems(
            [
                "Student practice - local Jupyter Notebook",
                "Teacher controlled - JupyterHub",
            ]
        )

        self.lessonPreview = QLabel()
        self.lessonPreview.setObjectName("lessonPreview")
        self.lessonPreview.setWordWrap(True)

        self.stuckHelpButton = QPushButton()
        self.stuckHelpButton.setObjectName("secondaryButton")
        self.stuckHelpButton.setMinimumHeight(40)
        self.stuckHelpButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.preflightButton = QPushButton()
        self.preflightButton.setObjectName("secondaryButton")
        self.preflightButton.setMinimumHeight(40)
        self.preflightButton.setCursor(Qt.CursorShape.PointingHandCursor)

        page_layout.addWidget(self.lessonPanel)

        self.statusPanel = QFrame()
        self.statusPanel.setObjectName("statusPanel")
        status_layout = QVBoxLayout(self.statusPanel)
        status_layout.setContentsMargins(20, 16, 20, 16)
        status_layout.setSpacing(12)

        status_title = QLabel("Assignment status")
        status_title.setObjectName("panelTitle")
        status_layout.addWidget(status_title)

        self.status_grid = QGridLayout()
        self.status_grid.setHorizontalSpacing(12)
        self.status_grid.setVerticalSpacing(10)
        self.assignmentStatusLabels = {}
        self.statusBarBadges = {}
        self.statusOrder = ("cloned", "opened", "submitted", "pushed")
        for name in self.statusOrder:
            label = QLabel()
            label.setObjectName("statusBadge")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.assignmentStatusLabels[name] = label

            bar_label = QLabel()
            bar_label.setObjectName("statusBadge")
            bar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.statusBarBadges[name] = bar_label
            self.statusBar().addPermanentWidget(bar_label)
        status_layout.addLayout(self.status_grid)

        self.assignmentStatusDetail = QLabel()
        self.assignmentStatusDetail.setObjectName("panelBody")
        self.assignmentStatusDetail.setWordWrap(True)
        status_layout.addWidget(self.assignmentStatusDetail)
        page_layout.addWidget(self.statusPanel)

        page_layout.addStretch()
        self.developerLabel = QLabel()
        self.developerLabel.setObjectName("developerLabel")
        self.developerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        page_layout.addWidget(self.developerLabel)

        self._build_menus()
        self._build_toolbar()
        self._apply_style()
        self.apply_responsive_layout(self.width())
        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    def _build_info_panel(self, title, body):
        panel = QFrame()
        panel.setObjectName("infoPanel")
        panel.setMinimumHeight(140)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 18, 20, 18)
        panel_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("panelTitle")
        title_label.setWordWrap(True)

        body_label = QLabel(body)
        body_label.setObjectName("panelBody")
        body_label.setWordWrap(True)

        panel_layout.addWidget(title_label)
        panel_layout.addWidget(body_label)
        panel_layout.addStretch()
        return panel

    def _build_menus(self):
        self.menuBar = QMenuBar(self)
        self.menuAssigment = QMenu(self.menuBar)
        self.menuHelp = QMenu(self.menuBar)
        self.menuFile = QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)

        self.actionOpen = QAction(self)
        self.actionClose = QAction(self)
        self.actionCreate_2 = QAction(self)
        self.actionUpdate_2 = QAction(self)
        self.actionPush = QAction(self)
        self.actionPull = QAction(self)
        self.actionWeek_3 = QAction(self)
        self.actionWeek_4 = QAction(self)
        self.actionexit = QAction(self)
        self.actionInfo = QAction(self)
        self.actionNew = QAction(self)
        self.actionExport = QAction(self)
        self.actionPush_To_Github = QAction(self)
        self.actionClone_from_Github = QAction(self)
        self.actionHelp = QAction(self)
        self.actionAbout_Us = QAction(self)
        self.actionHelpJup = QAction(self)
        self.actionStartLesson = QAction(self)
        self.actionStuckHelp = QAction(self)
        self.actionPreflight = QAction(self)

        self.menuAssigment.addAction(self.actionPreflight)
        self.menuAssigment.addAction(self.actionStartLesson)
        self.menuAssigment.addSeparator()
        self.menuAssigment.addAction(self.actionCreate_2)
        self.menuAssigment.addAction(self.actionUpdate_2)

        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionStuckHelp)
        self.menuHelp.addAction(self.actionHelpJup)
        self.menuHelp.addAction(self.actionAbout_Us)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionInfo)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionPush_To_Github)
        self.menuFile.addAction(self.actionClone_from_Github)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionexit)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAssigment.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

    def _build_toolbar(self):
        self.back = QAction(QIcon(asset_path("left.png")), "&Back", self)
        self.forward = QAction(QIcon(asset_path("right.png")), "&Forward", self)
        self.reload = QAction(QIcon(asset_path("reload.png")), "&Reload", self)
        self.home = QAction(QIcon(asset_path("home.png")), "&Home", self)
        self.plus = QAction(QIcon(asset_path("plus.png")), "&New Tab", self)
        self.jupyter = QAction(QIcon(asset_path("jupyter.png")), "&JupyterHub", self)
        self.github = QAction(QIcon(asset_path("github_2.png")), "&GitHub", self)
        self.github_class = QAction(
            QIcon(asset_path("github_class_2.png")), "&GitHub Classroom", self
        )

        self.urlbar = QLineEdit()
        self.urlbar.setObjectName("urlbar")
        self.urlbar.setPlaceholderText("Enter a URL or local notebook path")
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.toolBar = QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(24, 24))
        self.toolBar.addAction(self.jupyter)
        self.toolBar.addAction(self.github)
        self.toolBar.addAction(self.github_class)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.back)
        self.toolBar.addAction(self.forward)
        self.toolBar.addAction(self.reload)
        self.toolBar.addAction(self.home)
        self.toolBar.addAction(self.plus)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.urlbar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background: #f5f7fb;
                color: #172033;
                font-family: "Segoe UI", "Noto Sans", Arial, sans-serif;
            }
            QWidget#home {
                background: #f5f7fb;
            }
            QLabel#title {
                color: #172033;
                letter-spacing: 0;
            }
            QLabel#subtitle,
            QLabel#panelBody {
                color: #536174;
                line-height: 1.35;
            }
            QLabel#developerLabel {
                color: #7b8794;
                font-size: 11px;
            }
            QLabel#fieldLabel {
                color: #536174;
                font-weight: 700;
            }
            QLabel#lessonPreview {
                background: #eef3fb;
                color: #172033;
                border-left: 4px solid #1f6feb;
                border-radius: 6px;
                padding: 10px 12px;
            }
            QFrame#infoPanel {
                background: #ffffff;
                border: 1px solid #dfe5ef;
                border-radius: 8px;
            }
            QLabel#panelTitle {
                color: #172033;
                font-size: 17px;
                font-weight: 700;
            }
            QPushButton#primaryButton {
                background: #1f6feb;
                color: #ffffff;
                border: 0;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 15px;
                font-weight: 700;
            }
            QPushButton#primaryButton:hover {
                background: #185abd;
            }
            QPushButton#secondaryButton {
                background: #ffffff;
                color: #172033;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 15px;
                font-weight: 700;
            }
            QPushButton#secondaryButton:hover {
                background: #eef3fb;
            }
            QPushButton {
                min-width: 0;
            }
            QFrame#lessonPanel,
            QFrame#statusPanel {
                background: #ffffff;
                border: 1px solid #dfe5ef;
                border-radius: 8px;
            }
            QComboBox {
                min-height: 34px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 10px;
                background: #ffffff;
                color: #172033;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #eef3fb;
            }
            QLabel#statusBadge {
                background: #f1f5f9;
                color: #536174;
                border: 1px solid #dfe5ef;
                border-radius: 6px;
                padding: 7px 10px;
                font-weight: 700;
            }
            QLabel#statusBadge[complete="true"] {
                background: #e8f5ee;
                color: #146c43;
                border-color: #b7e0c7;
            }
            QToolBar#toolBar {
                background: #ffffff;
                border-bottom: 1px solid #dfe5ef;
                spacing: 8px;
                padding: 6px;
            }
            QToolButton {
                border: 0;
                border-radius: 6px;
                padding: 6px;
            }
            QToolButton:hover {
                background: #eef3fb;
            }
            QLineEdit#urlbar {
                min-height: 30px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 10px;
                background: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #dfe5ef;
            }
            QTabBar::tab {
                background: #e9eef6;
                color: #344054;
                padding: 8px 14px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #172033;
            }
            QMenuBar {
                background: #ffffff;
                border-bottom: 1px solid #edf1f7;
            }
            QStatusBar {
                background: #ffffff;
                color: #536174;
            }
            """
        )

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def tab_widget(self):
        self.stack.setCurrentWidget(self.tabs)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "quickCards"):
            self.apply_responsive_layout(event.size().width())

    def apply_responsive_layout(self, width):
        if width < 860:
            card_columns = 1
            status_columns = 2
            compact = True
        elif width < 1120:
            card_columns = 2
            status_columns = 2
            compact = False
        else:
            card_columns = 3
            status_columns = 4
            compact = False

        for card in self.quickCards:
            self.quick_grid.removeWidget(card)
        for index, card in enumerate(self.quickCards):
            self.quick_grid.addWidget(card, index // card_columns, index % card_columns)

        for label in self.assignmentStatusLabels.values():
            self.status_grid.removeWidget(label)
        for index, name in enumerate(self.statusOrder):
            self.status_grid.addWidget(
                self.assignmentStatusLabels[name],
                index // status_columns,
                index % status_columns,
            )

        for widget in (
            self.lessonTitle,
            self.courseLabel,
            self.deliveryLabel,
            self.courseModeSelect,
            self.deliveryModeSelect,
            self.lessonPreview,
            self.preflightButton,
            self.stuckHelpButton,
        ):
            self.lesson_layout.removeWidget(widget)

        if compact:
            self.lesson_layout.addWidget(self.lessonTitle, 0, 0)
            self.lesson_layout.addWidget(self.courseLabel, 1, 0)
            self.lesson_layout.addWidget(self.courseModeSelect, 2, 0)
            self.lesson_layout.addWidget(self.deliveryLabel, 3, 0)
            self.lesson_layout.addWidget(self.deliveryModeSelect, 4, 0)
            self.lesson_layout.addWidget(self.lessonPreview, 5, 0)
            self.lesson_layout.addWidget(self.preflightButton, 6, 0)
            self.lesson_layout.addWidget(self.stuckHelpButton, 7, 0)
            self.statusBar().setVisible(False)
        else:
            self.lesson_layout.addWidget(self.lessonTitle, 0, 0, 1, 2)
            self.lesson_layout.addWidget(self.courseLabel, 1, 0)
            self.lesson_layout.addWidget(self.deliveryLabel, 1, 1)
            self.lesson_layout.addWidget(self.courseModeSelect, 2, 0)
            self.lesson_layout.addWidget(self.deliveryModeSelect, 2, 1)
            self.lesson_layout.addWidget(self.lessonPreview, 3, 0, 1, 2)
            self.lesson_layout.addWidget(self.preflightButton, 4, 0)
            self.lesson_layout.addWidget(self.stuckHelpButton, 4, 1)
            self.statusBar().setVisible(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.shutdown_callback is not None:
                self.shutdown_callback()
            event.accept()
        else:
            event.ignore()

    def add_new_tab(self, url=None, label="Blank"):
        self.tab_widget()
        if url is None:
            url = QUrl("https://www.google.com")
        browser = HtmlView(self.tabs)
        browser.setUrl(url)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(
            lambda url, browser=browser: self.update_urlbar(url, browser)
        )
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(
                i, browser.page().title() or "New tab"
            )
        )

    def current_tab_changed(self, i):
        if i == -1:
            self.urlbar.setText("")
        else:
            qurl = self.tabs.currentWidget().url()
            self.update_urlbar(qurl, self.tabs.currentWidget())

    def navigate_to_url(self):
        if self.tabs.count() < 1:
            self.add_new_tab(QUrl(self.urlbar.text()))
            return
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("https")
        self.tabs.currentWidget().setUrl(q)

    def navigate_home(self):
        self.urlbar.setText("")
        self.stack.setCurrentWidget(self.homeScroll)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        self.statusBar().showMessage(q.toString())

    def close_current_tab(self, i):
        if self.tabs.count() < 1:
            return
        self.tabs.removeTab(i)
        if self.tabs.count() == 0:
            self.urlbar.setText("")
            self.stack.setCurrentWidget(self.homeScroll)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Portable Learning Environment")
        )
        self.toolBar.setWindowTitle(_translate("MainWindow", "Navigation"))
        self.menuAssigment.setTitle(_translate("MainWindow", "Assignment"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionCreate_2.setText(_translate("MainWindow", "Clone assignment"))
        self.actionUpdate_2.setText(_translate("MainWindow", "Upload assignment"))
        self.actionPreflight.setText(_translate("MainWindow", "Pre-flight check"))
        self.actionStartLesson.setText(_translate("MainWindow", "Start lesson"))
        self.actionPush.setText(_translate("MainWindow", "Push"))
        self.actionPull.setText(_translate("MainWindow", "Pull"))
        self.actionWeek_3.setText(_translate("MainWindow", "Week 1"))
        self.actionWeek_4.setText(_translate("MainWindow", "Week 2"))
        self.actionexit.setText(_translate("MainWindow", "Exit"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionPush_To_Github.setText(_translate("MainWindow", "Push to GitHub"))
        self.actionClone_from_Github.setText(
            _translate("MainWindow", "Clone from GitHub")
        )
        self.actionHelp.setText(_translate("MainWindow", "Help Center"))
        self.actionStuckHelp.setText(_translate("MainWindow", "Help stuck students"))
        self.actionAbout_Us.setText(_translate("MainWindow", "About"))
        self.actionHelpJup.setText(_translate("MainWindow", "Jupyter Notebook"))
        self.pushButton.setText(_translate("MainWindow", "Open JupyterHub"))
        self.startLessonButton.setText(_translate("MainWindow", "Start lesson"))
        self.preflightButton.setText(_translate("MainWindow", "Pre-flight check"))
        self.stuckHelpButton.setText(_translate("MainWindow", "Help stuck students"))
        self.label.setText(
            _translate("MainWindow", "Portable Learning Environment")
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                "A focused workspace for notebooks, GitHub Classroom assignments, "
                "and guided programming practice.",
            )
        )
        self.developerLabel.setText(_translate("MainWindow", "Developed by Haryanto"))
        self.update_lesson_preview()
        self.courseModeSelect.currentTextChanged.connect(self.update_lesson_preview)
        self.deliveryModeSelect.currentTextChanged.connect(self.update_lesson_preview)
        self.set_assignment_status(
            {
                "cloned": False,
                "opened": False,
                "submitted": False,
                "pushed": False,
            },
            "No assignment started yet. Use Start lesson to guide students through setup.",
        )

    def set_assignment_status(self, statuses, detail=None):
        labels = {
            "cloned": "Cloned",
            "opened": "Opened",
            "submitted": "Submitted",
            "pushed": "Pushed",
        }
        for key, label in self.assignmentStatusLabels.items():
            complete = bool(statuses.get(key, False))
            label.setText(("Done: " if complete else "Waiting: ") + labels[key])
            label.setProperty("complete", complete)
            label.style().unpolish(label)
            label.style().polish(label)
            bar_label = self.statusBarBadges[key]
            bar_label.setText(("Done: " if complete else "Wait: ") + labels[key])
            bar_label.setProperty("complete", complete)
            bar_label.style().unpolish(bar_label)
            bar_label.style().polish(bar_label)
        if detail is not None:
            self.assignmentStatusDetail.setText(detail)

    def lesson_preferences(self):
        return {
            "course": self.courseModeSelect.currentText(),
            "delivery": self.deliveryModeSelect.currentText(),
        }

    def update_lesson_preview(self):
        course_notes = {
            "General lecture": "Use this for concept explanation, demonstration, discussion, and a short exit ticket.",
            "Programming language": "Focus on syntax practice, debugging, functions, control flow, and code explanation.",
            "Digital image processing": "Guide students through image loading, transformation, filtering, comparison, and output evidence.",
            "AI / machine learning": "Guide students through dataset inspection, model training, evaluation, and result reflection.",
            "General lab": "Use this for open-ended lab work with setup checks, checkpoints, evidence, and submission.",
        }
        delivery_notes = {
            "Student practice - local Jupyter Notebook": "Students practice on a local notebook server started only when needed.",
            "Teacher controlled - JupyterHub": "The teacher or institution controls the notebook server and student environment.",
        }
        course = self.courseModeSelect.currentText()
        delivery = self.deliveryModeSelect.currentText()
        self.lessonPreview.setText(
            f"{course_notes.get(course, '')} {delivery_notes.get(delivery, '')}"
        )
