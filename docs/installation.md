# Installation
## Preparation
If you are the average user with no prior experience with Linux, you generally want to use WSL. Windows Subsystem for Linux is a Windows 10 tool that allows users to run a light instance of linux on their own computer without having to set up a complicated virtual machine or a separate server running Linux. In order to use Talos you will need the following:
- A windows 10 PC with WSL enabled
- Ubuntu 18.04 LTS installed on WSL

For a guide on getting this ready I suggest following the manual method found in [this guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10#manual-installation-steps). Make sure to select *Ubuntu 18.04* in step 6.

Once you have everything ready open up Ubuntu by opening the Start Menu and typing in Ubuntu 18.04 and selecting the first option. Follow instructions until you reach a prompt. To make sure your system is up to date run the following two commands:
```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

## Automatic script
### Get the right folder
Because this guide assumes no prior knowledge of Linux, we wrote a small script that will create a directory names Talos in the currently selected directory to install Talos to. If you are running WSL solely for the purposes of using Talos, it is recommended to install Talos in the home directory. If your prompt has a tilde (~) before the dollar sign ($) then you are at the home directory.

> **NOTE:** *In Linux, home directories are user-specific directories located in /home/your-username/. In my instance, as my user is named holtder, my home directory is /home/holtder/. For ease of use, linux has a wildcard to quickly access the home directory of the user that is currently logged in, the tilde (~).*

This is where you want to be:

![image](https://user-images.githubusercontent.com/1879915/111901355-e5502000-8a37-11eb-9870-bc012dbcf6b4.png)

In this image you can see that the prompt is currently located at the "*wrongdirectory*" directory.

![image](https://user-images.githubusercontent.com/1879915/111901409-5394e280-8a38-11eb-9ba1-3d8a15f1294f.png)

Solve this by using the following command
```bash
$ cd ~
```

![image](https://user-images.githubusercontent.com/1879915/111901395-33fdba00-8a38-11eb-83da-41606c2efee6.png)

### Starting the script
From the WSL prompt, use the following command:
```bash
$ source <(curl -s https://raw.githubusercontent.com/Holtder/Talos/master/installtaloswsl.sh)
```

Notice how the filename is "install talos **wsl**". If you are running a virtual machine use installtalos.sh.

### Installing prerequisites
Next you will be presented with the following prompt:

![image](https://user-images.githubusercontent.com/1879915/111901959-3ca3bf80-8a3b-11eb-8bb1-e9322631d4c4.png)

If you have read and done everyting that is suggested in this guide up to this point, you can accept this prompt without worries. If you forgot to use the update/upgrade commands, this script will crash and the Ubuntu windows will close.

This script requires administrator priviliges as it will install prerequisite packages and programs on your system, on the following prompt, enter the password you defined when configuring WSL/Ubuntu.

![image](https://user-images.githubusercontent.com/1879915/111902013-85f40f00-8a3b-11eb-95d2-9ab34ab46a77.png)

### Creating the folder and downloading the files
The next step the script will perform for you is the downloading (cloning) of all the relevant files you need for running talos and placing them in the right folder. Read the prompt as presented and accept.

![image](https://user-images.githubusercontent.com/1879915/111902241-c902b200-8a3c-11eb-891c-8364945430c3.png)


### Starting Talos from WSL

