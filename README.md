# instagram_scrapper dengan console log

step:
1. Download/Clone
   ```sh
   git clone https://github.com/sukaNLP/instagram_scrapper.git
   ```
2. Buka salah satu Browser dan masuk extensions (tested google chrome/brave)
3. Aktifkan mode `Developer mode`
4. klik `Load unpacked` dan pilih search for downloaded code
5. buka salah satu postingan, contoh : `https://www.instagram.com/p/<id_posting>`
6. buka Console dari Developer Tools atau tekan F12
7. klik extension logo (bisanya berbentuk `puzzle`)
8. tunggu sampai keluar hasilnya di console log (lama proses tergantung jumlah komentar perpostingan)


# instagram_scrapper dengan python ipynb
1. Buka File IG_Scraping.ipynb
2. Masukkan akun untuk login (username/password)
3. Masukkan Keyword/link target postingan
4. kemudian run all

# instagram_scrapper dengan Selenium
1. Create a virtual environment

   ```bash
   python -m venv [venv]
   ```

2. Activate virtual environment

   ```bash
   # For Windows
   source [venv]/scripts/activate
   # For Mac or Linux
   source [venv]/bin/activate
   ```

3. Install pip packages
   ```bash
   pip install -r requirements.txt
   ```
## 🔑 Usage

- `ChromeDriver` in `driver.py` is a customized version of Selenium webdriver.
  So some function of original webdriver is not available.

  ```python
  from driver import ChromeDriver
  driver = ChromeDriver()
  ```

- Details of customized setting

  - `user-agent` : randomly changed when launching script.
  - `auto download chrome driver` : automatically download chrome driver compatible with chrome browser installed.
  - Default download path
    ```bash
    # For windows
    C:/Program Files/chrome or C:/Program Files (x86)/chrome
    # For Mac
    /usr/bin/chrome
    ```

- It is necessary to login to access an instagram post. User account and password are entered on terminal. Password will be hided by `getpass` when entering input.

  ```python
  import getpass
  driver.move_to_login_page()

  username = input("Input ID : ")
  password = getpass.getpass("Input Password :")

  # For only personal usage, you can just put raw data.
  # username = "instagram_account"
  # password = "password"

  driver.login_to_instagram(username, password)
  ```

- Set an instagram post url to `target_url`

  ```python
  target_url = "https://www.instagram.com/p/..."
  driver.get(target_url)
  ```

- Load all comments and replies.

  ```python
  driver.load_all_comments()
  driver.load_all_replies()
  ```

- Save all comments and replies to CSV file. It will be saved to `comments_{yyyy_mm_dd_hh_mm_ss}.csv`

  ```python
  driver.collect_comments()
  ```

- Close chrome driver at the end of script.
  ```python
  driver.close()
  ```
