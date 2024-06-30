# AndAMR (RTL-AMR on Android)

Using an chroot environment such as UserLand we can download RTL-AMR, use the RTL-SDR blog RTL_TCP server and this app to display nice and 
clean RTL-AMR Result onto an android devices screen.

![Screenshot](https://github.com/SarahRoseLives/AndAMR/blob/master/rtlamr.jpg)


## Installation

* Install Userland or another chroot app
* Start an RTL-SDR blog driver app with port 1234
* Run the following script
___
wget https://raw.githubusercontent.com/SarahRoseLives/AndAMR/master/run_in_userland.sh

chmod +x run_in_userland.sh

sh run_in_userland.sh
___

Then Run the app apk in releases or /bin

