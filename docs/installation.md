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

This is where you want to be:

![image](https://user-images.githubusercontent.com/1879915/111901355-e5502000-8a37-11eb-9870-bc012dbcf6b4.png)

In this image you can see that the prompt is currently located at the "*wrongdirectory*" directory.

![image](https://user-images.githubusercontent.com/1879915/111901409-5394e280-8a38-11eb-9ba1-3d8a15f1294f.png)

Solve this by using the following command
```bash
$ cd ~
```

![image](https://user-images.githubusercontent.com/1879915/111901395-33fdba00-8a38-11eb-83da-41606c2efee6.png)

### Using the script
From the WSL prompt, use the following command:
```bash
$ source <(curl -s https://raw.githubusercontent.com/Holtder/Talos/master/installtaloswsl.sh)
```

Notice how the filename is "install talos **wsl**". If you are running a virtual machine use installtalos.sh.

### Starting Talos from WSL

