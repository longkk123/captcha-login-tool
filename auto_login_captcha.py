
import time
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import cv2

# Cấu hình đường dẫn tới Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Thông tin đăng nhập
username = "your_username"
password = "your_password"
server_name = "1"

# Khởi chạy trình duyệt
driver = webdriver.Chrome()
driver.get("https://hoisinhngocrong.com")

# Điền thông tin cơ bản
driver.find_element(By.XPATH, '//input[@placeholder="Tên đăng nhập"]').send_keys(username)
driver.find_element(By.XPATH, '//input[@placeholder="Mật khẩu"]').send_keys(password)
driver.find_element(By.XPATH, '//select').send_keys(server_name)

# Chụp toàn trang để cắt captcha
driver.save_screenshot("fullpage.png")

# Lấy vị trí captcha
captcha_element = driver.find_element(By.XPATH, '//img[contains(@src,"captcha")]')
location = captcha_element.location
size = captcha_element.size
x = int(location['x'])
y = int(location['y'])
w = int(size['width'])
h = int(size['height'])

# Cắt ảnh captcha
full_img = Image.open("fullpage.png")
captcha_img = full_img.crop((x, y, x + w, y + h))
captcha_img.save("captcha.png")

# Tiền xử lý ảnh và đọc ký tự
img = cv2.imread("captcha.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
cv2.imwrite("captcha_clean.png", thresh)

captcha_text = pytesseract.image_to_string(thresh, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
captcha_text = captcha_text.strip().replace(" ", "")
print("Captcha đọc được:", captcha_text)

# Điền captcha và đăng nhập
driver.find_element(By.XPATH, '//input[@placeholder="Captcha"]').send_keys(captcha_text)
driver.find_element(By.XPATH, '//button[contains(text(), "Đăng Nhập")]').click()

time.sleep(5)
driver.quit()
