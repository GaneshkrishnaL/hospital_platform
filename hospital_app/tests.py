# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Hospital, Bed, Reservation
import hashlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DjangoLoginTest(unittest.TestCase):

    def test_login(self):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/login/")  # Your Django login URL

        # Find the form elements
        email = driver.find_element(By.NAME, 'email')  # Updated method
        password = driver.find_element(By.NAME, 'password')  # Updated method
        submit = driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Input test data
        email.send_keys("laddo@gmail.com")
        password.send_keys("mouse")
        submit.click()
        print("login is working fine")

        # Include your assertions here

        # Close the browser after the test
        driver.quit()

class DjangoRegistrationTest(unittest.TestCase):

    def setUp(self):
        # Setup the Chrome WebDriver
        self.driver = webdriver.Chrome()

    def test_registration(self):
        # Open the registration page
        self.driver.get("http://127.0.0.1:8000/register/")  # Replace with your registration URL

        # Wait for the 'patient' radio button and click it using JavaScript
        user_type_patient = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@value="patient"]'))
        )
        self.driver.execute_script("arguments[0].click();", user_type_patient)

        # Find and fill in the form fields
        email = self.driver.find_element(By.NAME, 'email')
        password = self.driver.find_element(By.NAME, 'password')
        name = self.driver.find_element(By.NAME, 'name')
        phone = self.driver.find_element(By.NAME, 'phone')
        age = self.driver.find_element(By.NAME, 'age')
        add = self.driver.find_element(By.NAME, 'address')
        blood = self.driver.find_element(By.NAME, 'bloodGroup')
        # ... Continue for other fields ...

        # Input test data
        email.send_keys("test11@example.com")
        password.send_keys("YourTestPassword!123")
        name.send_keys("Test User")
        phone.send_keys("1234567890")
        age.send_keys("20")
        add.send_keys("temp")
        blood.send_keys("AB-")
        # ... Continue for other fields ...

        # Submit the form
        submit = self.driver.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        print("registration successfull")
        # Assertions to verify registration was successful
        # self.assertIn("Success Message or Redirect URL", self.driver.page_source)

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()




class DjangoDashboardTest(unittest.TestCase):

    def setUp(self):
        # Setup the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Implicit wait for elements to appear

    def test_reserve_bed(self):
        # Login first
        self.driver.get("http://127.0.0.1:8000/login/")
        email = self.driver.find_element(By.NAME, 'email')
        password = self.driver.find_element(By.NAME, 'password')
        submit = self.driver.find_element(By.XPATH, '//input[@type="submit"]')

        email.send_keys("patient1@gmail.com")
        password.send_keys("4f~zr98bCaBXTbw@")
        submit.click()

        # Assume you're redirected to the dashboard, otherwise use self.driver.get(url) to navigate

        # Find the first hospital's reserve form (customize this as needed)
        reserve_form = self.driver.find_elements(By.CSS_SELECTOR, 'form[action*="make_reservation"]')[0]

        # Select 'General' bed type
        bed_type_dropdown = reserve_form.find_element(By.NAME, 'bed_type')
        for option in bed_type_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'General':
                option.click()
                break

        # Submit the reservation
        reserve_button = reserve_form.find_element(By.TAG_NAME, 'button')
        reserve_button.click()
        print("bed reservation request sent")
        # Assertions to verify reservation was successful
        # self.assertIn("Success Message or Redirect URL", self.driver.page_source)

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()


class DjangoHospitalDashboardTest(unittest.TestCase):

    def setUp(self):
        # Setup the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Implicit wait for elements to appear

    def test_confirm_reservation(self):
        # Login as hospital
        self.driver.get("http://127.0.0.1:8000/login/")
        hospital_radio_button = self.driver.find_element(By.XPATH, '//input[@value="hospital"]')
        hospital_radio_button.click()

        email = self.driver.find_element(By.NAME, 'email')
        password = self.driver.find_element(By.NAME, 'password')
        submit = self.driver.find_element(By.XPATH, '//input[@type="submit"]')

        email.send_keys("yashoda@gmail.com")
        password.send_keys("yashoda123")
        submit.click()

        # Navigate to hospital dashboard
        self.driver.get("http://127.0.0.1:8000/hospital_dashboard/")

        # Check if there are pending reservations
        pending_reservations = self.driver.find_elements(By.CSS_SELECTOR, ".reservations-table a[href*='confirm']")
        if len(pending_reservations) > 0:
            # Confirm the first pending reservation
            pending_reservations[0].click()
            print("reservation successfull")
            # Add assertion or further actions here if needed
        else:
            print("No pending reservations to confirm")

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()




# class HospitalAppTests(TestCase):
#     def setUp(self):
#         # Create a client to simulate web requests
#         self.client = Client()

#         # Create test user and hospital
#         self.user_password = 'user_password'
#         self.user = User.objects.create(
#             name='Test User',
#             email='user@test.com',
#             phone='1234567890',
#             age=30,
#             gender='Male',
#             address='123 Test St',
#             bloodGroup='A+',
#             password=hashlib.sha256(self.user_password.encode()).hexdigest()
#         )

#         self.hospital_password = 'hospital_password'
#         self.hospital = Hospital.objects.create(
#             hospitalName='Test Hospital',
#             email='hospital@test.com',
#             phone='0987654321',
#             location='Hospital Location',
#             area='Hospital Area',
#             password=hashlib.sha256(self.hospital_password.encode()).hexdigest()
#         )

#         # Create test beds
#         Bed.objects.create(hospital=self.hospital, bed_type='ICU')
#         Bed.objects.create(hospital=self.hospital, bed_type='GEN')
#         Bed.objects.create(hospital=self.hospital, bed_type='PRI')

#     def test_login_view(self):
#         url = reverse('login')
#         response = self.client.post(url, {
#             'email': self.user.email,
#             'password': self.user_password,
#             'user_type': 'patient'
#         })
#         self.assertEqual(response.status_code, 302)
#         # Add more assertions here to test different scenarios

#     def test_logout_view(self):
#         self.client.login(email=self.user.email, password=self.user_password)
#         url = reverse('logout')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 302)

#     def test_register_view(self):
#         url = reverse('register')
#         response = self.client.post(url, {
#             'user_type': 'patient',
#             'name': 'New User',
#             'email': 'newuser@test.com',
#             'phone': '1231231234',
#             'age': 25,
#             'gender': 'Female',
#             'address': 'New Address',
#             'bloodGroup': 'O-',
#             'password': 'new_password'
#         })
#         self.assertEqual(response.status_code, 302)
#         # Add more assertions here




#     def test_make_reservation(self):
#         self.client.login(email=self.user.email, password=self.user_password)
#         url = reverse('make_reservation')
#         response = self.client.post(url, {
#             'hospital_id': self.hospital.id,
#             'bed_type': 'ICU'
#         })
#         self.assertEqual(response.status_code, 302)
#         # Add more assertions here

#     def test_update_reservation(self):
#         self.client.login(email=self.hospital.email, password=self.hospital_password)
#         reservation = Reservation.objects.create(
#             user=self.user, 
#             hospital=self.hospital, 
#             bed=Bed.objects.first(),
#             status='pending'
#         )
#         url = reverse('update_reservation', args=[reservation.id, 'confirm'])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 302)
#         # Add more assertions here

# # Add more test cases as needed