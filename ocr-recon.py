from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium
import time
import requests
import concurrent.futures
from colorama import Fore
import sys
import os
import subprocess
import warnings
from PIL import Image
import pytesseract
import shutil

warnings.filterwarnings("ignore", category=DeprecationWarning)

if len(sys.argv) < 3:
    print(Fore.WHITE+"Usage: python3 ocr-recon.py listwithURLs <stringtosearch>")
    sys.exit()

patternarg=sys.argv[2]

#Idea: adaptar esto para que busque regex en vez de strings


def recon_image(path,pattern=patternarg):
        #print(pattern)
        img = Image.open(path)
        #print("here")
        img.load()
        text = pytesseract.image_to_string(img)
        #print(pattern)
        if pattern in text:
            print(Fore.GREEN+"[+] Success in "+os.path.basename(path).split(".png")[0]+Fore.WHITE)
def cleanup():
    shutil.rmtree(os.path.join(os.getcwd(), r"tmp"))

def send_requests(_Url_):
    options = Options()
    options.add_argument('--headless')
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    driver = webdriver.Firefox(firefox_profile=profile,options=options, service_log_path="/dev/null")
    driver.set_page_load_timeout(10)
    try:
       driver.get(_Url_.strip())
       driver.get_screenshot_as_file("tmp/"+_Url_.strip().split("//")[1]+".png")
       driver.quit()
       text = recon_image(os.path.join(os.getcwd()+r"/tmp/"+_Url_.strip().split("//")[1]+".png"))

    except selenium.common.exceptions.TimeoutException:
        print(Fore.RED+"[-] Timeout in "+_Url_.strip()+Fore.WHITE)
        return
    except Exception as e:
        print(e)

    

def main():
    
    listwithURLs=open(sys.argv[1], "r").readlines()

    patternarg = sys.argv[2]


    #check if the tmp directory exists

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'tmp')
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
         executor.map(send_requests, listwithURLs)
    cleanup()

if __name__ == "__main__":
   main()
