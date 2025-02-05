from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QTextEdit, QHBoxLayout, QMenuBar,
                             QMenu, QStatusBar, QFileDialog, QMessageBox)
from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon
import sys

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super(MarkdownEditor, self).__init__()
        
        self.window_width, self.window_height = 700, 500
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowIcon(QIcon("thoughForge.ico"))
        self.setWindowTitle("Untitled - ThoughtForge")
        self.setStyleSheet("""
                            QWidget {
                                font-size: 18px;
                            }
                           """)
        
        self.main_window = QWidget()
        self.layout = QHBoxLayout(self.main_window)
        self.setCentralWidget(self.main_window)
        
        # Track the current file path
        self.current_file_path = None
        
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
        self.actionEditor_Only.setShortcut("Ctrl+1")
        # View -> Viewer Only
        self.actionViewer_Only = QAction(self)
        self.actionViewer_Only.setText("Viewer Only")
        self.actionViewer_Only.setStatusTip("Viewer Only")
        self.actionViewer_Only.setShortcut("Ctrl+2")
        # View -> Split View
        self.actionSplit_View = QAction(self)
        self.actionSplit_View.setText("Split View")
        self.actionSplit_View.setStatusTip("Vertical Split Between Editor and Viewer")
        self.actionSplit_View.setShortcut("Ctrl+3")
        # Adding Actions to View menu
        self.menuView.addAction(self.actionEditor_Only)
        self.menuView.addAction(self.actionViewer_Only)
        self.menuView.addAction(self.actionSplit_View)
        
        # Edit menu in menu bar
        self.menuEdit = QMenu(self.menu_bar)
        self.menuEdit.setTitle("Edit")
        # Edit -> Undo
        self.actionUndo = QAction(self)
        self.actionUndo.setText("Undo")
        self.actionUndo.setShortcut("Ctrl+Z")
        # Edit -> Redo
        self.actionRedo = QAction(self)
        self.actionRedo.setText("Redo")
        self.actionRedo.setShortcut("Ctrl+Shift+Z")
        # Edit -> Cut
        self.actionCut = QAction(self)
        self.actionCut.setText("Cut")
        self.actionCut.setShortcut("Ctrl+X")
        # Edit -> Copy
        self.actionCopy = QAction(self)
        self.actionCopy.setText("Copy")
        self.actionCopy.setShortcut("Ctrl+C")
        # Edit -> Paste
        self.actionPaste = QAction(self)
        self.actionPaste.setText("Paste")
        self.actionPaste.setShortcut("Ctrl+V")
        # Edit -> Select All
        self.actionSelectAll = QAction(self)
        self.actionSelectAll.setText("Select All")
        self.actionSelectAll.setShortcut("Ctrl+A")
        # Adding Actions to Edit menu
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSelectAll)
        
        # Adding menus to the menu bar
        self.menu_bar.addAction(self.menuFile.menuAction())
        self.menu_bar.addAction(self.menuEdit.menuAction())
        self.menu_bar.addAction(self.menuView.menuAction())
        
        
    def init_config_signals(self):
        self.md_editor.textChanged.connect(self.markdown_update)
        
        self.actionNew.triggered.connect(self.new_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_as_file)
        self.actionOpen.triggered.connect(self.open_file)
        
        self.actionUndo.triggered.connect(self.md_editor.undo)
        self.actionRedo.triggered.connect(self.md_editor.redo)
        self.actionCut.triggered.connect(self.md_editor.cut)
        self.actionCopy.triggered.connect(self.md_editor.copy)
        self.actionPaste.triggered.connect(self.md_editor.paste)
        self.actionSelectAll.triggered.connect(self.md_editor.selectAll)
        
        self.actionEditor_Only.triggered.connect(self.show_editor_only)
        self.actionViewer_Only.triggered.connect(self.show_viewer_only)
        self.actionSplit_View.triggered.connect(self.show_split_view)
        
    def markdown_update(self):
        self.md_viewer.setMarkdown(self.md_editor.toPlainText())
        
    def new_file(self):
        # Clear the editor and viewer
        self.md_editor.clear()
        self.md_viewer.clear()
        
        # Reset the file path and window title
        self.current_file_path = None
        self.setWindowTitle("Untitled - ThoughtForge")
        
    def save_file(self):
        if self.current_file_path:
            # Save to the existing file
            try:
                with open(self.current_file_path, "w", encoding="utf-8") as file:
                    file.write(self.md_editor.toPlainText())
                self.statusbar.showMessage(f"File saved: {self.current_file_path}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        else:
            # If no file path, use "Save As"
            self.save_as_file()
        
    def save_as_file(self):
        # Open a file dialog to get the file name
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            "",  # Start in the current directory
            "Markdown Files (*.md);;All Files (*)"  # Filter for .md files
        )
        
        if fileName:
            # Ensure the file has a .md extension
            if not fileName.endswith(".md"):
                fileName += ".md"
            
            try:
                # Write the content of md_editor to the file
                with open(fileName, "w", encoding="utf-8") as file:
                    file.write(self.md_editor.toPlainText())
                
                # Update the current file path and window title
                self.current_file_path = fileName
                self.setWindowTitle(f"{fileName} - ThoughtForge")
                self.statusbar.showMessage(f"File saved successfully: {fileName}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        
    def open_file(self):
        # Open a file dialog to select a file
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",  # Start in the current directory
            "Markdown Files (*.md);;All Files (*)"  # Filter for .md files
        )
        
        if fileName:
            try:
                # Read the content of the file
                with open(fileName, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Load the content into the editor
                self.md_editor.setPlainText(content)
                
                # Update the current file path and window title
                self.current_file_path = fileName
                self.setWindowTitle(f"{fileName} - ThoughtForge")
                self.statusbar.showMessage(f"File opened: {fileName}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
                
    def show_editor_only(self):
        self.md_editor.show()
        self.md_viewer.hide()
        
    def show_viewer_only(self):
        self.md_editor.hide()
        self.md_viewer.show()
        
    def show_split_view(self):
        self.md_editor.show()
        self.md_viewer.show()
        
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