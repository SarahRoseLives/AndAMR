sudo apt update --fix-missing
sudo apt install golang-go wget -y
go install github.com/bemasher/rtlamr@latest
wget https://raw.githubusercontent.com/SarahRoseLives/AndAMR/master/pipe_rtlamr.py
chmod +x pipe_rtlamr.py
python3 pipe_rtlamr.py