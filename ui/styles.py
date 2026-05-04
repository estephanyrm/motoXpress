# ─────────────────────────────────────────────
#  MotoXpress — Estilos globales
# ─────────────────────────────────────────────

# Paleta de colores (tema claro profesional)
WHITE      = "#FFFFFF"
OFF_WHITE  = "#F8F9FB"
PANEL      = "#F1F3F7"
BORDER     = "#DDE1E9"
BORDER2    = "#C8CDD8"
TEXT       = "#1A1D27"
TEXT2      = "#5C6478"
TEXT3      = "#8B92A5"
ACCENT     = "#2563EB"
ACCENT_L   = "#EEF3FD"
ACCENT_H   = "#1D4ED8"
SUCCESS    = "#16A34A"
SUCCESS_L  = "#ECFDF5"
DANGER     = "#DC2626"
DANGER_L   = "#FEF2F2"
WARNING    = "#D97706"
WARNING_L  = "#FFFBEB"
SIDEBAR_BG = "#1A1D27"
SIDEBAR_T  = "#A8B0C4"
SIDEBAR_A  = "#FFFFFF"
SIDEBAR_HV = "#252836"
SIDEBAR_SEL= "#2A2F42"

FONT_FAMILY = "'Segoe UI', 'SF Pro Display', 'Ubuntu', 'Helvetica Neue', sans-serif"

STYLE_GLOBAL = f"""
QWidget {{
    background-color: {OFF_WHITE};
    color: {TEXT};
    font-family: {FONT_FAMILY};
    font-size: 14px;
}}
QScrollBar:vertical {{
    background: {PANEL};
    width: 6px;
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER2};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {PANEL};
    height: 6px;
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
    padding: 6px 10px;
    font-size: 12px;
    border-radius: 4px;
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
    border-radius: 7px;
    padding: 9px 13px;
    color: {TEXT};
    font-size: 14px;
    selection-background-color: {ACCENT_L};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {ACCENT};
    background: {WHITE};
}}
QLineEdit:read-only {{
    color: {TEXT2};
    background: {PANEL};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0; height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {TEXT2};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 7px;
    selection-background-color: {ACCENT_L};
    color: {TEXT};
    outline: none;
    padding: 4px;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 14px;
    min-height: 30px;
    border-radius: 4px;
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
    border-radius: 7px;
    padding: 9px 13px;
    color: {TEXT};
    font-size: 14px;
}}
"""

STYLE_TABLE = f"""
QTableWidget {{
    background: {WHITE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    gridline-color: {PANEL};
    color: {TEXT};
    font-size: 13px;
    outline: none;
    selection-background-color: {ACCENT_L};
}}
QHeaderView::section {{
    background: {PANEL};
    color: {TEXT2};
    border: none;
    border-bottom: 1.5px solid {BORDER};
    border-right: 1px solid {BORDER};
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}}
QHeaderView::section:last {{
    border-right: none;
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {PANEL};
    color: {TEXT};
}}
QTableWidget::item:selected {{
    background: {ACCENT_L};
    color: {ACCENT};
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
    spacing: 8px;
    background: transparent;
    border: none;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
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
}}
"""

def card_style(radius=10, shadow=False):
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
            border-radius: 7px;
            padding: 9px 20px;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.2px;
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
            border-radius: 7px;
            padding: 9px 18px;
            font-size: 13px;
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
            border-radius: 7px;
            padding: 9px 18px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: #FEE2E2;
        }}
    """

def btn_success():
    return f"""
        QPushButton {{
            background-color: {SUCCESS};
            color: #FFFFFF;
            border: none;
            border-radius: 7px;
            padding: 9px 20px;
            font-weight: 600;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: #15803D;
        }}
    """

SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background: {SIDEBAR_BG};
    border-right: none;
}}
"""
