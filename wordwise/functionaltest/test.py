from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from wordbank.models import wordBank
import time

class HangmanGameTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_hangman_game_flow(self):
        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)
        # สร้าง database จำลอง 
        wordBank.objects.create(word="BED", meaning="A piece of furniture for sleeping on")

        # ปาร์คกดเข้าลิงค์ Hangman game จากหน้าเมนู 
        time.sleep(1)
        hangman_link = self.driver.find_element(By.LINK_TEXT, "Hangman Game")
        hangman_link.click()

        # รอจนกว่าจะสร้างมีกล่อง class word 
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'word'))
        )
        
        # ปาร์คสังเกตเห็นว่ามีเส้นประ 3 เส้น มีปุ่มที่มีคำว่า Guess และ มีเห็นคำว่า Guessed Letters: None"
        label = self.driver.find_element(By.CSS_SELECTOR, "label[for='letter']")
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        word_display = self.driver.find_element(By.CLASS_NAME, 'word')
        guess_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertTrue(len(word_display.text.split()) == 3)  # 3-letter word
        self.assertTrue(word_display.text == "_ _ _")
        self.assertEqual(label.text, "Enter a letter:")  # ตรวจสอบข้อความใน label
        self.assertEqual(guessed_letters ,"Guessed Letters: None")
        self.assertIn("Guess",guess_button.text)

        # คำใบ้จาก database มาเทียบกับหน้า web ว่าตรงกันมั้ย
        word_obj = wordBank.objects.get(word="BED")
        expected_hint = word_obj.meaning
        hint = self.driver.find_element(By.CSS_SELECTOR, ".meaning").text
        self.assertEqual("Hint: "+expected_hint, hint)

        # ปาร์คใส่ตัวอักษร A และกดปุ่ม Guess
        input_field = self.driver.find_element(By.NAME, "letter")
        guess_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(1)
        input_field.send_keys("A")
        time.sleep(1)
        guess_button.click()

        # ปาร์คเห็นว่า Guessed Letters: จาก None กลายเป็น A และAttempts Left: เหลือ 5 
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text
        self.assertEqual("Guessed Letters: A", guessed_letters)
        self.assertEqual("Attempts Left: 5", attempts_left)
        time.sleep(1)

        # รอจนกว่า input field สำหรับกรอกตัวอักษรจะพร้อมใช้งานอีกครั้ง
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 

        # ส่ปาร์คใส่ตัวอักษร E และกดปุ่ม Guess
        input_field.send_keys("E")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        time.sleep(1)          
        guess_button.click()
        word_display = self.driver.find_element(By.CLASS_NAME, 'word')
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text
        self.assertEqual("Guessed Letters: A E", guessed_letters)
        self.assertEqual("Attempts Left: 5", attempts_left)
        self.assertTrue(word_display.text == "_ E _")
        
        # ตัวอักษรที่ต้องการเดาต่อให้ครบคำว่า "BED"
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        # ปาร์คใส่ตัว B 
        input_field.send_keys("B")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        # ปาร์คใส่ตัว D 
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("D")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        time.sleep(1)
        # ปาร์คเห็นข้อความ 🎉 Congratulations! You won! 🎉
        message =  self.driver.find_element(By.CLASS_NAME,"message")
        self.assertEqual("🎉 Congratulations! You won! 🎉",message.text)
        time.sleep(2)
                

