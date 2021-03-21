# Installation
## Before you start
This guide requires the use of WSL. In the next section will elaborate more on that, but it is wise to get familliar with the elements of the WSL terminal first:

![image](https://user-images.githubusercontent.com/1879915/111908655-5274ad00-8a5a-11eb-9ab7-d3afcd8151e5.png)

| Element         | Purpose                                                                                                                                              |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| username        | Linux has users, just like Windows. This is the name you chose when you first set up WSL.                                                            |
| ComputerName    | When Windows is installed to a PC or laptop, it assigns a name to it. In Linux, the name of the pc is shown after the username with an @ in between. |
| ~/DirectoryName | Whenever you make/do anything in WSL, it happens in a directory/folder. The blue text shows which folder is currently active.                        |
| $               | Anything you type will appear after this dollar sign. In this guide several commands will be supplied to copy in the WSL window, enter those here.   |

> **NOTE:** *In WSL, copy and paste are not assigned to CTRL+C and CTRL+V. If you want to paste something in WSL, you have to press the right mouse button. Then press Enter to confirm.*

## Preparation
If you are the average user with no prior Linux experience, you generally want to use the Windows Subsystem for Linux (WSL). WSL is a Windows 10 tool that allows users to run a light instance of Linux on their own computer without having to set up a complicated virtual machine or a separate server running Linux. In order to use Talos you will need the following:
- A windows 10 PC with WSL enabled
- Ubuntu 18.04 LTS installed on WSL

For a guide on getting this ready I suggest following the manual method found in [this guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10#manual-installation-steps). Make sure to select *Ubuntu 18.04* in step 6.

Once you have everything ready start Ubuntu by opening the Start Menu and typing in Ubuntu 18.04 and selecting the first option. Follow instructions until you reach a prompt. To make sure your system is up to date run the first command, then the second:
```bash
sudo apt-get update
sudo apt-get upgrade
```
> **NOTE 1:** *As mentioned above, copy each command and paste it into WSL by clicking the right mouse button on the WSL window.*
> **NOTE 2:** *In Linux, administrator accounts are referred to as super-users. The first word of each line, sudo, stands for "super-user do". Everything written after this word is executed with administator privileges. If you are asked for the password you defined when setting up WSL, please do so.*

## Automatic script
Because this guide assumes no prior knowledge of Linux, we wrote a small script that will install Talos in the current user's home directory.

> **NOTE:** *In Linux, home directories are user-specific directories located in /home/your-username/. In my instance, as my user is named holtder, my home directory is /home/holtder/. For ease of use, linux has a wildcard to quickly access the home directory of the user that is currently logged in, the tilde (~).*

### Starting the script
From the WSL prompt, use the following command:
```bash
source <(curl -s https://raw.githubusercontent.com/Holtder/Talos/master/installtaloswsl.sh)
```

You will be presented with the following:

![image](https://user-images.githubusercontent.com/1879915/111909326-20b11580-8a5d-11eb-8ee5-b3656d60df10.png)

Type "1" and press "Enter" to confirm.

### Installing prerequisites
Next you will be presented with the following prompt:

![image](https://user-images.githubusercontent.com/1879915/111901959-3ca3bf80-8a3b-11eb-8bb1-e9322631d4c4.png)

If you have read and done everyting in this guide up to this point, you can accept this prompt without worries. If you forgot to use the update/upgrade commands, this script will crash and the Ubuntu windows will close.

> **WARNING:** *This script requires administrator priviliges as it will install prerequisite packages and programs on your system, if asked, enter the password you defined when configuring WSL/Ubuntu.*

![image](https://user-images.githubusercontent.com/1879915/111902013-85f40f00-8a3b-11eb-95d2-9ab34ab46a77.png)

### Creating the folder and downloading the files
The next step the script will perform for you is the downloading (cloning) of all the relevant files you need for running talos and placing them in the right folder. Read the prompt as presented and accept.

![image](https://user-images.githubusercontent.com/1879915/111902241-c902b200-8a3c-11eb-891c-8364945430c3.png)

Let the installer run it's course, you will know this if you are presented with the following prompt:

![image](https://user-images.githubusercontent.com/1879915/111902301-36aede00-8a3d-11eb-9754-f36013ccbd77.png)

**Congratulations**, Talos is now successfully installed on your instance of Ubuntu.

## Starting Talos
In WSL, type the following:
``` bash
talos-server
```

You will be presented wit


