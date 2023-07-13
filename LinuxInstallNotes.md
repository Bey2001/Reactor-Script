- Installing on the desktop tower set up by Brad
  - Runs Ubuntu 22.04

# Installing Firefox

- Software Center should have it available

# Downloading Visual Studio Code

- Software Center should also have this available

# Downloading git

- Should already come on the machine

# Downloading npm and Node.js

- Run `sudo apt-get install nodejs` on a terminal
  - Enter your password if prompted
  - Run `sudo apt install node`
    - Should take a bit
    - Check with `which npm`
      - Should be something along the lines of `/usr/bin/npm`

# Downloading (Ana)Conda

- Go to https://docs.anaconda.com/anaconda/install/linux/
  - Run the appropriate installation command for your Linux flavor
    - If Ubuntu, run the Debian version
    - Follow the remaining directions from there
      - Verify the installation using the methods they recommend at Step 13 (As of 4/7/2023)

# Cloning from Git

- Need to access the files from the GitHub link
  - Assuming you have Git open, sign into the VTReactorDesign GitHub account in a web browser
    - Click the CLONE button, then copy from the HTTPS tab the link to download
      - Open a terminal and enter `git clone <pasted link from web browser>`
      - This will download the entire repo to your local machine, so make sure you are in the current directory you want to download it into
        - If you want to go to a different directory, use `ls` to see the contents of your current directory (folder)
        - To change directories, use `cd` followed by the path you want to change to
          - To access the parent directory, use `cd ..`

# Running the Frontend

- Only operate this once npm and node have both been downloaded
  - Need to install the node_modules directories, and certain modules
  - Run:
    - `npm install mui`
    - Every other module should also install due to the package-lock.json file that is already in the directory
  - Next, go to the Reactor-Script/frontend directory
    - Run `npm start`
    - You should not be getting any issues at this point, but may be prompted to download more files

# Running the Backend

- Only operate once conda has been downlaoded
  - Need to install dependencies and modules
    - Run `conda create -n reactors`
      - This will create a new Python environment that can be altered without affecting any other environments or versions
      - Run `conda install -n reactors numpy scipy matplotlib flask flask-cors flask-restful`
      - Enter y when prompted
  - Once your dependencies are installed, go into the Reactor-Script/backend directory
    - Run `conda activate reactors`
      - You should now see (reactors) preceding your shell prompt
      - Run `flask run`
