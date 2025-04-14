from gui import App
import time

app = App()
app.show_image("test_images/grass1.png")
time.sleep(5)
app.show_image("test_images/grass2.png")
app.show_info("Test")
app.run()