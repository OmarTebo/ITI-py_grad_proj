from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QHBoxLayout
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
        self.md_editor = QTextEdit()
        self.md_viewer = QTextEdit(readOnly=True)
        
        self.layout.addWidget(self.md_editor)
        self.layout.addWidget(self.md_viewer)
        
    def init_config_signals(self):
        self.md_editor.textChanged.connect(self.markdown_update)
        
    def markdown_update(self):
        self.md_viewer.setMarkdown(self.md_editor.toPlainText())
        
        
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
