import time, threading, random, string, warnings, os
from ocr_handler import ocr_screen_handler
from memu_handler import memu_instance_handler
from bs4 import XMLParsedAsHTMLWarning
from bs4 import BeautifulSoup as bs
from colorama import Fore, init
init()

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class MSPHandler(object):
    def __init__(self):
        super(MSPHandler, self).__init__()

        self.running = True

class MSPThread(threading.Thread):
    def __init__(self, memu, ocr, msp, location, index, name=None, new_instances=None):
        super(MSPThread, self).__init__()

        self.daemon = True
        self.new_instance = new_instances
        self.msp = msp
        self.memu = memu
        self.ocr = ocr
        self.index = index
        self.name = name
        self.location = location
        self.pictures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Pictures')
        self.image_path = os.path.join(self.pictures_dir, f"screenshot{self.index}.png")

    def run(self):
        self.set_minimal_settings()
        self.memu.start(self.index, None, False, True, None) #index, name, headless, taskid, timeout
        if self.new_instance:
            print(f"New instance: {self.new_instance} [{self.index}]. Waiting 1 minute 30 seconds")
            time.sleep(90)
            #print(f"Attempting to bypass ads {self.index}")
            #self.memu.send_key(self.index, None, "home")
            #adb shell dumpsys window windows | grep -E 'mCurrentFocus'
            if "com.applovin.adview.AppLovinFullscreenActivity" in self.memu.adb(self.index, None, "shell dumpsys window windows | grep -E 'mCurrentFocus'"):
                print(f"[!] ADS DETECTED || Sending to home {self.index}")
                self.memu.send_key(self.index, None, "home")
            #print(self.memu.adb(self.index, None, "shell am force-stop com.applovin.adview.AppLovinFullscreenActivity"))
        else:
            print(f"Old instance: {self.new_instance} [{self.index}]. Waiting 1 minute...")
            time.sleep(60)
            if "com.applovin.adview.AppLovinFullscreenActivity" in self.memu.adb(self.index, None, "shell dumpsys window windows | grep -E 'mCurrentFocus'"):
                print(f"[!] ADS DETECTED || Sending to home {self.index}")
                self.memu.send_key(self.index, None, "home")
        self.setup_instance(r"C:\Users\vials\Downloads\MovieStarPlanet_ Classic_53.0.30_APKPure.apk", "air.MSPMobile")
        time.sleep(2)
        self.memu.set_configex(self.index, None, "geometry", self.location)
        self.wait_msp_main_login()
        self.set_msp_server_region()
        self.verify_msp_server_region()
        while self.msp.running:
            time.sleep(1)
        
    def set_minimal_settings(self):
        self.memu.randomize(self.index, self.name)
        self.memu.set_configex(self.index, None, "custom_resolution", "1600 1000 300")
        self.memu.set_configex(self.index, None, "enable_su", "1")
        self.memu.set_configex(self.index, None, "memory", "2048")
        self.memu.set_configex(self.index, None, "cpus", "1")
        self.memu.set_configex(self.index, None, "enable_audio", "0")

    def setup_instance(self, apk="", package_name=""):
        try:
            reset_counter = 0
            max_attempt = 8
            current_attempt = 0
            checkScreenError = None
            screenChecked = True
            while screenChecked:
                if "Running" in self.memu.is_vm_running(self.index, None):
                    if current_attempt == max_attempt:
                        #nuke instance then remake
                        reset_counter += 1
                        self.reset_instance()
                        current_attempt = 0
                    checkScreenError = self.memu.dumpScreenView(self.index)
                    if checkScreenError:
                        memuLauncherFix = bs(checkScreenError.split("\n")[2], "lxml")
                        for content in memuLauncherFix.find_all("node"):
                            if "MEmu Launcher2 has stopped" in content["text"] or "MEmu Launcher2 has stopped" in content["text"] or "MEmu Launcher2 isn't responding" in content["text"]:
                                #self.memu.adb(self.index, None, "shell input tap 400 400")
                                self.memu.send_key(self.index, None, "home")
                                #time.sleep(10)
                            elif "Search Games and Apps" in content["text"]:
                                #print(f"Home screen detected {self.index}")
                                screenChecked = False
                    else:
                        #print(f"[{Fore.RED}-{Fore.WHITE}] Failed to dump screen {self.index}, retrying in 5 seconds")
                        current_attempt += 1
                        self.memu.send_key(self.index, None, "home")
                        time.sleep(5)
                    """if not self.home_screen_check():
                        print(f"Home screen not detected on {self.index}")
                        current_attempt += 1"""
                            
            #print(f"STARTING APP INSTALLATION {self.index}")
            #self.memu.uninstall_apk(self.index, None, package_name)
            #print(f"Attempting app install on: {self.index} after 5 seconds")
            time.sleep(5)
            self.memu.send_key(self.index, None, "home")
            #self.memu.install_apk(self.index, None, apk)
            #self.memu.send_key(self.index, None, "home") #bypass ads on new instance
            self.memu.adb(self.index, None, f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        except Exception as e:
            print(f"{e}")
            pass

    def home_screen_check(self):
        checkScreenError = self.memu.dumpScreenView(self.index)
        if checkScreenError:
            memuLauncherFix = bs(checkScreenError.split("\n")[2], "lxml")
            for content in memuLauncherFix.find_all("node"):
                if "MEmu Launcher2 has stopped" in content["text"] or "MEmu Launcher2 has stopped" in content["text"] or "MEmu Launcher2 isn't responding" in content["text"]:
                    #self.memu.adb(self.index, None, "shell input tap 400 400")
                    self.memu.send_key(self.index, None, "home")
                    #time.sleep(10)
                    """elif "MEmu Launcher2 isn't responding" in content["text"]:
                    #self.memu.adb(self.index, None, "shell input tap 600 420")
                    self.memu.send_key(self.index, None, "home")"""
                elif "Search Games and Apps" in content["text"]:
                    #print(f"Home screen detected {self.index}")
                    return True
                
        else:
            #print(f"[{Fore.RED}-{Fore.WHITE}] Failed to dump screen {self.index}, retrying in 5 seconds")
            self.memu.send_key(self.index, None, "home")
            time.sleep(5)
        return False

    def reset_instance(self):
        self.memu.stop(self.index, None, False)
        self.memu.remove(self.index, None)
        self.memu.create("76")
        self.memu.randomize(self.index, self.name)
        self.memu.set_configex(self.index, None, "custom_resolution", "1600 1000 300")
        self.memu.set_configex(self.index, None, "enable_su", "1")
        self.memu.set_configex(self.index, None, "memory", "2048")
        self.memu.set_configex(self.index, None, "cpus", "1")
        self.memu.set_configex(self.index, None, "enable_audio", "0")
        self.memu.start(self.index, None, False, False, None) #index name, headless, taskid, timeout


    #def reset_msp_memu_instance(self):
    def wait_msp_main_login(self):
        wait_main_page = True
        while wait_main_page:
            #print(f"{self.index} is waiting for danish main login page")
            if "LOG IND" in self.ocr_display_to_text("dan", True, True, False, False, 1239, 137, 1441, 196):
                wait_main_page = False
            time.sleep(2)

    def set_msp_server_region(self):
        self.memu.adb(self.index, None, "shell input tap 1392 251")
        self.memu.adb(self.index, None, "shell input tap 1408 659")
        self.memu.adb(self.index, None, "shell input tap 1408 659")
        self.memu.adb(self.index, None, "shell input tap 223 513")
        time.sleep(5)

    def verify_msp_server_region(self):
        self.memu.adb(self.index, None, f"shell screencap -p /sdcard/screenshot{self.index}.png")
        self.memu.adb(self.index, None, f'pull "/sdcard/screenshot{self.index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"')
        if "PRIVACY POLICY" in self.ocr_display_to_text("eng", True, False, True, True, 1234, 913, 1559, 966).strip():
            print(f"{self.index} is ready to hack!")
        

    def ocr_display_to_text(self, image_lang, cropped=False, filtered=False, pointed=False, enhanced=False, x1=None, y1=None, x2=None, y2=None):
        self.memu.adb(self.index, None, f"shell screencap -p /sdcard/screenshot{self.index}.png")
        self.memu.adb(self.index, None, f'pull "/sdcard/screenshot{self.index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"') # CHANGE_ME
        #self.pictures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Pictures')
        #self.image_path = os.path.join(pictures_dir, f"screenshot{self.index}.png")
        #image_to_text(self, image_name, image_lang="eng", cropped=False, filtered=False, pointed=False, enhanced=False, x1=None, y1=None, x2=None, y2=None)
        text = self.ocr.image_to_text(self.image_path, image_lang, cropped, filtered, pointed, enhanced, x1, y1, x2, y2) #check main menu text
        #print(f"{self.index} {text}")
        return text


def setup_instance(memu, ocr, index, name=None, apk="", package_name=""):
    username = "vials"
    password = "vials123"
    #start(self, index, name=None, headless=False, wait_for_taskid=True, timeout=False)
    print(memu.start(index, None, False, True, None)) #name, headless, taskid, timeout
    screenChecked = True
    while screenChecked:
        checkScreenError = memu.dumpScreenView(index)
        if checkScreenError:
            memuLauncherFix = bs(checkScreenError.split("\n")[2], "lxml")
            for content in memuLauncherFix.find_all("node"):
                if "MEmu Launcher2 has stopped" in content["text"]:
                    memu.syscallOut("memuc -i {index} adb shell input tap 400 400")
                    time.sleep(10)
                elif "MEmu Launcher2 isn't responding" in content["text"]:
                    memu.syscallOut("memuc -i {index} adb shell input tap 600 420")
                elif "Search Games and Apps" in content["text"]:
                    screenChecked = False
        else:
            print(f"[{Fore.RED}-{Fore.WHITE}] Failed to dump screen 0, retrying in 10 seconds")
            time.sleep(10)
    print(memu.uninstall_apk(index, name, package_name))
    print(memu.install_apk(index, name, apk))
    memu.adb(index, name, "shell monkey -p air.MSPMobile -c android.intent.category.LAUNCHER 1")
    time.sleep(30)
    #memuc adb -i 0 shell screencap -p /sdcard/screenshot.png
    memu.adb(index, name, f"shell screencap -p /sdcard/screenshot{index}.png")
    memu.adb(index, name, f'pull "/sdcard/screenshot{index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"')
    pictures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Pictures')
    image_path = os.path.join(pictures_dir, f"screenshot{index}.png")
    #print(ocr.image_to_text(image_path, "dan"))
    ocr.image_to_text(image_path, "dan", True, True, False, False, 1239, 137, 1441, 196) #check main menu text
    memu.adb(index, None, "shell input tap 1392 251")
    memu.adb(index, None, "shell input tap 1408 659")
    memu.adb(index, None, "shell input tap 1408 659")
    memu.adb(index, None, "shell input tap 223 513")
    time.sleep(10)
    #image_to_text(self, image_name, image_lang="eng", cropped=False, filtered=False, pointed=False, enhanced=False, x1=None, y1=None, x2=None, y2=None)
    memu.adb(index, name, f"shell screencap -p /sdcard/screenshot{index}.png")
    memu.adb(index, name, f'pull "/sdcard/screenshot{index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"')
    ocr.image_to_text(image_path, "eng", True, False, True, True, 1234, 913, 1559, 966) # check login page text
    memu.adb(index, None, "shell input tap 1361 294") #tap username box
    memu.memuc_input(index, None, username) #input username
    memu.adb(index, None, "shell input tap 1380 375") #tap password box
    memu.memuc_input(index, None, f"{password}!") #input password
    memu.adb(index, None, "shell input tap 1393 766") #tap login button
    time.sleep(5)
    memu.adb(index, name, f"shell screencap -p /sdcard/screenshot{index}.png")
    memu.adb(index, name, f'pull "/sdcard/screenshot{index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"')
    #print(ocr.image_to_text(image_path, "eng", True, False, True, True, 874, 260, 1219, 323).replace("\n", " "))
    if "INVALID USERNAME OR PASSWORD" in ocr.image_to_text(image_path, "eng", True, False, True, True, 874, 260, 1219, 323).replace("\n", " "):
        print(f"Wrong password to: {username}")
    memu.adb(index, None, "shell input tap 1380 375") #tap password box
    memu.adb(index, None, "shell input tap 1551 366") #clear password field
    memu.memuc_input(index, None, password) #input password
    memu.adb(index, None, "shell input tap 1393 766") #tap login button
    time.sleep(10)
    memu.adb(index, name, f"shell screencap -p /sdcard/screenshot{index}.png")
    memu.adb(index, name, f'pull "/sdcard/screenshot{index}.png" "C:\\Users\\vials\\Desktop\\Reversing\\Memu_Instance_Handler\\Pictures"')
    if "Messages" in ocr.image_to_text(image_path, "eng", True, False, True, True, 256, 955, 356, 971):
        print(f"Successfully logged into: {username}:{password}")


if __name__ == "__main__":
    memu = memu_instance_handler.MemuInstanceHandler()
    ocr = ocr_screen_handler.OCRScreenHandler()
    msp = MSPHandler()
    memuVersion = "76"
    new_instances = False

    #new_instances = False
    new_instances = True
    #for _ in range(4):
    #    if "SUCCESS: create vm finished." in memu.create(memuVersion):
    #        print(f"Successfully created memu instance with version: {memuVersion}")
            
    x_axis_geometry = 0
    vm_list = memu.list_vms().splitlines()
    for line in vm_list[:-1]:
        index = line.split(',')[0]
        name = line.split(',')[1]
        thread = MSPThread(memu, ocr, msp, f"{x_axis_geometry} 450 200 200", index, name, new_instances=new_instances)
        thread.start()
        x_axis_geometry += 250
        #print(f"Index: {line.split(',')[0]} Name: {line.split(',')[1]}")
        #set_minimal_settings(memu, line.split(',')[0], None)
        #memu.start(index, None, False, True, None)

    try:
        while msp.running:
            time.sleep(1)
    except KeyboardInterrupt:
        msp.running = False
        pass
    memu.stopall()
    print("Closing MSP script")
    
