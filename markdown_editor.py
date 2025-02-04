from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QHBoxLayout, QMenuBar, QMenu, QStatusBar
from PyQt6 import QtCore
from PyQt6.QtGui import QAction
import sys

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super(MarkdownEditor, self).__init__()
        
        self.window_width, self.window_height = 700, 500
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle("My Journal App")
        self.setStyleSheet("""
                            QWidget {
                                font-size: 18px;
                            }
                           """)
        
        self.main_window = QWidget()
        self.layout = QHBoxLayout(self.main_window)
        self.setCentralWidget(self.main_window)
        
        self.init_ui()
        self.init_config_signals()
        
    def init_ui(self):
        # Editor And Viewer
        self.md_editor = QTextEdit()
        self.md_viewer = QTextEdit(readOnly=True)
        
        self.layout.addWidget(self.md_editor)
        self.layout.addWidget(self.md_viewer)
        
        # Menu Bar and its subs
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 700, 18))
        self.menu_bar.setStyleSheet("""
                                        QWidget {
                                            font-size: 9pt
                                        }
                                    """)
        self.setMenuBar(self.menu_bar)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.setStyleSheet("""
                                        QWidget {
                                            font-size: 9pt
                                        }
                                    """)
        # File menu in menu bar
        self.menuFile = QMenu(self.menu_bar)
        self.menuFile.setTitle("File")
        # File -> New
        self.actionNew = QAction(self)
        self.actionNew.setText("New")
        self.actionNew.setStatusTip("Create a new entry")
        self.actionNew.setShortcut("Ctrl+N")
        # File -> Open
        self.actionOpen = QAction(self)
        self.actionOpen.setText("Open")
        self.actionOpen.setStatusTip("Open an existing entry")
        self.actionOpen.setShortcut("Ctrl+O")
        # File -> Save
        self.actionSave = QAction(self)
        self.actionSave.setText("Save")
        self.actionSave.setStatusTip("Save entry")
        self.actionSave.setShortcut("Ctrl+S")
        # File -> Save As
        self.actionSave_As = QAction(self)
        self.actionSave_As.setText("Save As")
        self.actionSave_As.setStatusTip("Save entry as...")
        self.actionSave_As.setShortcut("Ctrl+Shift+S")
        # Adding Actions to File menu
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        
        # View menu in menu bar
        self.menuView = QMenu(self.menu_bar)
        self.menuView.setTitle("View")
        # View -> Editor Only
        self.actionEditor_Only = QAction(self)
        self.actionEditor_Only.setText("Editor Only")
        self.actionEditor_Only.setStatusTip("View Editor Only")
        # View -> Viewer Only
        self.actionViewer_Only = QAction(self)
        self.actionViewer_Only.setText("Viewer Only")
        self.actionViewer_Only.setStatusTip("Viewer Only")
        # View -> Split View
        self.actionSplit_View = QAction(self)
        self.actionSplit_View.setText("Split View")
        self.actionSplit_View.setStatusTip("Vertical Split Between Editor and Viewer")
        # Adding Actions to View menu
        self.menuView.addAction(self.actionEditor_Only)
        self.menuView.addAction(self.actionViewer_Only)
        self.menuView.addAction(self.actionSplit_View)
        
        # Adding menus to the menu bar
        self.menu_bar.addAction(self.menuFile.menuAction())
        self.menu_bar.addAction(self.menuView.menuAction())
        
        
    def init_config_signals(self):
        self.md_editor.textChanged.connect(self.markdown_update)
        self.actionNew.triggered.connect(self.new_file)
        
    def markdown_update(self):
        self.md_viewer.setMarkdown(self.md_editor.toPlainText())
        
    def new_file(self):
        print("New was clicked")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
                        QWidget {
                            font-size: 14px;
                        }
                      """)
    win = MarkdownEditor()
    win.show()
    sys.exit(app.exec())