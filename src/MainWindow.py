from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QMetaObject, QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QFont, QIcon, QPixmap
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QTextBrowser,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ple.core import ASSET_DIR, DOCS_DIR, asset_path
from ple.views.theme import load_stylesheet


# Documentation entries shown in the in-app docs browser come from the model.
from ple.models import DOC_ENTRIES  # noqa: E402  (kept near the other doc imports for readability)


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

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def init_Ui(self):
        self.statusBar().showMessage("Ready")
        self.setMinimumSize(960, 620)
        self.resize(1280, 820)
        self.setWindowIcon(QIcon(asset_path("ico.png")))

        # Root container: sidebar (nav) + content stack
        self.rootSplit = QSplitter(Qt.Orientation.Horizontal, self)
        self.rootSplit.setChildrenCollapsible(False)
        self.rootSplit.setHandleWidth(1)

        self._build_sidebar()
        self.rootSplit.addWidget(self.sidebar)

        # Right side: a stack that holds Home / Docs / Settings / About / Browser
        self.contentStack = QStackedWidget(self)
        self.contentStack.setObjectName("contentStack")

        self._build_home_page()
        self._build_docs_page()
        self._build_settings_page()
        self._build_about_page()

        # Browser tab area (shown when a tab opens a notebook or web page)
        self.tabsContainer = QWidget()
        tabs_layout = QVBoxLayout(self.tabsContainer)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(0)
        tabs_layout.addWidget(self.tabs)

        # Index order matters — kept in self.PAGE_* constants below
        self.contentStack.addWidget(self.homeScroll)      # 0
        self.contentStack.addWidget(self.docsPage)        # 1
        self.contentStack.addWidget(self.settingsPage)    # 2
        self.contentStack.addWidget(self.aboutPage)       # 3
        self.contentStack.addWidget(self.tabsContainer)   # 4

        self.PAGE_HOME = 0
        self.PAGE_DOCS = 1
        self.PAGE_SETTINGS = 2
        self.PAGE_ABOUT = 3
        self.PAGE_BROWSER = 4

        self.rootSplit.addWidget(self.contentStack)
        self.rootSplit.setStretchFactor(0, 0)
        self.rootSplit.setStretchFactor(1, 1)
        self.rootSplit.setSizes([220, 1060])

        self.setCentralWidget(self.rootSplit)

        self._build_menus()
        self._build_toolbar()
        self._apply_style()
        self.apply_responsive_layout(self.width())
        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

        # Default landing page
        self.show_page(self.PAGE_HOME)

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    def _build_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMinimumWidth(196)
        self.sidebar.setMaximumWidth(280)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setSpacing(6)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)
        brand_icon = QLabel()
        brand_icon.setFixedSize(32, 32)
        brand_icon.setPixmap(QPixmap(asset_path("ico.png")))
        brand_icon.setScaledContents(True)
        brand_text = QLabel("PLE")
        brand_text.setObjectName("brandText")
        brand_row.addWidget(brand_icon)
        brand_row.addWidget(brand_text)
        brand_row.addStretch()
        layout.addLayout(brand_row)

        subtitle = QLabel("Portable Learning\nEnvironment")
        subtitle.setObjectName("brandSubtitle")
        layout.addWidget(subtitle)
        layout.addSpacing(14)

        nav_label = QLabel("WORKSPACE")
        nav_label.setObjectName("navSectionLabel")
        layout.addWidget(nav_label)

        self.navButtons = {}
        self.navGroup = QButtonGroup(self)
        self.navGroup.setExclusive(True)

        def make_nav(key, text):
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(36)
            layout.addWidget(button)
            self.navButtons[key] = button
            self.navGroup.addButton(button)
            return button

        self.navHomeBtn = make_nav("home", "  Home")
        self.navDocsBtn = make_nav("docs", "  Documentation")
        self.navSettingsBtn = make_nav("settings", "  Settings")
        self.navAboutBtn = make_nav("about", "  About")

        layout.addSpacing(18)
        actions_label = QLabel("QUICK ACTIONS")
        actions_label.setObjectName("navSectionLabel")
        layout.addWidget(actions_label)

        self.sidebarPreflightBtn = QPushButton("  Pre-flight check")
        self.sidebarPreflightBtn.setObjectName("navButtonGhost")
        self.sidebarPreflightBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebarPreflightBtn.setMinimumHeight(32)
        layout.addWidget(self.sidebarPreflightBtn)

        self.sidebarStartLessonBtn = QPushButton("  Start lesson")
        self.sidebarStartLessonBtn.setObjectName("navButtonGhost")
        self.sidebarStartLessonBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebarStartLessonBtn.setMinimumHeight(32)
        layout.addWidget(self.sidebarStartLessonBtn)

        self.sidebarOpenJupyterBtn = QPushButton("  Open Jupyter")
        self.sidebarOpenJupyterBtn.setObjectName("navButtonGhost")
        self.sidebarOpenJupyterBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebarOpenJupyterBtn.setMinimumHeight(32)
        layout.addWidget(self.sidebarOpenJupyterBtn)

        layout.addStretch()
        footer = QLabel("v2026.05 · MIT")
        footer.setObjectName("sidebarFooter")
        layout.addWidget(footer)

        # Wire nav buttons
        self.navHomeBtn.clicked.connect(lambda: self.show_page(self.PAGE_HOME))
        self.navDocsBtn.clicked.connect(lambda: self.show_page(self.PAGE_DOCS))
        self.navSettingsBtn.clicked.connect(lambda: self.show_page(self.PAGE_SETTINGS))
        self.navAboutBtn.clicked.connect(lambda: self.show_page(self.PAGE_ABOUT))

    def show_page(self, index):
        self.contentStack.setCurrentIndex(index)
        nav_map = {
            self.PAGE_HOME: self.navHomeBtn,
            self.PAGE_DOCS: self.navDocsBtn,
            self.PAGE_SETTINGS: self.navSettingsBtn,
            self.PAGE_ABOUT: self.navAboutBtn,
        }
        button = nav_map.get(index)
        if button is not None:
            button.setChecked(True)
        else:
            for b in self.navButtons.values():
                b.setChecked(False)

    def toggle_sidebar(self):
        """Show or hide the left navigation sidebar.

        Navigation stays reachable when hidden via the View menu and the
        toolbar, so collapsing it never traps the user.
        """
        self.sidebar.setVisible(not self.sidebar.isVisible())

    # ------------------------------------------------------------------
    # Home page
    # ------------------------------------------------------------------
    def _build_home_page(self):
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("home")
        self.homeScroll = QScrollArea(self)
        self.homeScroll.setWidgetResizable(True)
        self.homeScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.homeScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.homeScroll.setWidget(self.centralwidget)

        page_layout = QVBoxLayout(self.centralwidget)
        page_layout.setContentsMargins(36, 32, 36, 32)
        page_layout.setSpacing(24)

        # ---- Hero header
        header = QFrame()
        header.setObjectName("hero")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(28, 24, 28, 24)
        header_layout.setSpacing(22)

        title_block = QVBoxLayout()
        title_block.setSpacing(8)

        eyebrow = QLabel("WORKSPACE")
        eyebrow.setObjectName("heroEyebrow")

        self.label = QLabel()
        self.label.setObjectName("title")
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.label.setFont(title_font)

        self.label_2 = QLabel()
        self.label_2.setObjectName("subtitle")
        self.label_2.setWordWrap(True)
        self.label_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        self.label_2.setFont(subtitle_font)

        title_block.addWidget(eyebrow)
        title_block.addWidget(self.label)
        title_block.addWidget(self.label_2)
        header_layout.addLayout(title_block, 1)

        cta_block = QVBoxLayout()
        cta_block.setSpacing(8)

        # Primary action for everyone: open a local Jupyter Notebook.
        self.pushButton = QPushButton()
        self.pushButton.setObjectName("primaryButton")
        self.pushButton.setMinimumHeight(44)
        self.pushButton.setMinimumWidth(190)
        self.pushButton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Connect to an institution JupyterHub.
        self.openHubButton = QPushButton()
        self.openHubButton.setObjectName("secondaryButton")
        self.openHubButton.setMinimumHeight(44)
        self.openHubButton.setMinimumWidth(190)
        self.openHubButton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Teacher-oriented guided flow (still available to everyone).
        self.startLessonButton = QPushButton()
        self.startLessonButton.setObjectName("secondaryButton")
        self.startLessonButton.setMinimumHeight(44)
        self.startLessonButton.setMinimumWidth(190)
        self.startLessonButton.setCursor(Qt.CursorShape.PointingHandCursor)

        cta_block.addWidget(self.pushButton)
        cta_block.addWidget(self.openHubButton)
        cta_block.addWidget(self.startLessonButton)
        cta_block.addStretch()
        header_layout.addLayout(cta_block, 0)

        page_layout.addWidget(header)

        # ---- Info cards row
        self.quick_grid = QGridLayout()
        self.quick_grid.setHorizontalSpacing(18)
        self.quick_grid.setVerticalSpacing(18)
        self.jupyterCard = self._build_info_panel(
            "Notebook workspace",
            "Open Jupyter notebooks, labs, datasets, and assignment folders.",
        )
        self.classroomCard = self._build_info_panel(
            "GitHub Classroom",
            "Clone starter repositories and submit student work from one place.",
        )
        self.practiceCard = self._build_info_panel(
            "Guided teaching",
            "Course-aware checklists, pre-flight checks, and submission preview.",
        )
        self.quickCards = [self.jupyterCard, self.classroomCard, self.practiceCard]
        page_layout.addLayout(self.quick_grid)

        # ---- Lesson setup panel
        self.lessonPanel = QFrame()
        self.lessonPanel.setObjectName("lessonPanel")
        self.lesson_layout = QGridLayout(self.lessonPanel)
        self.lesson_layout.setContentsMargins(24, 20, 24, 20)
        self.lesson_layout.setHorizontalSpacing(16)
        self.lesson_layout.setVerticalSpacing(12)

        self.lessonTitle = QLabel("Lesson setup")
        self.lessonTitle.setObjectName("panelTitle")

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

        # ---- Assignment status panel
        self.statusPanel = QFrame()
        self.statusPanel.setObjectName("statusPanel")
        status_layout = QVBoxLayout(self.statusPanel)
        status_layout.setContentsMargins(24, 20, 24, 20)
        status_layout.setSpacing(14)

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

    def _help_icon(self, tooltip, doc_filename=None):
        """Tiny round '?' button that shows a tooltip on hover and opens the named
        doc in the in-app docs viewer on click. The controller wires the click to
        Controller.show_doc via the `helpIcons` registry.
        """
        button = QPushButton("?")
        button.setObjectName("helpIcon")
        button.setFixedSize(20, 20)
        button.setCursor(Qt.CursorShape.WhatsThisCursor)
        button.setToolTip(tooltip)
        button.setProperty("docFilename", doc_filename or "")
        if not hasattr(self, "helpIcons"):
            self.helpIcons = []
        self.helpIcons.append(button)
        return button

    def _row_with_help(self, widget, tooltip, doc_filename=None):
        """Wrap a widget with a trailing help icon."""
        wrap = QWidget()
        row = QHBoxLayout(wrap)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        row.addWidget(widget, 1)
        row.addWidget(self._help_icon(tooltip, doc_filename), 0)
        return wrap

    def _build_info_panel(self, title, body):
        panel = QFrame()
        panel.setObjectName("infoPanel")
        panel.setMinimumHeight(132)
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

    # ------------------------------------------------------------------
    # Docs page (in-app markdown viewer)
    # ------------------------------------------------------------------
    def _build_docs_page(self):
        self.docsPage = QWidget()
        self.docsPage.setObjectName("docsPage")
        outer = QVBoxLayout(self.docsPage)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QFrame()
        header.setObjectName("pageHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(36, 24, 36, 18)
        header_layout.setSpacing(4)

        title = QLabel("Documentation")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Guides, setup instructions, and reference. Click an item to open."
        )
        subtitle.setObjectName("pageSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        outer.addWidget(header)

        body = QSplitter(Qt.Orientation.Horizontal, self.docsPage)
        body.setChildrenCollapsible(False)
        body.setHandleWidth(1)

        # Left: list of docs
        list_wrap = QFrame()
        list_wrap.setObjectName("docsListWrap")
        list_layout = QVBoxLayout(list_wrap)
        list_layout.setContentsMargins(24, 12, 12, 24)
        list_layout.setSpacing(8)

        self.docsList = QListWidget()
        self.docsList.setObjectName("docsList")
        self.docsList.setSpacing(2)
        for entry in DOC_ENTRIES:
            item = QListWidgetItem(f"{entry.title}\n{entry.subtitle}")
            item.setData(Qt.ItemDataRole.UserRole, entry.filename)
            self.docsList.addItem(item)
        self.docsList.setMinimumWidth(260)
        self.docsList.setMaximumWidth(360)
        list_layout.addWidget(self.docsList)

        open_in_editor = QPushButton("Open docs folder")
        open_in_editor.setObjectName("secondaryButton")
        open_in_editor.setCursor(Qt.CursorShape.PointingHandCursor)
        open_in_editor.setMinimumHeight(36)
        self.docsOpenFolderBtn = open_in_editor
        list_layout.addWidget(open_in_editor)

        body.addWidget(list_wrap)

        # Right: rendered markdown
        viewer_wrap = QFrame()
        viewer_wrap.setObjectName("docsViewerWrap")
        viewer_layout = QVBoxLayout(viewer_wrap)
        viewer_layout.setContentsMargins(24, 12, 36, 24)
        viewer_layout.setSpacing(10)

        self.docsCurrentTitle = QLabel("Select a document on the left")
        self.docsCurrentTitle.setObjectName("docsCurrentTitle")
        viewer_layout.addWidget(self.docsCurrentTitle)

        self.docsViewer = QTextBrowser()
        self.docsViewer.setObjectName("docsViewer")
        self.docsViewer.setOpenExternalLinks(True)
        self.docsViewer.setSearchPaths([str(DOCS_DIR)])
        viewer_layout.addWidget(self.docsViewer, 1)

        body.addWidget(viewer_wrap)
        body.setStretchFactor(0, 0)
        body.setStretchFactor(1, 1)
        body.setSizes([300, 800])

        outer.addWidget(body, 1)

        # Convenience: auto-select first entry when page is shown
        if self.docsList.count() > 0:
            self.docsList.setCurrentRow(0)

    # ------------------------------------------------------------------
    # Settings page
    # ------------------------------------------------------------------
    def _build_settings_page(self):
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName("settingsPage")
        outer = QVBoxLayout(self.settingsPage)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QFrame()
        header.setObjectName("pageHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(36, 24, 36, 18)
        header_layout.setSpacing(4)

        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Preferences are saved on this computer using Qt's settings store."
        )
        subtitle.setObjectName("pageSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        outer.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(36, 12, 36, 24)
        body_layout.setSpacing(20)

        # JupyterHub URL
        hub_card = self._settings_card(
            "JupyterHub URL",
            "Leave blank to use local Jupyter for student practice. Set this when your institution provides a JupyterHub server.",
        )
        self.settingsHubUrl = QLineEdit()
        self.settingsHubUrl.setPlaceholderText("https://your-jupyterhub.example.edu/hub/login")
        hub_card.layout().addWidget(
            self._row_with_help(
                self.settingsHubUrl,
                "Click for the Delivery guide — explains when to use JupyterHub vs local notebook.",
                "DELIVERY.md",
            )
        )
        body_layout.addWidget(hub_card)

        # Default work folder
        folder_card = self._settings_card(
            "Default work folder",
            "Where cloned assignments will be saved by default.",
        )
        folder_row = QHBoxLayout()
        self.settingsWorkFolder = QLineEdit()
        self.settingsWorkFolder.setPlaceholderText(str(Path.home()))
        self.settingsWorkFolderBrowse = QPushButton("Browse")
        self.settingsWorkFolderBrowse.setObjectName("secondaryButton")
        self.settingsWorkFolderBrowse.setCursor(Qt.CursorShape.PointingHandCursor)
        folder_row.addWidget(self.settingsWorkFolder, 1)
        folder_row.addWidget(self.settingsWorkFolderBrowse, 0)
        folder_row.addWidget(
            self._help_icon(
                "Use a short path like C:\\ple\\work to avoid Windows long-path errors. Click for the install guide.",
                "INSTALL_WINDOWS.md",
            ),
            0,
        )
        folder_wrap = QWidget()
        folder_wrap.setLayout(folder_row)
        folder_card.layout().addWidget(folder_wrap)
        body_layout.addWidget(folder_card)

        # Default course type
        course_card = self._settings_card(
            "Default course mode",
            "What course type is pre-selected on the home page.",
        )
        self.settingsDefaultCourse = QComboBox()
        self.settingsDefaultCourse.addItems(
            [
                "General lecture",
                "Programming language",
                "Digital image processing",
                "AI / machine learning",
                "General lab",
            ]
        )
        course_card.layout().addWidget(
            self._row_with_help(
                self.settingsDefaultCourse,
                "Click for the Teacher Guide — explains what each course mode is for.",
                "TEACHER_GUIDE.md",
            )
        )
        body_layout.addWidget(course_card)

        # Theme
        theme_card = self._settings_card(
            "Theme",
            "Choose Light or Dark. The window updates immediately when you save.",
        )
        self.settingsTheme = QComboBox()
        self.settingsTheme.addItems(["Light", "Dark"])
        theme_card.layout().addWidget(self.settingsTheme)
        body_layout.addWidget(theme_card)

        # Action buttons
        actions = QHBoxLayout()
        actions.addStretch()
        self.settingsResetBtn = QPushButton("Reset to defaults")
        self.settingsResetBtn.setObjectName("secondaryButton")
        self.settingsResetBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settingsResetBtn.setMinimumHeight(36)
        self.settingsSaveBtn = QPushButton("Save settings")
        self.settingsSaveBtn.setObjectName("primaryButton")
        self.settingsSaveBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settingsSaveBtn.setMinimumHeight(36)
        actions.addWidget(self.settingsResetBtn)
        actions.addWidget(self.settingsSaveBtn)
        body_layout.addLayout(actions)

        body_layout.addStretch()
        scroll.setWidget(body)
        outer.addWidget(scroll, 1)

    def _settings_card(self, title_text, subtitle_text):
        card = QFrame()
        card.setObjectName("settingsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 18)
        layout.setSpacing(8)
        title = QLabel(title_text)
        title.setObjectName("panelTitle")
        sub = QLabel(subtitle_text)
        sub.setObjectName("panelBody")
        sub.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(sub)
        return card

    # ------------------------------------------------------------------
    # About page
    # ------------------------------------------------------------------
    def _build_about_page(self):
        self.aboutPage = QWidget()
        self.aboutPage.setObjectName("aboutPage")
        outer = QVBoxLayout(self.aboutPage)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QFrame()
        header.setObjectName("pageHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(36, 24, 36, 18)
        header_layout.setSpacing(4)
        title = QLabel("About PLE")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Version, credits, and project links.")
        subtitle.setObjectName("pageSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        outer.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(36, 16, 36, 24)
        body_layout.setSpacing(20)

        about_card = QFrame()
        about_card.setObjectName("infoPanel")
        about_layout = QHBoxLayout(about_card)
        about_layout.setContentsMargins(24, 22, 24, 22)
        about_layout.setSpacing(22)

        logo = QLabel()
        logo.setFixedSize(96, 96)
        logo.setPixmap(QPixmap(asset_path("ico.png")))
        logo.setScaledContents(True)
        about_layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignTop)

        text_block = QVBoxLayout()
        text_block.setSpacing(6)
        name = QLabel("Portable Learning Environment")
        name.setObjectName("panelTitle")
        version = QLabel("v2026.05 · MIT License")
        version.setObjectName("panelBody")
        description = QLabel(
            "A desktop teaching workspace combining Jupyter, GitHub Classroom, and "
            "guided lesson flow for programming, image processing, AI, and general "
            "computing courses."
        )
        description.setWordWrap(True)
        description.setObjectName("panelBody")

        credits = QLabel(
            "Developed by Haryanto · <a href=\"mailto:haryanto462@gmail.com\">haryanto462@gmail.com</a>"
        )
        credits.setObjectName("panelBody")
        credits.setOpenExternalLinks(True)

        links = QLabel(
            "<a href=\"https://github.com/anto112/portable-learning-environment\">GitHub repository</a> · "
            "<a href=\"https://github.com/anto112/portable-learning-environment/issues\">Report an issue</a> · "
            "<a href=\"https://classroom.github.com\">GitHub Classroom</a>"
        )
        links.setObjectName("panelBody")
        links.setOpenExternalLinks(True)

        text_block.addWidget(name)
        text_block.addWidget(version)
        text_block.addSpacing(8)
        text_block.addWidget(description)
        text_block.addSpacing(8)
        text_block.addWidget(credits)
        text_block.addWidget(links)
        text_block.addStretch()
        about_layout.addLayout(text_block, 1)

        body_layout.addWidget(about_card)
        body_layout.addStretch()
        outer.addWidget(body, 1)

    # ------------------------------------------------------------------
    # Menubar and toolbar
    # ------------------------------------------------------------------
    def _build_menus(self):
        self.menuBar = QMenuBar(self)
        self.menuAssigment = QMenu(self.menuBar)
        self.menuHelp = QMenu(self.menuBar)
        self.menuFile = QMenu(self.menuBar)
        self.menuView = QMenu(self.menuBar)
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
        self.actionViewHome = QAction(self)
        self.actionViewDocs = QAction(self)
        self.actionViewSettings = QAction(self)
        self.actionDocClassroom = QAction(self)
        self.actionDocInstall = QAction(self)

        self.menuAssigment.addAction(self.actionPreflight)
        self.menuAssigment.addAction(self.actionStartLesson)
        self.menuAssigment.addSeparator()
        self.menuAssigment.addAction(self.actionCreate_2)
        self.menuAssigment.addAction(self.actionUpdate_2)

        self.menuView.addAction(self.actionViewHome)
        self.menuView.addAction(self.actionViewDocs)
        self.menuView.addAction(self.actionViewSettings)

        self.menuHelp.addAction(self.actionDocInstall)
        self.menuHelp.addAction(self.actionDocClassroom)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionStuckHelp)
        self.menuHelp.addAction(self.actionHelpJup)
        self.menuHelp.addSeparator()
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
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        # View menu wiring is done here since it only changes the stack page
        self.actionViewHome.triggered.connect(lambda: self.show_page(self.PAGE_HOME))
        self.actionViewDocs.triggered.connect(lambda: self.show_page(self.PAGE_DOCS))
        self.actionViewSettings.triggered.connect(lambda: self.show_page(self.PAGE_SETTINGS))

    def _build_toolbar(self):
        self.back = QAction(QIcon(asset_path("left.png")), "&Back", self)
        self.forward = QAction(QIcon(asset_path("right.png")), "&Forward", self)
        self.reload = QAction(QIcon(asset_path("reload.png")), "&Reload", self)
        self.home = QAction(QIcon(asset_path("home.png")), "&Home", self)
        self.plus = QAction(QIcon(asset_path("plus.png")), "&New Tab", self)
        self.jupyter = QAction(QIcon(asset_path("jupyter.png")), "&Jupyter Notebook", self)
        self.github = QAction(QIcon(asset_path("github_2.png")), "&GitHub", self)
        self.github_class = QAction(
            QIcon(asset_path("github_class_2.png")), "&GitHub Classroom", self
        )

        # Hamburger button to show/hide the sidebar — always reachable.
        self.sidebarToggle = QPushButton("☰")  # ☰
        self.sidebarToggle.setObjectName("sidebarToggle")
        self.sidebarToggle.setFixedSize(34, 30)
        self.sidebarToggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sidebarToggle.setToolTip("Show or hide the sidebar")
        self.sidebarToggle.clicked.connect(self.toggle_sidebar)

        self.urlbar = QLineEdit()
        self.urlbar.setObjectName("urlbar")
        self.urlbar.setPlaceholderText("Enter a URL or local notebook path")
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.toolBar = QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(20, 20))
        self.toolBar.addWidget(self.sidebarToggle)
        self.toolBar.addSeparator()
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

    # ------------------------------------------------------------------
    # Style
    # ------------------------------------------------------------------
    def _apply_style(self, theme="light"):
        """Load the stylesheet for the requested theme from disk.

        Stylesheets live in ple/views/theme/*.qss so they can be edited as
        plain CSS without touching Python. Falls back to light on any
        unrecognised value.
        """
        self.current_theme = "dark" if theme == "dark" else "light"
        self.setStyleSheet(load_stylesheet(self.current_theme))

    # ------------------------------------------------------------------
    # Browser tabs (notebook / web)
    # ------------------------------------------------------------------
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def tab_widget(self):
        self.show_page(self.PAGE_BROWSER)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "quickCards"):
            self.apply_responsive_layout(event.size().width())

    def apply_responsive_layout(self, width):
        # Subtract approximate sidebar width when computing card columns
        content_width = max(width - 220, 480)

        if content_width < 720:
            card_columns = 1
            status_columns = 2
            compact = True
        elif content_width < 1000:
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

        removable = [
            self.lessonTitle,
            self.courseLabel,
            self.deliveryLabel,
            self.courseModeSelect,
            self.deliveryModeSelect,
            self.lessonPreview,
            self.preflightButton,
            self.stuckHelpButton,
        ]
        if hasattr(self, "_courseSelectWrap"):
            removable.extend([self._courseSelectWrap, self._deliverySelectWrap])
        for widget in removable:
            self.lesson_layout.removeWidget(widget)

        # Wrap course/delivery selects with help icons (created lazily, kept reusable)
        if not hasattr(self, "_courseSelectWrap"):
            self._courseSelectWrap = self._row_with_help(
                self.courseModeSelect,
                "Course mode picks the lesson checklist and which packages pre-flight verifies. Open Teacher Guide.",
                "TEACHER_GUIDE.md",
            )
            self._deliverySelectWrap = self._row_with_help(
                self.deliveryModeSelect,
                "Student practice = local Jupyter. Teacher controlled = your JupyterHub. Open Delivery guide.",
                "DELIVERY.md",
            )

        if compact:
            self.lesson_layout.addWidget(self.lessonTitle, 0, 0)
            self.lesson_layout.addWidget(self.courseLabel, 1, 0)
            self.lesson_layout.addWidget(self._courseSelectWrap, 2, 0)
            self.lesson_layout.addWidget(self.deliveryLabel, 3, 0)
            self.lesson_layout.addWidget(self._deliverySelectWrap, 4, 0)
            self.lesson_layout.addWidget(self.lessonPreview, 5, 0)
            self.lesson_layout.addWidget(self.preflightButton, 6, 0)
            self.lesson_layout.addWidget(self.stuckHelpButton, 7, 0)
            self.statusBar().setVisible(False)
        else:
            self.lesson_layout.addWidget(self.lessonTitle, 0, 0, 1, 2)
            self.lesson_layout.addWidget(self.courseLabel, 1, 0)
            self.lesson_layout.addWidget(self.deliveryLabel, 1, 1)
            self.lesson_layout.addWidget(self._courseSelectWrap, 2, 0)
            self.lesson_layout.addWidget(self._deliverySelectWrap, 2, 1)
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
        self.show_page(self.PAGE_HOME)

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
            self.show_page(self.PAGE_HOME)

    # ------------------------------------------------------------------
    # Translation / text
    # ------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Portable Learning Environment")
        )
        self.toolBar.setWindowTitle(_translate("MainWindow", "Navigation"))
        self.menuAssigment.setTitle(_translate("MainWindow", "Assignment"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
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
        self.actionAbout_Us.setText(_translate("MainWindow", "About PLE"))
        self.actionHelpJup.setText(_translate("MainWindow", "Jupyter Notebook docs"))
        self.actionDocInstall.setText(_translate("MainWindow", "Installation guide"))
        self.actionDocClassroom.setText(_translate("MainWindow", "GitHub Classroom setup"))
        self.actionViewHome.setText(_translate("MainWindow", "Home"))
        self.actionViewDocs.setText(_translate("MainWindow", "Documentation"))
        self.actionViewSettings.setText(_translate("MainWindow", "Settings"))
        self.pushButton.setText(_translate("MainWindow", "Open Jupyter Notebook"))
        self.openHubButton.setText(_translate("MainWindow", "Open JupyterHub"))
        self.startLessonButton.setText(_translate("MainWindow", "Start lesson"))
        self.preflightButton.setText(_translate("MainWindow", "Pre-flight check"))
        self.stuckHelpButton.setText(_translate("MainWindow", "Help stuck students"))
        self.label.setText(
            _translate("MainWindow", "Your learning workspace")
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                "Open a notebook on this computer, connect to a JupyterHub server, "
                "or run a guided lesson.",
            )
        )
        self.developerLabel.setText(_translate("MainWindow", "Developed by Haryanto"))

        # ---- Tooltips (hover help). Keep these short — one or two sentences.
        self.pushButton.setToolTip(
            "Start a Jupyter Notebook server on this computer and open it in a new tab.\n"
            "Best for individual practice and learning."
        )
        self.openHubButton.setToolTip(
            "Connect to an institution-hosted JupyterHub.\n"
            "You'll be asked for the hub URL the first time (saved in Settings)."
        )
        self.startLessonButton.setToolTip(
            "Walk through the lesson setup: course type, delivery, assignment URL, work folder, and checklist."
        )
        self.preflightButton.setToolTip(
            "Check Python, Git, Jupyter, packages, and your JupyterHub URL before class starts."
        )
        self.stuckHelpButton.setToolTip(
            "Open the help page for students who get stuck (kernel restart, file not found, etc.)."
        )
        self.courseModeSelect.setToolTip(
            "Course mode adjusts the lesson checklist and which packages the pre-flight check verifies."
        )
        self.deliveryModeSelect.setToolTip(
            "Student practice: PLE starts a local Jupyter server.\n"
            "Teacher controlled: PLE opens your institution's JupyterHub URL."
        )
        for key, label in self.assignmentStatusLabels.items():
            label.setToolTip(self._status_tooltip(key))
        for key, badge in self.statusBarBadges.items():
            badge.setToolTip(self._status_tooltip(key))

        self.sidebarPreflightBtn.setToolTip("Run the pre-flight environment check.")
        self.sidebarStartLessonBtn.setToolTip("Begin a guided lesson flow.")
        self.sidebarOpenJupyterBtn.setToolTip("Open Jupyter (local notebook or JupyterHub).")
        self.navDocsBtn.setToolTip("Browse all documentation inside the app.")
        self.navSettingsBtn.setToolTip("Edit JupyterHub URL, work folder, default course, and theme.")

        self.settingsHubUrl.setToolTip(
            "Full URL ending in /hub/login. Leave blank to use local Jupyter for student practice."
        )
        self.settingsWorkFolder.setToolTip(
            "Where new assignments are cloned by default. Use a short path like C:\\ple\\work to avoid Windows long-path errors."
        )
        self.settingsDefaultCourse.setToolTip(
            "What course type is pre-selected on the home page each time you launch PLE."
        )

        self.urlbar.setToolTip("Enter a URL or local file path and press Enter.")

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

    # ------------------------------------------------------------------
    # Status / preview
    # ------------------------------------------------------------------
    def set_assignment_status(self, statuses, detail=None):
        labels = {
            "cloned": "Cloned",
            "opened": "Opened",
            "submitted": "Submitted",
            "pushed": "Pushed",
        }
        for key, label in self.assignmentStatusLabels.items():
            complete = bool(statuses.get(key, False))
            label.setText(("✓ " if complete else "○ ") + labels[key])
            label.setProperty("complete", complete)
            label.style().unpolish(label)
            label.style().polish(label)
            bar_label = self.statusBarBadges[key]
            bar_label.setText(("✓ " if complete else "○ ") + labels[key])
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

    def _status_tooltip(self, key):
        return {
            "cloned": "Cloned — the assignment repo is on disk in the work folder.",
            "opened": "Opened — the assignment folder was opened in Jupyter at least once.",
            "submitted": "Submitted — you marked the assignment ready to upload.",
            "pushed": "Pushed — Git successfully pushed your work to GitHub.",
        }.get(key, "")

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
