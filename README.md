# Visualization Term Project: Visualization of Tube-Thinning Data #

# How To Run #

All instructions are to be performed in the project root directory. It could potentially
work in a Windows environment, though I have only tried it on Ubuntu 18.04.

## Install Python 3 ##
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Installing Dependencies ##
### Virtual Environment ###
**To install pipenv:**
```bash
pip3 install --user pipenv
```

After installing pipenv, navigate to your project root and do the following to set it up:
```bash
pipenv install
pipenv shell
```

## Running ##
First, make `project.py` executable (if it isn't already).
```bash
chmod +x tube_vis.py
```

Now run in the `pipenv`:
```bash
pipenv run ./tube_vis.py
```
