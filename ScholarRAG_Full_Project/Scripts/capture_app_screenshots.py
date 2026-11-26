import subprocess
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

APP_DIR = r"C:\Users\sdmal\OneDrive\Desktop\hunt\Multi-PDF-RAG-App---25-08-2026"
STREAMLIT_EXE = os.path.join(APP_DIR, "venv", "Scripts", "streamlit.exe")
ASSETS_DIR = r"C:\Users\sdmal\OneDrive\Desktop\hunt\assets"
SAMPLE_PDF = r"C:\Users\sdmal\OneDrive\Desktop\pdf\Unit4_Easy_Notes.pdf"

print("Starting Streamlit server...")
proc = subprocess.Popen(
    [STREAMLIT_EXE, "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
    cwd=APP_DIR
)

time.sleep(4)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1000")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://localhost:8501")
    time.sleep(6)
    
    # 1. Dark mode full screenshot
    driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_01_landing_dark.png"))
    print("Saved screenshot_01_landing_dark.png")

    # 2. Toggle to Light mode
    radios = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='stRadio'] label")
    print(f"Found {len(radios)} radio labels")
    for r in radios:
        print("Radio text:", r.text)
        if "Light" in r.text:
            r.click()
            time.sleep(3)
            driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_02_landing_light.png"))
            print("Saved screenshot_02_landing_light.png")
            break

    # Switch back to dark mode
    for r in driver.find_elements(By.CSS_SELECTOR, "div[data-testid='stRadio'] label"):
        if "Dark" in r.text:
            r.click()
            time.sleep(2)
            break

    # 3. Sidebar close-up
    sidebar = driver.find_element(By.CSS_SELECTOR, "section[data-testid='stSidebar']")
    sidebar.screenshot(os.path.join(ASSETS_DIR, "screenshot_03_sidebar_controls.png"))
    print("Saved screenshot_03_sidebar_controls.png")

    # 4. Upload file
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(SAMPLE_PDF)
    print("Sent file to uploader...")
    time.sleep(5)
    driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_04_file_uploaded.png"))
    print("Saved screenshot_04_file_uploaded.png")

    # 5. Click process button
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    for b in buttons:
        if "Submit & Process" in b.text:
            print("Clicking Submit & Process...")
            b.click()
            break

    # Wait for indexing to complete
    print("Waiting for processing to complete...")
    for _ in range(60):
        time.sleep(2)
        txt = driver.page_source
        if "Processed" in txt or "Vector Store" in txt or "stAlert" in txt or "total_pages" in txt:
            # check if spinner is gone
            spinners = driver.find_elements(By.CSS_SELECTOR, "[data-testid='stSpinner']")
            if not spinners:
                print("Processing completed!")
                break
    time.sleep(3)
    driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_05_indexed_dashboard.png"))
    print("Saved screenshot_05_indexed_dashboard.png")

    # 6. Ask Question
    text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    print(f"Found {len(text_inputs)} text inputs")
    if text_inputs:
        target_input = text_inputs[0]
        target_input.click()
        target_input.send_keys("Summarize the key architectural components and methodology.")
        time.sleep(1)
        
        # Submit
        for b in driver.find_elements(By.CSS_SELECTOR, "button"):
            if "Ask" in b.text or "Submit" in b.text or "Send" in b.text:
                b.click()
                print("Clicked ask button")
                break
        else:
            from selenium.webdriver.common.keys import Keys
            target_input.send_keys(Keys.RETURN)
            print("Pressed Enter")

        print("Waiting for response...")
        for _ in range(40):
            time.sleep(1)
            spinners = driver.find_elements(By.CSS_SELECTOR, "[data-testid='stSpinner']")
            if not spinners and len(driver.find_elements(By.CSS_SELECTOR, "div.stMarkdown")) > 5:
                break
        time.sleep(4)
        driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_06_rag_answer.png"))
        print("Saved screenshot_06_rag_answer.png")

        # 7. Expand expanders (citations)
        expanders = driver.find_elements(By.CSS_SELECTOR, "details, [data-testid='stExpander']")
        print(f"Found {len(expanders)} expanders")
        for exp in expanders:
            try:
                exp.click()
            except Exception:
                pass
        time.sleep(2)
        driver.save_screenshot(os.path.join(ASSETS_DIR, "screenshot_07_citations_expanded.png"))
        print("Saved screenshot_07_citations_expanded.png")

except Exception as err:
    print("Error:", err)
finally:
    driver.quit()
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    print("Finished.")
