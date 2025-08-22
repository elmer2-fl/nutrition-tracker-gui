DARK_STYLE = """
    QWidget {
        background-color: #121212;
        color: #e0e0e0;
        font-family: Arial;
        font-size: 28px; /* scaled 200% */
    }
    QLabel {
        font-size: 22px;
        color: #e0e0e0;
    }
    QLineEdit, QComboBox {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 8px;
        font-size: 22px;
    }
    QPushButton {
        background-color: #333;
        border-radius: 8px;
        padding: 12px;
        font-size: 24px;
    }
    QPushButton:hover {
        background-color: #444;
    }
    QSlider::groove:horizontal {
        height: 12px;
        background: #333;
        border-radius: 6px;
    }
    QSlider::handle:horizontal {
        background: #e0e0e0;
        border: 1px solid #666;
        width: 20px;
        margin: -4px 0;
        border-radius: 10px;
    }
"""

LIGHT_STYLE = """
    QWidget {
        background-color: #f5f5f5;
        color: #222;
        font-family: Arial;
        font-size: 28px; /* scaled 200% */
    }
    QLabel {
        font-size: 22px;
        color: #222;
    }
    QLineEdit, QComboBox {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 8px;
        font-size: 22px;
    }
    QPushButton {
        background-color: #ddd;
        border-radius: 8px;
        padding: 12px;
        font-size: 24px;
    }
    QPushButton:hover {
        background-color: #bbb;
    }
    QSlider::groove:horizontal {
        height: 12px;
        background: #ccc;
        border-radius: 6px;
    }
    QSlider::handle:horizontal {
        background: #333;
        border: 1px solid #666;
        width: 20px;
        margin: -4px 0;
        border-radius: 10px;
    }
"""
