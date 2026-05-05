WHITE      = "#FFFFFF"
OFF_WHITE  = "#F7F8FA"
PANEL      = "#EEF0F5"
BORDER     = "#E2E6EF"
BORDER2    = "#C9CEDB"
TEXT       = "#111827"
TEXT2      = "#4B5563"
TEXT3      = "#9CA3AF"

ACCENT     = "#2563EB"
ACCENT_L   = "#EFF6FF"
ACCENT_H   = "#1D4ED8"
ACCENT_XL  = "#DBEAFE"

SUCCESS    = "#059669"
SUCCESS_L  = "#ECFDF5"
DANGER     = "#DC2626"
DANGER_L   = "#FEF2F2"
WARNING    = "#D97706"
WARNING_L  = "#FFFBEB"

SIDEBAR_BG  = "#111827"
SIDEBAR_T   = "#9CA3AF"
SIDEBAR_A   = "#FFFFFF"
SIDEBAR_HV  = "#1F2937"
SIDEBAR_SEL = "#1E3A5F"
SIDEBAR_ACC = "#3B82F6"

FONT_FAMILY = "'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Ubuntu', sans-serif"

STYLE_GLOBAL = f"""
QWidget {{
    background-color: {OFF_WHITE};
    color: {TEXT};
    font-family: {FONT_FAMILY};
    font-size: 14px;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 5px;
    border-radius: 3px;
    margin: 4px 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER2};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 5px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER2};
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QToolTip {{
    background: {TEXT};
    color: {WHITE};
    border: none;
    padding: 6px 12px;
    font-size: 12px;
    border-radius: 5px;
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    width: 0; height: 0; border: none;
}}
"""

STYLE_INPUT = f"""
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 9px 13px;
    color: {TEXT};
    font-size: 13px;
    font-family: {FONT_FAMILY};
    selection-background-color: {ACCENT_XL};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {ACCENT};
    background: {WHITE};
    outline: none;
}}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {BORDER2};
}}
QLineEdit:read-only {{
    color: {TEXT2};
    background: {PANEL};
}}
QComboBox::drop-down {{
    border: none;
    width: 32px;
    border-left: 1px solid {BORDER};
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background: transparent;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0; height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {TEXT2};
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    selection-background-color: {ACCENT_L};
    color: {TEXT};
    outline: none;
    padding: 4px;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 14px;
    min-height: 32px;
    border-radius: 5px;
}}
QComboBox QAbstractItemView::item:selected {{
    background: {ACCENT_L};
    color: {ACCENT};
}}
"""

STYLE_INPUT_ERROR = f"""
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {DANGER_L};
    border: 1.5px solid {DANGER};
    border-radius: 8px;
    padding: 9px 13px;
    color: {TEXT};
    font-size: 13px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {DANGER};
}}
"""

STYLE_TABLE = f"""
QTableWidget {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 10px;
    gridline-color: {OFF_WHITE};
    color: {TEXT};
    font-size: 13px;
    outline: none;
    selection-background-color: {ACCENT_L};
    alternate-background-color: {OFF_WHITE};
}}
QHeaderView {{
    background: {PANEL};
}}
QHeaderView::section {{
    background: {PANEL};
    color: {TEXT3};
    border: none;
    border-bottom: 1.5px solid {BORDER};
    border-right: 1px solid {BORDER};
    padding: 10px 16px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-family: {FONT_FAMILY};
}}
QHeaderView::section:last {{
    border-right: none;
}}
QTableWidget::item {{
    padding: 11px 16px;
    border-bottom: 1px solid {OFF_WHITE};
    color: {TEXT};
}}
QTableWidget::item:selected {{
    background: {ACCENT_L};
    color: {ACCENT};
}}
QTableWidget::item:hover {{
    background: {OFF_WHITE};
}}
QTableCornerButton::section {{
    background: {PANEL};
    border: none;
}}
"""

STYLE_CHECKBOX = f"""
QCheckBox {{
    color: {TEXT};
    font-size: 13px;
    spacing: 9px;
    background: transparent;
    border: none;
    font-family: {FONT_FAMILY};
}}
QCheckBox::indicator {{
    width: 17px;
    height: 17px;
    border: 1.5px solid {BORDER2};
    border-radius: 5px;
    background: {WHITE};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
}}
QCheckBox::indicator:hover {{
    border-color: {ACCENT};
    background: {ACCENT_L};
}}
"""

SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background: {SIDEBAR_BG};
    border: none;
}}
"""

def card_style(radius=10):
    return f"""
        QFrame {{
            background-color: {WHITE};
            border: 1.5px solid {BORDER};
            border-radius: {radius}px;
        }}
    """

def btn_primary():
    return f"""
        QPushButton {{
            background-color: {ACCENT};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 9px 22px;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.2px;
            font-family: {FONT_FAMILY};
        }}
        QPushButton:hover {{
            background-color: {ACCENT_H};
        }}
        QPushButton:pressed {{
            background-color: #1E40AF;
        }}
        QPushButton:disabled {{
            background-color: {BORDER};
            color: {TEXT3};
        }}
    """

def btn_secondary():
    return f"""
        QPushButton {{
            background-color: {WHITE};
            color: {TEXT2};
            border: 1.5px solid {BORDER};
            border-radius: 8px;
            padding: 9px 20px;
            font-size: 13px;
            font-family: {FONT_FAMILY};
        }}
        QPushButton:hover {{
            background-color: {PANEL};
            color: {TEXT};
            border-color: {BORDER2};
        }}
        QPushButton:pressed {{
            background-color: {BORDER};
        }}
    """

def btn_danger():
    return f"""
        QPushButton {{
            background-color: {DANGER_L};
            color: {DANGER};
            border: 1.5px solid #FCA5A5;
            border-radius: 8px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
            font-family: {FONT_FAMILY};
        }}
        QPushButton:hover {{
            background-color: #FEE2E2;
            border-color: {DANGER};
        }}
    """

def btn_success():
    return f"""
        QPushButton {{
            background-color: {SUCCESS};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 9px 22px;
            font-weight: 600;
            font-size: 13px;
            font-family: {FONT_FAMILY};
        }}
        QPushButton:hover {{
            background-color: #047857;
        }}
    """

def btn_ghost():
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {ACCENT};
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_L};
        }}
    """
