import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def initiate_argparser() -> argparse.Namespace:
    """
    Parses and retrieves command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments with the following attributes:
            - url (str): URL of the page containing the input form.
            - level (str): Level to be entered in the form.
            - level_field (str): Name of the input field for the level.
            - payload_field (str): Name of the input field for the payload.
            - button (str): Class name of the submit button.
            - sink (str, optional): CSS selector of the element where the reflection should be checked.
            - wordlist (str): Path to the file containing XSS payloads.
            - headless (bool): True if the browser should run in headless mode, False otherwise.
    """
    parser = argparse.ArgumentParser(description="XSStrike - Reflected XSS Tester for interactive forms")
    parser.add_argument("-u", "--url", required=True, help="URL of the page containing the input form")
    parser.add_argument("-l", "--level", required=True, help="Level to be entered in the form")
    parser.add_argument("-l_f", "--level_field", required=True, help="Name of the input field for the level")
    parser.add_argument("-p_f", "--payload_field", required=True, help="Name of the input field for the payload")
    parser.add_argument("-b", "--button", required=True, help="Class_Name of the submit button")
    parser.add_argument("-s", "--sink", help="CSS selector of the element where the reflection should be checked")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the file containing XSS payloads")
    parser.add_argument("--headless", action="store_true", help="Runs the browser in headless mode")
    return parser.parse_args()


def load_payloads(wordlist_path: str) -> list[str]:
    """
    Loads XSS payloads from a wordlist file.

    Args:
        wordlist_path (str): Path to the wordlist file.

    Returns:
        list[str]: List of XSS payloads.
    """
    try:
        with open(wordlist_path, "r", encoding="utf-8") as file:
            payloads = [line.strip() for line in file if line.strip()]
        print(f"[*] Loaded {len(payloads)} payloads.")
        return payloads
    except FileNotFoundError:
        print(f"[!] Error: File {wordlist_path} not found.")
        exit(1)


def get_driver_options(headless: bool = False) -> FirefoxOptions:
    """
    Returns Firefox WebDriver options without starting the driver.
    """
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return options


def find_elements(driver: webdriver.Firefox, level_field: str, payload_field: str, button: str):
    """
    Finds the relevant HTML elements on the page.

    Args:
        driver (webdriver.Firefox): Selenium WebDriver instance.
        level_field (str): Name of the level input field.
        payload_field (str): Name of the payload input field.
        button (str): Class name of the submit button.

    Returns:
        tuple: (level_input, payload_input, submit_button) or (None, None, None) if not found.
    """
    try:
        level_input = driver.find_element(By.NAME, level_field)
        payload_input = driver.find_element(By.NAME, payload_field)
        submit_button = driver.find_element(By.CLASS_NAME, button)
        return level_input, payload_input, submit_button
    except NoSuchElementException:
        print("[!] Error: One or more input elements were not found.")
        return None, None, None


def submit_payload(
    level_input: str, 
    payload_input: str, 
    submit_button: str, 
    level: str, 
    payload: str
) -> None:
    """
    Fills in the input fields and submits the form.

    Args:
        driver (webdriver.Firefox): Selenium WebDriver instance.
        level_input: WebElement for the level input field.
        payload_input: WebElement for the payload input field.
        submit_button: WebElement for the submit button.
        level (str): Level value to be entered.
        payload (str): XSS payload to be tested.
    """
    level_input.clear()
    level_input.send_keys(level)

    payload_input.clear()
    payload_input.send_keys(payload)

    submit_button.click()
    time.sleep(2)  # Wait for the page to load


def check_alert(driver: webdriver.Firefox, payload: str) -> bool:
    """
    Checks if an alert box appears (indicating a successful XSS attack).

    Args:
        driver (webdriver.Firefox): Selenium WebDriver instance.
        payload (str): The tested XSS payload.

    Returns:
        bool: True if an alert box was detected, False otherwise.
    """
    try:
        alert = driver.switch_to.alert
        print(f"[!] XSS detected with payload: {payload}")
        alert.accept()  # Close the alert box
        return True
    except NoAlertPresentException:
        print("[-] No XSS detected.")
        return False
    

def check_sink(driver: webdriver.Firefox, sink: str, payload: str):
    """
    Checks if the XSS payload is reflected in the given sink element.

    Args:
        driver (webdriver.Firefox): Selenium WebDriver instance.
        sink (str): CSS selector of the sink element.
        payload (str): The tested XSS payload.
    """
    try:
        sink_element = driver.find_element(By.CSS_SELECTOR, sink)
        if payload in sink_element.get_attribute("innerHTML"):
            print(f"[!] XSS reflection detected in {sink}")
    except NoSuchElementException:
        print(f"[-] Sink {sink} not found.")


def test_xss(
    url: str, 
    level: str, 
    level_field: str, 
    payload_field: str, 
    button: str, 
    sink: str | None, 
    driver_options: FirefoxOptions, 
    payloads: list[str]
) -> None:
    """
    Tests an interactive web page for reflected XSS vulnerabilities.

    Args:
        url (str): URL of the page containing the input form.
        level (str): Level value to be entered.
        level_field (str): Name or ID of the level input field.
        payload_field (str): Name or ID of the payload input field.
        button (str): Name or ID of the submit button.
        sink (str | None): CSS selector of the sink element (if applicable).
        driver (webdriver.Firefox): Selenium WebDriver instance.
        payloads (list[str]): List of XSS payloads to be tested.
    """
    for payload in payloads:
        print(f"[*] Testing Payload: {payload}")

        # Start Webdriver
        driver = webdriver.Firefox(options=driver_options)
        driver.get(url)

        # Find input fields & button
        level_input, payload_input, submit_button = find_elements(driver, level_field, payload_field, button)
        if not level_input or not payload_input or not submit_button:
            return

        # Inject payload & submit form
        submit_payload(driver, level_input, payload_input, submit_button, level, payload)

        # Check for alert box
        if check_alert(driver, payload):
            driver.quit()
            return  # Stop after a successful attack

        # Check reflection in the sink element (if applicable)
        if sink:
            check_sink(driver, sink, payload)
        
        driver.quit()


def main() -> None:
    """
    Main function to parse arguments and start the XSS test.
    """
    args = initiate_argparser()
    payloads = load_payloads(args.wordlist)  # Load payloads from file
    driver_options = get_driver_options(args.headless)

    test_xss(args.url, args.level, args.level_field, args.payload_field, args.button, args.sink, driver_options, payloads)
    

if __name__ == "__main__":
    main()