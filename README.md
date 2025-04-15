# Fetch_Take_Home_exercise
My Submission for the Fetch SRE take home exercise.
### Prerequisite for Installation
1. The first thing you need for this project is to install git. Go to the link below and follow the instructions on installing git.
For Windows users this should also download the ***git bash*** application which we will use later as our terminal.
https://git-scm.com/downloads


2. Next we need to download python on to our machines.
- **(Mac Users)** For  Mac users I suggest going onto https://www.python.org/downloads/ and downloading version 3.13. It
should be in a big yellow box. Once downloaded open the file and follow the installation process.
- **(Windows users)**  For Windows users open the microsoft store application and search for **Python 3.13**. 
then download it.

3. Now we must verify that we have both git and python  on our machines. 
- **(Mac users)** Open the ***terminal*** application. 
- **(Windows users)**  Open the ***git bash*** application that was downloaded when we installed git. We will use this as your terminal. 
- In  your terminal run the command `git -v` on your command line. It should now display the git version that your machine has.

4. Finally,  we need to verify that we have python on your machine. In the command line run the command `python --version` . It should display the version number
of python that you currently have. 
- If you get a response saying **"Command not found"** then try running this command `python3 --version` on
the command line. That should display your current version number of python.

### Downloading the files
1. In your terminal go to the desired location you wish to put this repository. You can do this by running the following command
`cd <your/desired/folder/location>`. Be sure to replace `<your/desired/folder/location>` with the actual desired path for the repository.


2. Now in your terminal run the command `git clone https://github.com/Preston-H-code/Fetch_Take_Home_exercise.git`. You should
now have the repository in your current folder.

### Installation and running the script
1. In your terminal run `cd <path/to/Fetch_Take_Home_exercise>` to go into project's folder. Be sure to replace `<path/to/Fetch_Take_Home_exercise>` with the actual path to the project's folder. Then run the command `pwd` to verify you are in the appropriate folder.

 
2. Now we must download the required packages for the code. 
- If you were able to verify your python installation by running `python --version` then run  `pip install -r requirments.txt`.
- If you were able to verify your python installation by running `python3 --version`  then run `pip3 install -r requirments.txt`. 
- This should download all the required packages for the script.


3. Finally, we can run the script. 
- If you were able to verify your python installation by running `python --version` ,then you can run the script with the command  `python main.py sample.yml`. 
- If you were able to verify your python installation by running `python3 --version`  ,then run the script with the command `python3 main.py sample.yml`. 
- You can replace **sample.yml** in the command line with a path to any valid yaml file that matches the structure of the sample file. 


## Issues and Fixes
### YAML Issues 
1. One of the first issues I noticed was with the handling of the yaml file. I noticed that there wasn't a check to see if the file existed, 
so I added a the `does_file_exist` function that would check that a file exist and is not a directory.


2. There also wasn't a check to ensure that the file was in fact a  yaml file. So that capability was added with the function `is_file_yaml`. 


3. The final issue I noticed with the yaml file was that the endpoint data wasn't verified. In the requirements it was stated that every endpoint was required to have a name and url. 
So the `is_config_valid` function was added to ensure that every endpoint has name and url.

### Check Health function changes
1. One of the requirements in the documentation was that the HTTP method would be set to GET if there wasn't a HTTP method given in the yaml. 
I added a default value of GET for the HTTP method in the `check_health` function to handle that.

 
2. I noticed that when a request had a body the request would fail when it wasn't supposed to. So I used the `json.loads()` function 
to change the body from a json object to a proper python object so that the HTTP request function could handle the body properly.
 
 
3. Finally, the requirements stated that the request should time out after 500ms. This led me to adding a time out parameter for the request.
 
### Monitor endpoints function changes
1. I wanted to ensure that there was a clear way to keep track of the amount of cycles that were run and when they took place. 
This led me to adding a parameter for the cycle number and adding timestamps at the beginning and end of each cycle. That way we keep track of the amount of cycles that have run and how long each cycle takes.

 
2. Another issue I noticed was with determining the domain. The original code removed the protocol and the page path, but not the subdomains and ports number.
My changes handled the removal of port numbers and subdomains.
- So a URL like `https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error` **domain** would be ``fetchrewards.com`` instead of ``dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com``
- and a URL like `http://localhost:8080/status` **domain** would be `localhost` instead of `localhost:8080`

3. In the requirements the cycles were required to run every 15 second regardless of the amount of endpoints and their response times. 
The issue with the original implementation  of the `monitor_endpoints`  function is that it would have to check all the endpoints before it waited 15 seconds.
In the event that there are a bunch of endpoints to check and checking them takes a long time, the cycles will be delayed and not run every 15 seconds. To fix this I created a function called 
`run_monitor` that runs the `monitor_endpoints` function in a thread. `run_monitor` is then called in the main function every 15 seconds. This allows a cycle to begin every 15 seconds regardless of if a previous cycle is completed. 
