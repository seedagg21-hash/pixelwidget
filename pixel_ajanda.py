import sys
import os
import locale
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QCheckBox, QScrollArea, 
                             QLineEdit, QFrame)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QSize, QLocale
from PyQt6.QtGui import QMovie, QFont, QPixmap, QPainter, QPen, QColor, QImage

# Türkçe gün isimleri için yerel ayar (Sistemin Türkçeyse otomatik alır ama garanti olsun)
try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
except:
    pass

class PixelAjanda(QWidget):
    def __init__(self):
        super().__init__()

        # --- AYARLAR ---
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 560) # Gün ismi sığsın diye biraz uzattık

        # RENKLER
        self.bg_color = "#f9d5e5"      # Ana Pembe
        self.border_color = "#8b4b62"  # Koyu Çizgiler
        self.text_color = "#8b4b62"

        # Otomatik Pixel Grafikleri Oluştur
        self.create_tick_icon()
        self.create_pixel_skin() # Çerçeve resmi oluşturuluyor

        self.init_ui()

    def create_tick_icon(self):
        """Tik işaretini (✓) oluşturur."""
        size = 14
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(QColor(self.border_color))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(2, 7, 5, 11)
        painter.drawLine(5, 11, 12, 3)
        painter.end()
        pixmap.save("tik.png")

    def create_pixel_skin(self):
        """
        Köşeleri yumuşatılmış, ortası şeffaf bir pixel çerçeve (skin) oluşturur.
        Bu resmi hem ana pencerede hem de kutucuklarda kullanacağız.
        """
        s = 24 
        img = QImage(s, s, QImage.Format.Format_ARGB32)
        img.fill(QColor(0,0,0,0)) # Tamamen şeffaf zemin
        
        painter = QPainter(img)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) 
        
        c_border = QColor(self.border_color)
        painter.setBrush(c_border)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # --- PİXEL ÇERÇEVE ÇİZİMİ ---
        # Üst, Alt, Sol, Sağ kenarlar
        painter.drawRect(4, 0, 16, 4) 
        painter.drawRect(4, 20, 16, 4)
        painter.drawRect(0, 4, 4, 16) 
        painter.drawRect(20, 4, 4, 16)
        
        # Köşeler (Nokta nokta merdiven etkisi)
        painter.drawRect(2, 2, 2, 2)   # Sol Üst
        painter.drawRect(20, 2, 2, 2)  # Sağ Üst
        painter.drawRect(2, 20, 2, 2)  # Sol Alt
        painter.drawRect(20, 20, 2, 2) # Sağ Alt
        
        painter.end()
        img.save("pixel_frame.png")

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # --- ANA GÖVDE (Pembe Arka Plan + Pixel Çerçeve) ---
        self.container = QFrame()
        self.container.setObjectName("MainFrame")
        self.container.setStyleSheet(f"""
            QFrame#MainFrame {{
                background-color: {self.bg_color}; /* Pembe zemin */
                border-image: url(pixel_frame.png) 8 fill; 
                border-width: 8px;
            }}
        """)
        
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # --- ÜST KISIM ---
        self.header_layout = QHBoxLayout()
        
        # Kedi
        self.cat_label = QLabel()
        self.movie = QMovie("kedi.gif")
        self.movie.setScaledSize(QSize(60, 60))
        self.cat_label.setMovie(self.movie)
        self.movie.start()
        self.header_layout.addWidget(self.cat_label)

        # Saat ve Tarih
        self.time_vbox = QVBoxLayout()
        self.time_vbox.setSpacing(2) # Satırlar arası boşluğu kıstık
        
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Press Start 2P", 18))
        self.time_label.setStyleSheet(f"color: {self.text_color}; border: none; background: transparent;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Press Start 2P", 9))
        self.date_label.setStyleSheet(f"color: {self.text_color}; border: none; background: transparent;")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.time_vbox.addWidget(self.time_label)
        self.time_vbox.addWidget(self.date_label)
        self.header_layout.addLayout(self.time_vbox)

        # Kapat Butonu
        self.close_btn = QPushButton("x")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #e9a9c4;
                border: 2px solid {self.border_color};
                color: {self.border_color};
                font-family: 'Press Start 2P';
                font-size: 10px;
                margin-top: 5px;
            }}
            QPushButton:hover {{ background-color: #ff69b4; color: white; }}
        """)
        self.header_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.header_layout)

        # --- BAŞLIK ---
        self.todo_head = QLabel("⊹ TO-DO LIST ⊹")
        self.todo_head.setFont(QFont("Press Start 2P", 8))
        self.todo_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.todo_head.setStyleSheet(f"""
            color: white; 
            background: {self.border_color}; 
            padding: 8px; 
            margin-top: 5px;
            border: 2px solid {self.border_color};
        """)
        self.layout.addWidget(self.todo_head)

        # --- LİSTE ALANI (Buna da Pixel Çerçeve Ekledik) ---
        # ScrollArea'yı bir Frame içine alıyoruz ki çerçeve düzgün dursun
        self.list_container = QFrame()
        self.list_container.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.6); /* Hafif şeffaf beyaz */
                border-image: url(pixel_frame.png) 8 fill; 
                border-width: 8px;
            }}
        """)
        self.list_layout_wrap = QVBoxLayout(self.list_container)
        self.list_layout_wrap.setContentsMargins(5, 5, 5, 5) # Çerçevenin içine pay

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        # ScrollArea'nın kendi kenarlığını kapatıyoruz, dıştaki Frame'i kullanacağız
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        
        self.list_layout_wrap.addWidget(self.scroll)
        self.layout.addWidget(self.list_container)

        # --- GİRİŞ KUTUSU (Pixel Çerçeveli) ---
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Yeni görev...")
        self.task_input.setFont(QFont("Press Start 2P", 7))
        self.task_input.returnPressed.connect(self.add_task)
        self.task_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url(pixel_frame.png) 8 fill; 
                border-width: 8px;
                padding: 5px 10px; /* Yazı çerçeveye yapışmasın diye */
                background-color: white; 
                color: #333;
            }}
        """)
        self.layout.addWidget(self.task_input)

        self.main_layout.addWidget(self.container)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        # Saat
        current_time = QTime.currentTime().toString("HH:mm")
        
        # Tarih (Örn: 26 NOV 2024)
        date_text = QDate.currentDate().toString("dd MMM yyyy").upper()
        
        # Gün İsmi (Örn: PAZARTESİ) - Türkçe locale ayarına göre gelir
        day_text = QDate.currentDate().toString("dddd").upper()
        
        self.time_label.setText(current_time)
        # Tarih ve Günü alt alta yazdırıyoruz
        self.date_label.setText(f"{date_text}\n{day_text}")

    def add_task(self):
        text = self.task_input.text().strip()
        if text:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 4, 0, 4)
            
            check = QCheckBox(text)
            check.setFont(QFont("Press Start 2P", 7))
            
            # TİK İŞARETİ AYARLARI
            check.setStyleSheet(f"""
                QCheckBox {{ color: {self.text_color}; spacing: 12px; }}
                QCheckBox::indicator {{ 
                    width: 18px; height: 18px; 
                    border: 3px solid {self.border_color}; 
                    background-color: white; 
                }}
                QCheckBox::indicator:checked {{ 
                    image: url(tik.png);
                    background-color: white;
                    border: 3px solid {self.border_color};
                }}
                QCheckBox:checked {{ color: #d8a0b5; text-decoration: line-through; }}
            """)
            
            del_btn = QPushButton("x")
            del_btn.setFixedSize(20, 20)
            del_btn.setStyleSheet(f"""
                QPushButton {{ color: {self.border_color}; border: none; background: transparent; font-weight: bold; font-family: 'Press Start 2P'; }}
                QPushButton:hover {{ color: red; }}
            """)
            del_btn.clicked.connect(lambda: row.deleteLater())

            row_layout.addWidget(check)
            row_layout.addStretch()
            row_layout.addWidget(del_btn)
            
            self.scroll_layout.addWidget(row)
            self.task_input.clear()

    # Sürükleme
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PixelAjanda()
    ex.show()
    sys.exit(app.exec())