# COMP3000 Computing Project

# Audio Authentication via Voice Recognition on QTrobot (AAVR)

---

## Supervisor

> [Dr Hai-Van Dang - University of Plymouth](https://www.plymouth.ac.uk/staff/hai-van-dang)

---

## Resources

| Github Repository | https://github.com/greatyarn/COMP3000_Computing_Project                                        |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| Trello            | https://trello.com/invite/b/stCxAKF8/bacc4ca9cf8aefa46403a2451d15e98f/comp3000computingproject |
| creative commons  | https://creativecommons.org/                                                                   |
| LuxAI             | https://luxai.com/robot-for-teaching-children-with-autism-at-home/                             |
| ROS Robots        | https://robots.ros.org/qtrobot/                                                                |
| GanttProject      | https://www.ganttproject.biz/                                                                  |

---

## Project Vision

The QTrobot is a toddler-like humanoid robot built by LuxAI. This project, Audio Authentication via Voice Recognition on QTrobot, or AAVR for short, aims at providing two-factor authentication for the QTrobot which is a social robot that is originally used as an autism robot tutor for improving a child’s learning outcome at home (Qtrobot, n.d.) This authentication process with the use of a human voice and SMS allows for patients to retrieve their medical records, which might contain their age, height, and weight. This method of authenticating by voice is more convenient as it reduces the amount of human interaction that is needed.

---

## How to run the project

```batch
::Creating the Package and installing dependencies
::These commands allows you to create the package 
cd ~/catkin_ws/src
catkin_create_pkg AAVR rospy roscpp -D "AAVR"
::Within AAVR, copy all the files from the repository to the newly created folder.
::Within the repository folder in catkin_ws, run the requirements command with
pip install -r requirements.txt

::Creating .env file
::Command to create a blank .env file
touch .env

::Then, edit the file with this command
nano .env

::Template below for .env
EMAILSEND="Write which email you would like to send from here"
EMAILPASS="Write the email pass here, needs to be app password"
COMPOSEUSER=root

::Building and running project
::Run this to build the project
catkin_make
::Then, from the AAVR folder run
chmod +x /src/main.py
::This is to give write access to the program.
rosrun AAVR main.py
::This command then allows the program to run.


```

---

<div>
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/greatyarn/COMP3000_Computing_Project">Audio Authentication via Voice Recognition on QTrobot</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/greatyarn">Gregory Kua Wee Leng</a> is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>
</div>