from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
# Chemin vers le pilote (driver) de votre navigateur
#driver_path = 'chemin/vers/votre/driver/chromedriver'

# Créez une instance du navigateur
# Set the download directory : kol 7ad ybadel esm l theme elli 3andou : lists, dictate....
download_directory = os.path.join(os.getcwd(), "dataset-collection-LOW/format")

# Configure Chrome to automatically download files to the specified directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
}
chrome_options.add_experimental_option("prefs", prefs)

# Create a Chrome instance with the configured options
driver = webdriver.Chrome(chrome_options)

# Ouvrez le site https://freetts.com/
driver.get("https://freetts.com/")

# Trouvez le champ de texte pour saisir le texte à convertir en audio
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.XPATH, "*")))

text_input = driver.find_element(By.ID, "textarea")

command_list = {
    "align_center": ["align center"],
    "align_left": ["align left"],
    "align_right": ["align right"],
    "bold_word": ["bold word"],
    "bold_phrase": ["bold phrase"],
    "bold_that": ["bold that"],
    "capitalize_word": ["capitalize word"],
    "capitalize_phrase": ["capitalize phrase"],
    "capitalize_that": ["capitalize that"],
    "clear": ["clear formatting"],
    "decrease": ["decrease indent"],
    "increase": ["increase indent"],
    "italicize_word": ["italicize word"],
    "italicize_phrase": ["italicize phrase"],
    "italicize_that": ["italicize that"],
    "italics": ["italics"],
    "lowercase_word": ["lowercase word"],
    "lowercase_phrase": ["lowercase phrase"],
    "lowercase_that": ["lowercase that"],
    "remove_strikethrough_from_word": ["remove strikethrough from word"],
    "remove_strikethrough_from_phrase": ["remove strikethrough from phrase"],
    "remove_strikethrough_from_that": ["remove strikethrough from that"],
    "remove_bold_from_word": ["remove bold from word"],
    "remove_bold_from_phrase": ["remove bold from phrase"],
    "remove_bold_from_that": ["remove bold from that"],
    "remove_highlight": ["remove highlight", "remove highlight from word", "remove highlight from phrase", "remove highlight from that"],
    "remove_italics_from_word": ["remove italics from word"],
    "remove_italics_from_phrase": ["remove italics from phrase"],
    "remove_italics_from_that": ["remove italics from that"],
    "remove_subscript_from_word": ["remove subscript from word"],
    "remove_subscript_from_phrase": ["remove subscript from phrase"],
    "remove_subscript_from_that": ["remove subscript from that"],
    "remove_superscript_from_word": ["remove superscript from word"],
    "remove_superscript_from_phrase": ["remove superscript from phrase"],
    "remove_superscript_from_that": ["remove superscript from that"],
    "remove_underline": ["remove underline", "remove underline from word", "remove underline from phrase", "remove underline from that"],
    "remove_uppercase_from_word": ["remove uppercase from word"],
    "remove_uppercase_from_phrase": ["remove uppercase from phrase"],
    "remove_uppercase_from_that": ["remove uppercase from that"],
    "strikethrough_word": ["strikethrough word"],

    ##"strikethrough_phrase": ["strikethrough phrase"],
    ##"strikethrough_that": ["strikethrough that"],
    ##"subscript_word": ["subscript word"],
    ##"subscript_phrase": ["subscript phrase"],
    ##"subscript_that": ["subscript that"],
    ##"superscript_word": ["superscript word"],
    ##"superscript_phrase": ["superscript phrase"],
    ##"superscript_that": ["superscript that"],
    ##"underline_word": ["underline word"],
    ##"underline_phrase": ["underline phrase"],
    ##"underline_that": ["underline that"],
    ##"uppercase_word": ["uppercase word"],
    ##"uppercase_phrase": ["uppercase phrase"],
    ##"uppercase_that": ["uppercase that"],
}
#liste des commandes textuelles à convertir pour Maissa
#command_list = {"stop" : ["stop dictation","stop","stop now"],
#                "pause" : ["pause dictation","pause","pause now"],
#                "close" : ["close dictation","close","exit dictation"],
#                "help" : ["show help","help","open help","show commands"]
# 
#            }
#liste des commandes textuelles à convertir pour Maissa : Editing
command_list = {"delete" : ["delete word","delete","scratch","erase","delete that","delete sentence"],
                "insert" : ["insert space"],
                "undo" : ["undo"],
                }

#liste des commandes textuelles à convertir pour Amna
command_list = {
     "create_numbered_list" : ["create numbered list","create number list","create list","start numbered list","start number list","insert numbered list","insert number list","add numbered list","add number list"],
                "create_bulleted_list" : ["create bulleted list","create bullet list","create list","start bulleted list","start bullet list","start list","insert bulleted list","insert bullet list","insert list","add bulleted list","add bullet list","add list"],
                "next_numbered_list" : ["next item","next line"],
                "next_bulleted_list" : ["next bullet","next line"],
                "exit_numbered_list" : ["exit numbered list","exit number list","exit list"],
                "exit_bulleted_list" : ["exit bulleted list","exit bullet list","exit list"]               
               }

# Selectionner le premier choix de la voix ( first radio button)
wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@type,'radio')]")))
first_radio_button = driver.find_elements(By.XPATH,"//input[contains(@type,'radio')]")
#changer 0 ou 1 ou 2 pour changer le type de la voix 
first_radio_button[0].click()

for key in command_list:
          folder_path = os.path.join(download_directory, key)
          if not os.path.exists(folder_path):
             os.makedirs(folder_path)
          for command in command_list[key] :
               print(command)
               text_input.send_keys(command)
               print(text_input)
               # Cliquez sur le bouton de conversion en audio 
               wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'convert-button')]")))
               convert_button = driver.find_element(By.XPATH,"//button[contains(@class,'convert-button')]")
               convert_button.click()
               #driver.execute_script("arguments[0].click();", convert_button)
               
               #print(convert_button)
               # Attendez que la conversion soit terminée
               time.sleep(5)
               
               # Cliquez sur le bouton de téléchargement de l'audio 
               wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'download-button')]")))
               download_button = driver.find_element(By.XPATH,"//button[contains(@class,'download-button')]")
               download_button.click()
               print(download_button)
               # Wait for the download to complete
               time.sleep(3)
               
               # Move the downloaded file to the folder
               downloaded_files = os.listdir(download_directory)
               for file in downloaded_files:
                 if file.endswith(".mp3"):
                     os.rename(os.path.join(download_directory, file), os.path.join(folder_path, file))    
               text_input.clear()
     
# Fermez le navigateur
driver.quit()
