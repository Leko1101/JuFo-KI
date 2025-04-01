from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QGuiApplication, QPalette, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer

import os


try:
    current_image_name = os.listdir("images")[0]
except:
    current_image_name = None
count = 0
bottom_label = None

def create_main_window() -> QWidget:
    window = QWidget()
    window.setWindowTitle("JuFo KI GUI")
    screen = QGuiApplication.primaryScreen() 
    size = screen.availableSize()
    window.resize(size.width(), size.height())
    
    palette = window.palette()
    palette.setColor(window.backgroundRole(), QColor("gray"))
    window.setPalette(palette)
    
    return window

def create_text_bar(text: str, text_color: QColor, text_font: str, text_size: int, background_color: QColor, bar_size: int, alignment: Qt.AlignmentFlag) -> QWidget:
    bar = QWidget()
    bar.setFixedHeight(bar_size)
    bar.setAutoFillBackground(True)
    palette = bar.palette()
    palette.setColor(bar.backgroundRole(), background_color)
    bar.setPalette(palette)
    
    text_label = QLabel(text)
    
    text_palette = text_label.palette()
    text_palette.setColor(text_label.foregroundRole(), text_color)
    text_label.setPalette(text_palette)
    
    font = QFont(text_font, text_size)
    text_label.setFont(font)
    
    layout = QHBoxLayout(bar)
    layout.addWidget(text_label)
    layout.setAlignment(alignment)
    
    return bar, text_label

def create_main_layout(window: QWidget, content: list) -> QWidget:
    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    
    for item in content:
        main_layout.addWidget(item)
    
    return main_layout

def create_image_widget() -> QLabel:
    global current_image_name, image_label
    image_label = QLabel(window)
    image_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    if current_image_name != None:
        pixmap = QPixmap(f"images/" + current_image_name)
        image_label.setPixmap(pixmap)
    return image_label


def move_images(exception: str) -> None:
    for file in os.listdir("images"):
        if not file == exception:
            os.rename(f"images/{file}", f"old_images/{file}")

def update_image_if_needed():
    global current_image_name, image_label, count, bottom_label
    
    if len(os.listdir("images")) > 0:
        for image_name in os.listdir("images"):
            if image_name != current_image_name:
                current_image_name = image_name
                count = count + 1
                bottom_label.setText(f"Running [Iteration: {count}]")
                break
        
        move_images(current_image_name)
        
        pixmap = QPixmap("images/"+current_image_name)
        image_label.setPixmap(pixmap)

def run() -> None:
    global window, bottom_label
    app = QApplication([])
    
    if not os.path.exists("old_images"):
        os.makedirs("old_images")
    
    window = create_main_window()
    top_bar, top_label = create_text_bar("JuFo KI", QColor("white"), "Arial", 12, QColor("#393939"), 40, Qt.AlignmentFlag.AlignLeft)
    bottom_bar, bottom_label = create_text_bar(f"Running [Iteration: {count}]", QColor("white"), "Arial", 14, QColor("#393939"), 40, Qt.AlignmentFlag.AlignCenter)
    image = create_image_widget()
    main_layout = create_main_layout(window, [top_bar, image, bottom_bar])
    
    timer = QTimer()
    timer.timeout.connect(update_image_if_needed)
    timer.start(10)
    
    window.show()
    app.exec()

if __name__ == "__main__":
    run()