# attendance_management_bot
### reference information
#### ref: http://www.tornadoweb.org
####      https://minzkraut.com/2016/11/23/making-a-simple-spritesheet-generator-in-python
### The default deployment path is ~/oneapp_samplebot_attendance_management_bot/attendance_management_bot, and if you want to change the deployment path, please modify the configuration file
#### setting.py
### Using the default irteam user to boot by default 
### python version 3.6.3

1. install miniconda3(python3.6 env) to ~/miniconda3; add ~/miniconda3/bin to $PATH;
   refer https://conda.io/miniconda.html 
   
2. install the modules in requirements.txt to python3
   refer https://pip.pypa.io/en/stable/user_guide/#installing-packages

3. clone this repository
    https://oss.navercorp.com/works-mobile/oneapp_samplebot_calendar.git

4. modify conf/config.py

5. sh autoInit.sh

6. simple running
   python main.py --port=8080 --daemonize True

# document
[here](https://pages.oss.navercorp.com/works-mobile/oneapp_samplebot_attendance_management_bot/)
```
cd doc/

make markdown
ls _build/markdown/

make html
sphinx-serve
cp -R _build/html/* ../docs/
```
