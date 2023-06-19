# Wordpress Setup Docker
A python script that sets up wordpress site using docker-compose

# Environment to run the script on
Linux (Ubuntu)

# General guidelines for running the script
1. Since the script makes changes to the **/etc/hosts** files, it requires to be run using the root privilege.
2. After cloning the script to a local repository, change the permissions of the script to all:<br>
   **chmod -R 777 ./wp_docker_setup.py**
3. This script assumes that python / python3 and pip are already installed in the Linux environment. If not, then they have to be     installed.
4. Make sure that proxy is enabled in the network settings of the virtual machine from which the script is being run.
5. Use Google chrome browser to browse the URL on which the site is deployed.
6. On the first run, the script will download multiple images from docker which may take time.

## Commands and Sub-commands
1. **Setup**<br>
To run the script: <br>**sudo python3 wp_docker_setup.py sitename**<br>
This will deploy a wordpress site at the mentioned <sitename>. Check the site address displayed on the terminal in Chrome browser.
Firefox can't be used for this case as it needs installation of some softwares for opening the site. The site might show an initial      message that: Database connection can't be established. However, this will resolve after a few seconds.

2. **Disable site**<br>
This sub-command will stop the containers and disable the site:<br>
  **sudo python3 wp_docker_setup.py disable**

3. **Enable disabled site**<br>
This sub-command will re-start the containers after the disable and enable the site:<br>
  **sudo python3 wp_docker_setup.py enable**
  
4. **Delete site**<br>
This sub-command will delete the site, associated docker containers and data folder created inside the repository from which the script is run:<br>
  **sudo python3 wp_docker_setup.py delete sitename**
