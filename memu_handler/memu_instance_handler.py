import subprocess as sp

class MemuInstanceHandler(object):
    def __init__(self):
        super(MemuInstanceHandler, self).__init__()

        self.running = False
        
    #GUEST COMMANDS

    def execute_command(self, index, name=None, guest_command=None):
        #<-n vmname | -i vmid> execcmd <guestcmd>
        #memuc -i 1 execcmd “getprop persist.sys.language"
        return False

    def install_apk(self, index, name=None, apk_file=None, package_name=None, shortcut=False):
        #installapp <-n vmname | -i vmid> <apkfile> [-s]
        #installapp <-n vmname | -i vmid> -p <packagename>
        command = "memuc installapp"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' "{apk_file}"' #full windows path
        if shortcut:
            command += " -s"
        return self.syscallOut(command)

    def uninstall_apk(self, index, name=None, package_name=""):
        #uninstallapp <-n vmname | -i vmid> <packagename> [-s xxx]
        command = "memuc uninstallapp"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {package_name}"
        return self.syscallOut(command)

    def startapp(self, index, name=None, package_activity=""):
        #startapp <-n vmname | -i vmid> <packageactivity>
        command = "memuc startapp"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {package_activity}"
        return self.syscallOut(command)

    def stopapp(self, index, name=None, package_name=""):
        #stopapp <-n vmname | -i vmid> <packagename>
        command = "memuc stopapp"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {package_name}"
        return self.syscallOut(command)

    def send_key(self, index, name=None, key_press=None):
        #sendkey <-n vmname | -i vmid> <back | home | menu | volumeup | volumedown>
        #memuc sendkey -i 0 home
        #SUCCESS: home finished.
        command = "memuc sendkey"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {key_press}"
        return self.syscallOut(command)

    def activate(self, index, name=None):
        #activate <-n vmname | -i vmid>
        command = "memuc activate"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def shake(self, index, name=None):
        #shake <-n vmname | -i vmid>
        command = "memuc shake"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def rotate(self, index, name=None):
        #rotate <-n vmname | -i vmid>
        command = "memuc rotate"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def reboot(self, index, name=None, wait_for_taskid=False):
        #reboot <-n vmname | -i vmid> [-t]
        command = "memuc reboot"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        if wait_for_taskid:
            command += " -t"
        return self.syscallOut(command)

    def connect(self, index, name=None):
        #connect <-n vmname | -i vmid>
        command = "memuc connect"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def disconnect(self, index, name=None):
        #disconnect <-n vmname | -i vmid>
        command = "memuc disconnect"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def memuc_input(self, index, name=None, text_input=""):
        #input <-n vmname | -i vmid> <text>
        command = "memuc input"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' "{text_input}"'
        return self.syscallOut(command)

    def set_gps(self, index, name, longitude=0, latitude=0):
        #setgps <-n vmname | -i vmid> <longitude> <latitude>
        #set gps -i 0 (-180, 180) (-180, 180)
        command = "memuc setgps"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {longitude} {latitude}"
        return self.syscallOut(command)

    def set_screen_lock(self, index, name=None, unlock=False): #add boolean value
        #setscreenlock <-n vmname | -i vmid> <0|1>
        command = "memuc setscreenlock"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {int(unlock)}"
            
        return self.syscallOut(command)

    def zoom_in(self, index, name=None):
        #zoomin <-n vmname | -i vmid>
        command = "memuc zoomin"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def zoom_out(self, index, name=None):
        #zoomout <-n vmname | -i vmid> ???
        command = "memuc zoomout"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def accelorometer(self, index, name=None, x=0.0, y=0.0, z=0.0):
        #accelerometer <-n vmname | -i vmid> <-x 0.0> <-y 8.9> <-z 4.5>
        command = "memuc accelerometer"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {x} {y} {z}"
        return self.syscallOut(command)

    def get_app_info_list(self, index, name=None):
        #getappinfolist <-n vmname | -i vmid>
        command = "memuc getappinfolist"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        print(command)
        return self.syscallOut(command)

    def create_shortcut(self, index, name=None, package_name=None):
        #createshortcut <-n vmname | -i vmid> <packagename>
        command = "memuc createshortcut"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {package_name}"
        print(command)
        return self.syscallOut(command)

    def network(self, index, name=None, vmip=None, vmmask=None, vmgateway=None, vmdns=None):
        #network <-n vmname | -i vmid> --ip vmip --mask vmmask --gateway vmgateway --dns vmdns
        command = "memuc network"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" --ip {vmip} --mask {vmmask} --gateway {vmgateway} --dns {vmdns}"
        return self.syscallOut(command)

    def upload_file(self, index, name=None, windows_file_path="", android_file_path=""):
        #uploadfile <-n vmname | -i vmid> -s windowsFilePath -d androidFilePath
        command = "memuc uploadfile"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' -s "{windows_file_path}" -d "{android_file_path}"'
        return self.syscallOut(command)

    def download_file(self, index, name=None, android_file_path="", windows_file_path=""):
        #downloadfile <-n vmname | -i vmid> -s androidFilePath -d windowsFilePath
        command = "memuc downloadfile"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' -s "{android_file_path}" -d "{windows_file_path}"'
        return self.syscallOut(command)

    def create_file(self, index, name=None, android_file_path=""):
        #createfile <-n vmname | -i vmid> <androidFilePath>
        command = "memuc createfile"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' "{android_file_path}"'
        return self.syscallOut(command)

    def remove_file(self, index, name=None, android_file_path=""):
        #removefile <-n vmname | -i vmid> <androidFilePath>
        command = "memuc removefile"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' "{android_file_path}"'
        return self.syscallOut(command)

    #ADB Commands

    def adb(self, index, name=None, adb_command=""):
        # <-n vmname | -i vmid> adb <adbcmd>
        command = "memuc adb"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f' "{adb_command}"'
        return self.syscallOut(command)
        

    #Multi-MEmu Management
    
    def create(self, version):
        #create [ovafile | ovadir]
        """
        x32 5.1 (51)
        x32 7.1 (71)
        x64 7.1 (76)
        x64 9.0 (90)
        x64 12.0 (120)
        """
        return self.syscallOut(f"memuc create {version}")
        

    def remove(self, index, name=None):
        #remove <-n vmname | -i vmid>
        #SUCCESS: delete vm finished.
        command = "memuc remove"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def clone(self, index, name=None, rename=None, wait_for_taskid=False):
        #clone <-n vmname | -i vmid> [-r nametag] [-t]
        command = "memuc clone"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        if rename:
            command += f' -r "{rename}"'
        if wait_for_taskid:
            command += f" -t"
        return self.syscallOut(command)

    def memu_export(self):
        #export <-n vmname | -i vmid> <ovafile> [-t]
        return False

    def memu_import(self):
        #import <ovafile> [-t]
        #import <memufile>
        return False

    def start(self, index, name=None, headless=False, wait_for_taskid=True, timeout=""):
        #start <-n vmname | -i vmid> [-b] [-t] [-e expiredtime]
        command = "memuc start"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        if headless:
            command += " -b"
        if wait_for_taskid:
            command += " -t"
        if timeout:
            command += f" -e {timeout}"
        return self.syscallOut(command)

    def stop(self, index, name=None, wait_for_taskid=True):
        #stop <-n vmname | -i vmid> [-t]
        command = "memuc stop"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        if wait_for_taskid:
            command += f" -t"
        return self.syscallOut(command)

    def stopall(self):
        #stopall
        #SUCCESS: stop all vms finished.
        return self.syscallOut("memuc stopall")

    def compress(self, index, name=None, wait_for_taskid=False):
        #compress <-n vmname | -i vmid> [-t]
        command = "memuc compress"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        if wait_for_taskid:
            command += " -t"
        return self.syscallOut(command)

    def list_vms(self):
        #listvms [--running] [-s] [--render] [--androidver] [-n vmname | -i vmid]
        return self.syscallOut(f"memuc listvms")
    
    def is_vm_running(self, index, name=None):
        #isvmrunning <-n vmname | -i vmid>
        #Running || Not Running
        command = "memuc isvmrunning"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    def sort_windows(self):
        #sortwin
        return self.syscallOut("memuc sortwin")

    def rename(self, index, name=None, title=None):
        #rename <-n vmname | -i vmid> <title>
        command = "memuc rename"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        command += f' "{title}"'
        print(command)
        return self.syscallOut(command)

    def task_status(self, taskid=None):
        #taskstatus <taskid>
        return self.syscallOut(f"memuc taskstatus {taskid}")

    def randomize(self, index, name=None):
        #randomize [-n vmname | -i vmid]
        #SUCCESS: change device attributes finished.
        command = "memuc randomize"
        if name:
            command += f' -n "{name}"'
        else:
            command += f" -i {index}"
        return self.syscallOut(command)

    #MEmu Config Management Advance

    def set_configex(self, index, name=None, key=None, value=None):
        #setconfigex <-n vmname | -i vmid> <key> <value>
        """
        General Options :
        <key>
           [cpus number]
           [memory memorysize in MB]
           [cpucap 1-100]
           [picturepath path]
           [musicpath path]
           [moviepath path]
           [downloadpath path]
           [is_full_screen 0|1]
           [is_hide_toolbar 0|1]
           [graphics_render_mode 0|1]
           [enable_su 0|1]
           [enable_audio 0|1]
           [fps 10|20|30|40|50|60]
           [vkeyboard_mode 0|1]
           [sync_time 0|1]
           [phone_layout 0|1|2]
           [start_window_mode 0|1]
           [win_x x]
           [win_y y]
           [win_scaling_percent2 0-100]
           [is_customed_resolution 0|1]
           [resolution_width width]
           [resolution_height height]
           [vbox_dpi dpi]
           [linenum +8617651413549]
           [imei 860504493831119]
           [imsi 460003811612558|auto]
           [ssid rgqiev662|auto]
           [simserial 11223344556677889900]
           [macaddress 11:22:33:44:55:66]
           [microvirt_vm_brand HUAWEI]
           [microvirt_vm_manufacturer HUAWEI]
           [microvirt_vm_model FRD-L19]
           [selected_map 0|1]
           [longitude 30.978785]
           [latitude 121.824455]
           [geometry x y width height]
           [custom_resolution width height dpi]
           [cache_mode 0|1]
           [disable_resize 0|1]
           [exit_option 0|1|2|3]
           [vbox_abi_mode 0|1]
           [disk_attach_mode 0|1]
        """
        command = "memuc setconfigex"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {key} {value}"
        return self.syscallOut(command)

    def get_configex(self, index, name=None, key=None):
        #getconfigex <-n vmname | -i vmid> <key>
        """
        General Options :
        <key>
           [cpus]
           [memory]
           [cpucap]
           [picturepath]
           [musicpath]
           [moviepath]
           [downloadpath]
           [is_full_screen]
           [is_hide_toolbar]
           [graphics_render_mode]
           [enable_su]
           [enable_audio]
           [fps]
           [vkeyboard_mode]
           [sync_time]
           [phone_layout]
           [start_window_mode]
           [win_x]
           [win_y]
           [win_scaling_percent2]
           [is_customed_resolution]
           [resolution_width]
           [resolution_height]
           [vbox_dpi]
           [linenum]
           [imei]
           [imsi]
           [ssid]
           [simserial]
           [macaddress]
           [microvirt_vm_brand]
           [microvirt_vm_manufacturer]
           [microvirt_vm_model]
           [selected_map]
           [longitude]
           [latitude]
           [geometry]
           [custom_resolution]
           [cache_mode]
           [disable_resize]
           [exit_option]
           [vbox_abi_mode]
           [disk_attach_mode]
        """
        command = "memuc getconfigex"
        if name:
            command += f" -n {name}"
        else:
            command += f" -i {index}"
        command += f" {key}"
        return self.syscallOut(command)

    def dumpScreenView(self, index, name=None):
        #def adb(self, index, name=None, adb_command=""):
        #command = f'{self.adb("0", None, "shell uiautomator dump")}'
        #print(command)
        dumpScreen = self.adb(index, None, "shell uiautomator dump")
        if dumpScreen:
            if "UI hierchary dumped to" in dumpScreen:
                #readXML = self.syscallOut(f"memuc -i {index} adb shell cat /storage/emulated/0/window_dump.xml", timeout=20)
                readXML = self.adb(index, None, "shell cat /storage/emulated/0/window_dump.xml")
                return readXML
        return False

    def syscallOut(self, command, timeout=5):
        try:
            return sp.run(command, capture_output=True, shell=True, timeout=timeout).stdout.decode("utf-8")
        except Exception as e:
            pass

