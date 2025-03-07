# XSStrike

A **reflected XSS Tester for interactive forms** - The program automates testing for reflected XSS vulnerabilities by injecting various XSS payloads into a web application, automatically filling and submitting forms, and verifying whether the attack was successful by detecting alert() pop-ups or reflected code in the webpage.  

The program was created as part of my training at the Developer Academy and is used exclusively for teaching purposes.  

## Table of Contents

1. [Technologies](#technologies)
1. [Features](#features)  
1. [Getting Started](#getting-started)
1. [Usage](#usage)  
1. [Additional Notes](#additional-notes)

## Technologies

* **Python** 3.12.2
  * **argparse, time** (modules from standard library)
  * **Selenium** 4.9.0 (module to install, [More Information](https://selenium-python.readthedocs.io/))
    * **GeckoDriver for Firefox browser** v0.35.0 (driver to install, [More Information](https://github.com/mozilla/geckodriver))

## Features

The following table shows which functions **XSStrike** supports:  

| Flag | Description | Required |
| ---- | ----------- | -------- |
| -h <br> --help | Get a list of the **available options** | no |
| -u <br> --url | **URL** of the page containing the input form | yes |
| -l <br> --level | **Level** to be entered in the form | yes |
| -l_f <br> --level_field | Name of the **input field for the level** | yes |
| -p_f <br> --payload_field | Name of the **input field for the payload** | yes |
| -b <br> --button | Class_Name of the **submit button** | yes |
| -w <br> --wordlist | Path to the **file** containing XSS payloads | yes |
| -s <br> --sink | CSS selector of the **element** where the reflection should be checked | no |
| --headless | Runs the browser in **headless mode** | no |

* Loads the **XSS payloads** from the specified wordlist.
* Creates and configures the **WebDriver options** for Firefox.
* **Tests the XSS payloads** one after another:
  * Starts a new WebDriver instance for each payload.
  * Finds the definedinput fields and the submit button on the page.
  * Injects the respective XSS payload and submits the form.
  * Checks for a JavaScript execution (alert()) to confirm an XSS vulnerability.
  * If --sink is specified, it verifies if the payload appears in the HTML.
  * If XSS is detected, the test stops, otherwise, the next payload is tested.

## Getting Started

0) [Fork](https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the project to your namespace, if you want to make changes or open a [Pull Request](https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

1) [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the project to your platform if you just want to use the program:
   * <ins>Example</ins>: Clone the repo e.g. using an SSH-Key:

    ```bash
    git clone git@github.com:SarahZimmermann-Schmutzler/XSStrike.git
    ```

2) There are **dependencies to install**, the other modules are part of the standard library:
   * **Selenium**, you can install it across platforms with **Pip**:

    ```bash
    pip install selenium==4.9.0
    ```

   * The WebDriver for Selenium, in this case **GeckoDriver** for the Firefox browser:
     * Linux / Ubuntu:
       * [Downloading from GitHub](https://github.com/mozilla/geckodriver/releases)
         * `geckodriver-v0.35.0-linux64.tar.gz`
       * Open a terminal in the Download directory:
         * Unzip file:

            ```bash
            tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
            ```

         * Move the driver to a directory in which executable programs are stored and can be used system-wide:

            ```bash
            sudo mv geckodriver /usr/local/bin/geckodriver
            ```

     * [Versions for other operating systems](https://github.com/mozilla/geckodriver/releases)

## Usage

* Make sure you are in the folder where you cloned **XSStrike** into.  

* **Help!** What options does the program support!?

    ```bash
    python xsstrike.py -h
    # or
    python xsstrike.py --help
    ```  

* To run the reflected XSS Tester for interactive forms use the following **command** in your terminal:

    ```bash
    python xsstrike.py -u [URL] \
      -l [levelName] \
      -l_f [nameOfLevelInputField] \
      -p_f [nameOfPayloadInputField] \
      -b [classNameOfSubmitButton] \
      -s [cssSelectorOfSink] \ #optional
      -w [pathToWordlist]
    ```

  * **Example**: to automatically complete the fourth level of the `Insta XSS Challenges` from the Developer Akademie's XSS VM:

      ```bash
      python xsstrike.py -u "http://10.0.2.6/index.php" \
        -l "admin4"  \
        -l_f "user" \
        -p_f "password" \
        -b "login-btn" \
        -w "payload.txt"
      ```

  * What you see, in the **terminal**, if the right payload was the third entry in the wordlist:

      ```bash
      [*] Loaded 6 payloads.
      [*] Testing Payload: x" onerror="alert('Gehackt!')
      [-] No XSS detected.
      [*] Testing Payload: alert('Gehackt!')
      [-] No XSS detected.
      [*] Testing Payload: String.fromCharCode(97,108,101,114,116,40,39,71,101,104,97,99,107,116,33,39,41)
      [!] XSS detected with payload: String.fromCharCode(97,108,101,114,116,40,39,71,101,104,97,99,107,116,33,39,41)
      ```

## Additional Notes

In Python, **Selenium** is a library (open-source) that allows developers to automate web applications by writing a script that performs certain actions in a web browser as if it were controlled by a human user.  

To use Selenium, a WebDriver must be installed for the respective browser (e.g. **GeckoDriver** for Firefox).  

The **argparse** module is used to parse (read) command line arguments in Python programs. It allows to define arguments and options that can be passed to the program when starting it from the command line. These are then processed and are available in the program as variables.  

The **time** module in Python is a module from the standard library that provides functions to work with time. It provides basic tools to deal with time measurements, time zones and sleep functions.  
  
**Pip** is the default package manager for Python. It allows you to install, manage, and uninstall third-party Python libraries and modules. It simplifies the process of adding functionality to your Python projects by letting you download and install libraries from the Python Package Index (PyPI), a repository of Python packages.  
