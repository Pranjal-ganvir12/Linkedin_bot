import tkinter as tk #GUI
from tkinter import messagebox #GUI message 
from selenium import webdriver #using chrome for testing
from selenium.webdriver.common.by import By #helps in locating things on webpage
from selenium.webdriver.common.keys import Keys #using keys 
import time, random # time: Pauses, random : imitating humanly intervals 

driver = webdriver.Chrome()  # Will detect local chromedriver
driver.get("https://google.com")

def start_bot():
    print("Bot started...")
    jobs = job_entry.get("1.0", tk.END).strip().split("\n")
    companies = company_entry.get("1.0", tk.END).strip().split("\n")
    message = message_box.get("1.0", tk.END).strip()

    if not jobs or not companies:
        messagebox.showerror("Error", "Fill in the Job Titles and Company")
        return
    
    send_message = bool(message)
    sent = 0

    driver = webdriver.Chrome()
    #link = "https://www.linkedin.com/login"
    driver.get("https://www.linkedin.com/login")
    time.sleep(60)

    for job in jobs:
        for company in companies:
            if sent >= 10:
                break
            
            search = f"{job} {company}"
            url = "https://www.linkedin.com/search/results/people/?keywords=" + search.replace(" ", "%20")
            driver.get(url)
            time.sleep(10)

            for scroll in range(3):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(2)

            buttons = driver.find_elements(By.XPATH,"//span[text()='Connect']/ancestor::button")
            for button in buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(1)
                    button.click()
                    time.sleep(2)
                    if send_message:
                        add_note_btn = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
                        add_note_btn.click()
                        time.sleep(1)
                        msg_box = driver.find_element(By.XPATH, "//textarea[@name='message']")
                        msg_box.send_keys(message)
                        time.sleep(1)
                        send_btn = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                        send_btn.click()
                    else:
                        send_btn = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                        send_btn.click()

                    time.sleep(2)
                    sent += 1
                except Exception as e:
                    print("Skipped a button due to error:", e)
                    continue
                
    driver.quit()







#GUI stuff
root = tk.Tk()
root.title("Smart LinkedIn Outreach Bot")
root.geometry("500x500")  # Set a bigger window size
root.configure(bg="white")

tk.Label(root, text="Job Titles (one per line):").pack()
job_entry = tk.Text(root, height=5, width=50)
job_entry = tk.Text(root, height=5, width=40, bg="white", fg="black", font=("Arial", 12))
job_entry.pack()

tk.Label(root, text="Companies (one per line):").pack()
company_entry = tk.Text(root, height=5, width=50)
company_entry.pack()

tk.Label(root, text="Connection Message (optional):").pack()
message_box = tk.Text(root, height=5, width=50)
message_box.pack()

start_button = tk.Button(root, text="Start Automation", command=start_bot)
start_button.pack(pady=10)
root.update_idletasks()

root.mainloop()

