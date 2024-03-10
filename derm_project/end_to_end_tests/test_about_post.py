import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

driver = webdriver.Chrome()
# driver = webdriver.Firefox()


@pytest.fixture(autouse=True)
def start_automatic_fixture():
    """_summary_"""
    print("Start Test With Automatic Fixture")


@pytest.fixture()
def setup_teardown():
    """_summary_"""
    driver.get("http://127.0.0.1:8000/")
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys("drGriffin")
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(
        "goldsmiths456"
    )
    driver.find_element(By.ID, "login").click()
    print("Log In")
    # setup occurs before yield
    # teardown occurs after
    yield
    driver.find_element(By.ID, "logout").click()
    print("Log Out")


def test_about(setup_teardown):
    """
    simple  test to login with dummy credentials,
    navigate to about page,
    then logout
    """
    driver.find_element(By.XPATH, "//a[@href='/about/']").click()
    about_text = driver.find_element(By.TAG_NAME, "h1").text
    assert about_text == "About Page", "About page text does not match expected text"
    print("About page test is complete")


def test_post(setup_teardown):
    """
    test post function end-to-end
    """
    driver.find_element(By.XPATH, "//a[@href='/post/new/']").click()
    driver.find_element(By.ID, "id_age").send_keys("25")
    driver.find_element(By.ID, "id_gender").send_keys("female")
    driver.find_element(By.ID, "id_ethnicity").send_keys("African")
    driver.find_element(By.ID, "id_country").send_keys("United Kingdom")
    driver.find_element(By.ID, "id_history").send_keys(
        "pregnant woman with sudden eruption of multiple papules on trunk, slightly itchy"
    )
    driver.find_element(By.ID, "id_skin_location").send_keys("trunk")
    driver.find_element(By.ID, "id_provdx").send_keys("PUPPP")
    driver.find_element(By.ID, "id_ddx1").send_keys("chronic urticaria")
    driver.find_element(By.ID, "id_ddx2").send_keys("scabies")
    driver.find_element(By.ID, "id_pic1").send_keys(
        os.getcwd() + "/derm_project/media/pics/puppp.png"
    )
    driver.find_element(By.ID, "id_tags").send_keys("trunk")

    # Wait until the post button is clickable
    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
    post_button = wait.until(EC.element_to_be_clickable((By.ID, "post")))

    # Scroll the post button into view
    driver.execute_script("arguments[0].scrollIntoView();", post_button)

    # Use JavaScript to click the post button
    driver.execute_script("arguments[0].click();", post_button)
    WebDriverWait(driver, 5).until(
        lambda _: "home" in driver.current_url,
        "Page did not load: %s" % driver.current_url,
    )
    age = driver.find_element(By.XPATH, "//div[@class='container']//p[1]").text
    assert age == "Age: 25", "Age does not match expected value"
    gender = driver.find_element(By.XPATH, "//div[@class='container']//p[2]").text
    assert gender == "Gender: female", "Gender does not match expected value"
    ethnicity = driver.find_element(By.XPATH, "//div[@class='container']//p[3]").text
    assert ethnicity == "Ethnicity: African", "Ethnicity does not match expected value"
    country = driver.find_element(By.XPATH, "//div[@class='container']//p[4]").text
    assert country == "Country: United Kingdom", "Country does not match expected value"
    skin_location = driver.find_element(
        By.XPATH, "//div[@class='container']//p[5]"
    ).text
    assert (
        skin_location == "Location on body: trunk"
    ), "Skin location does not match expected value"
    history = driver.find_element(By.XPATH, "//div[@class='container']//p[6]").text
    assert "pregnant" in history, "History does not match expected value"

    provdx = driver.find_element(By.XPATH, "//div[@class='container']//p[7]").text
    assert (
        provdx == "Provisional Diagnosis: PUPPP"
    ), "Provisional diagnosis does not match expected value"
    dx1 = driver.find_element(By.XPATH, "//div[@class='container']//p[8]").text
    assert (
        dx1 == "Differential Diagnosis#1: chronic urticaria"
    ), "Differential diagnosis # does not match expected value"
    dx2 = driver.find_element(By.XPATH, "//div[@class='container']//p[9]").text
    assert (
        dx2 == "Differential Diagnosis#2: scabies"
    ), "Differential diagnosis does not match expected value"
    tags = driver.find_element(By.XPATH, "//div[@class='container']//p/b/i[1]").text
    assert tags == "trunk", "Tags do not match expected value"
    img = driver.find_element(
        By.XPATH, "//div[@class='container']//a[1]/img[@alt='PUPPP']"
    )
    assert img, "Image not found"

    print("Post test is complete")
