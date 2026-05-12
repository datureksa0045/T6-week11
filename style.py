def app_stylesheet() -> str:
    return """
QMainWindow {
    background: #1F232A;
}
QWidget {
    background: #242A33;
    color: #E8E8E8;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 10pt;
}
QPushButton {
    border-radius: 10px;
    background: #4C90FF;
    color: white;
    padding: 10px 16px;
}
QPushButton:hover {
    background: #6EA7FF;
}
QPushButton:pressed {
    background: #3B74E0;
}
QPushButton#danger {
    background: #E75C5C;
}
QPushButton#danger:hover {
    background: #FF7474;
}
QTableWidget {
    background: #232A33;
    gridline-color: #3B4252;
    alternate-background-color: #2A303B;
}
QHeaderView::section {
    background: #2B3341;
    color: #E8E8E8;
    padding: 8px;
    border: none;
}
QLineEdit, QComboBox, QTextEdit {
    background: #1E242D;
    border: 1px solid #3B4252;
    border-radius: 8px;
    padding: 6px;
    color: #E8E8E8;
}
QTextEdit {
    selection-background-color: #4C90FF;
}
QStatusBar {
    background: #1E232B;
    color: #B0B8C1;
}
QProgressBar {
    border: 1px solid #3B4252;
    border-radius: 8px;
    background: #1E232B;
    color: #E8E8E8;
    text-align: center;
}
QProgressBar::chunk {
    border-radius: 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4C90FF, stop:1 #6EA7FF);
}
QScrollBar:vertical {
    background: #1E232B;
    width: 12px;
    margin: 16px 0 16px 0;
}
QScrollBar::handle:vertical {
    background: #3D4758;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
