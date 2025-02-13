from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Changed from LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from wordbank.models import wordBank

class HangmanGameTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        wordBank.objects.create(word="BED", meaning="A piece of furniture for sleeping on")

        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)
    def tearDown(self):
        self.driver.quit()

    def test_hangman_game(self):


        # ปาร์คกดเข้าลิงค์ Hangman game จากหน้าเมนู 
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
        self.assertIn("GUESS",guess_button.text)

        # คำใบ้จาก database มาเทียบกับหน้า web ว่าตรงกันมั้ย
        word_obj = wordBank.objects.get(word="BED")
        expected_hint = word_obj.meaning
        hint = self.driver.find_element(By.CSS_SELECTOR, ".meaning").text
        self.assertEqual("HINT: "+expected_hint, hint)

        # ปาร์คใส่ตัวอักษร A และกดปุ่ม Guess
        input_field = self.driver.find_element(By.NAME, "letter")
        guess_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        input_field.send_keys("A")

        guess_button.click()

        # ปาร์คเห็นว่า Guessed Letters: จาก None กลายเป็น A สีแดง และAttempts Left: เหลือ 5  รวมทั้งตัวอักษรใน 
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text
        incorrect_letter_element = self.driver.find_element(By.XPATH, "//*[text()='A']")
        color = incorrect_letter_element.value_of_css_property('color')
        # self.assertEqual(color, 'rgba(255, 0, 0, 1)')  # rgba(255, 0, 0, 1) คือสีแดง
        self.assertEqual("Guessed Letters: A", guessed_letters)
        self.assertEqual("Attempts Left: 5", attempts_left)

        # รอจนกว่า input field สำหรับกรอกตัวอักษรจะพร้อมใช้งานอีกครั้ง
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 

        # ส่ปาร์คใส่ตัวอักษร E และกดปุ่ม Guess
        input_field.send_keys("E")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
          
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

        # ปาร์คเห็นข้อความ 🎉 Congratulations! You won! 🎉
        message =  self.driver.find_element(By.CLASS_NAME,"message")
        self.assertEqual("🎉 Congratulations! You won! 🎉",message.text)

         # ทดสอบว่ามีปุ่ม Start New Game มั้ย
        start_button = self.driver.find_element(By.CSS_SELECTOR, "button#restart")
        self.assertEqual("START NEW GAME",start_button.text);

        # เปลี่ยนคำใน database 
        wordBank.objects.all().delete() 
        wordBank.objects.create(word="YOLK", meaning="The yellow part of an egg, rich in nutrients")

        # ปาร์คกดปุ่ม Start New Game 
        start_button.click()

        # รอจนกว่าจะมี element ที่มี class word ปรากฏ ในที่นี้ก็คือ word_display 
        new_word = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'word'))
        )
        word_obj = wordBank.objects.get(word="YOLK")
        expected_hint = word_obj.meaning

        hint = self.driver.find_element(By.CSS_SELECTOR, ".meaning").text
        # ปาร์คสังเกตได้ว่ามีเส้นประ 4 ช่อง และคำใบ้เปลี่ยนไปเป็นคำว่า Hint: The yellow part of an egg, rich in nutrients
        self.assertEqual("HINT: "+expected_hint, hint)
        self.assertEqual(new_word.text,"_ _ _ _")


        # ปาร์คลองใส่ตัว A , B , C ปรากฏว่าไม่ถูกเลยทำให้ attempts_left เหลือ 3 

        #  ------------------A--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("A")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()   
        # ------------------B--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("B")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()   
        # ------------------C--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("C")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text

        # เทสว่า attempts_left เหลือ 3 จริงป่าว 
        self.assertEqual(attempts_left ,"Attempts Left: 3")
   

        # ปาร์คลองใส่ตัว A ปรากฏว่ามีการเเจ้งเตือนว่า 'You already guessed that letter!'
        input_field = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "letter"))
        )
        input_field.send_keys("A")

        # ปาร์คกดปุ่ม Guess
        guess_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        # รอจนกว่าข้อความแจ้งเตือนจะปรากฏ
        alert_message = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "message"))
        )

        # ตรวจสอบว่าข้อความแจ้งเตือนถูกต้อง
        self.assertEqual(alert_message.text, "You already guessed that letter!")
        
        # ปาร์คลองใส่ "ก" ปรากฏว่ามีการแจ้งเตือนว่า 'Please enter a valid single letter!'
        input_field = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "letter"))
        )
        input_field.send_keys("ก")

        # ปาร์คกดปุ่ม Guess
        guess_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        # รอจนกว่าข้อความแจ้งเตือนจะปรากฏ
        alert_message = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.NAME, "letter"))
        )
        input_field.clear()


        
        # ตรวจสอบว่าข้อความแจ้งเตือนถูกต้อง
        self.assertEqual(alert_message.get_attribute("title"), "Please enter a valid single English letter (A-Z)!")

        # ปาร์คลองใส่อักษรที่เหลือคือ D , Z , T ปรากฏว่าไม่ถูกเลยทำให้ attempts_left เหลือ 0 และขึ้นข้อความ "😢 Game Over! The word was: WE"
        
        #  ------------------D--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("D")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
   
        # ------------------Z--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("Z")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
   
        # ------------------T--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("T")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        attempts_left = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,".attempts"))
        ).text

        # เทสว่า attempts_left เหลือ 1 จริงป่าว 
        self.assertEqual(attempts_left ,"Attempts Left: 0")
 
        # ปาร์คเห็นข้อความ "😢 Game Over! The word was: WE"
        message =  self.driver.find_element(By.CLASS_NAME,"message")
        self.assertEqual("😢 Game Over! The word was: YOLK",message.text)
        # ปาร์คเห็นปุ่มที่มีคำว่า Back to menu และกดปุ่ม ทำให้ปาร์คกลับมาอยู่ในหน้าเมนูและเห็นลิงค์ Hangman Game
        back = self.driver.find_element(By.CLASS_NAME,"back_to_menu")
        self.assertEqual(back.text,"BACK TO MENU")
        back.click()

        hangman_link = self.driver.find_element(By.LINK_TEXT, "Hangman Game")
        self.assertIsNotNone(hangman_link) 
