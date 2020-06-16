# workloader
A tool to control WorkloadWisdom.
1. [History](#history)
2. [Author](#author)
3. [Download](#download)
    1. [Bootstrap-install-on-linux](#bootstrap-install-on-linux)
    2. [Uninstall](#uninstall)
    3. [Manual-download-and-install](#manual-download-and-install)
4. [Usage](#usage)
    1. [Use-the-workloader](#use-the-workloader)
    2. [Use-the-lib-only](#use-the-lib-only)
5. [Documentation](#documentation)

```
                      __   .__                    .___
 __  _  _____________|  | _|  |   _________     __| _/___________
 \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
                          \/               \/      \/    \/
    Copyright (c) 2018 Stephen Shao <Stephen.Shao@emc.com>
```

    
----

# History
July 2019, v1.1.3:
- implement list/show an iteration suite
- implement list/show/start/stop an iteration test suite
- bug fixing

Apr 2019, v1.1.2:
- AR#999302

Dec 2018, v1.1.1:
- implement stop test by project name function
- bug fixing

Nov 2018, v1.1.0:
- implemented composite workloads

Oct 2018, v1.0.1:

- a workLoader tool is provided

- bootstrap for linux

Oct 2018, v1.0.0:

- implemented generator related API

- implemented test_bed related API

- implemented most workloads(formerly projects) related API

- implemented most tests related API

----
# Author
<i>
<h4>Stephen Shao</h4>
<h4>SPE DevOps CEV China</h4>
</i>

----
# Download
## Bootstrap-install-on-linux

**Preferred.**

From your linux client, just copy & paste below and enter:

```bash
curl http://10.228.32.103:8888/install.sh|sh -
```

Examples:
```bash
[root@filetigerteam ~]# curl http://10.228.32.103:8888/install.sh|sh -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   381  100   381    0     0   119k      0 --:--:-- --:--:-- --:--:--  372k
INFO: Download workloader tool.
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 18050  100 18050    0     0  12.9M      0 --:--:-- --:--:-- --:--:-- 17.2M
workloader/
workloader/.workloaderascii
workloader/bootstrap.sh
workloader/workLoader.py
workloader/workloader-1.0.1-py2.py3-none-any.whl
INFO: Install workloader tool.

    ############################################

    USAGE: /opt/workloader/bootstrap.sh install|clean]

    ############################################


========================================================
                      __   .__                    .___
 __  _  _____________|  | _|  |   _________     __| _/___________
 \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
                          \/               \/      \/    \/
    Copyright (c) 2018 Stephen Shao <Stephen.Shao@emc.com>
========================================================

Processing ./workloader-1.0.1-py2.py3-none-any.whl
Collecting requests (from workloader==1.0.1)
  Downloading https://files.pythonhosted.org/packages/f1/ca/10332a30cb25b627192b4ea272c351bce3ca1091e541245cccbace6051d8/requests-2.20.0-py2.py3-none-any.whl (60kB)
    100% |################################| 61kB 179kB/s
Collecting urllib3<1.25,>=1.21.1 (from requests->workloader==1.0.1)
  Downloading https://files.pythonhosted.org/packages/8c/4b/5cbc4cb46095f369117dcb751821e1bef9dd86a07c968d8757e9204c324c/urllib3-1.24-py2.py3-none-any.whl (117kB)
    100% |################################| 122kB 542kB/s
Requirement already up-to-date: chardet<3.1.0,>=3.0.2 in /usr/lib/python2.7/site-packages (from requests->workloader==1.0.1)
Requirement already up-to-date: idna<2.8,>=2.5 in /usr/lib/python2.7/site-packages (from requests->workloader==1.0.1)
Requirement already up-to-date: certifi>=2017.4.17 in /usr/lib/python2.7/site-packages (from requests->workloader==1.0.1)
Installing collected packages: urllib3, requests, workloader
  Found existing installation: urllib3 1.23
    Uninstalling urllib3-1.23:
      Successfully uninstalled urllib3-1.23
  Found existing installation: requests 2.19.1
    Uninstalling requests-2.19.1:
      Successfully uninstalled requests-2.19.1
Successfully installed requests-2.20.0 urllib3-1.24 workloader-1.0.1
You are using pip version 9.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
INFO: Dryrun workloader tool.
Fri, 19 Oct 2018 10:56:48 workLoader.py[line:251] INFO
                      __   .__                    .___
 __  _  _____________|  | _|  |   _________     __| _/___________
 \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
                          \/               \/      \/    \/
    Copyright (c) 2018 Stephen Shao <Stephen.Shao@emc.com>

usage: workLoader.py [-h] [-d IP] -u USERNAME -p PASSWORD
                     {generator,workload,testbed,test} ...
workLoader.py: error: too few arguments
```

----
# Uninstall

```bash
[root@vx-d1207-dm4cge1 opt]# cd /opt/workloader/
[root@vx-d1207-dm4cge1 workloader]# ./bootstrap.sh clean

========================================================
                      __   .__                    .___
 __  _  _____________|  | _|  |   _________     __| _/___________
 \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
                          \/               \/      \/    \/
========================================================

Uninstalling workloader-1.0.1:
  Successfully uninstalled workloader-1.0.1
You are using pip version 9.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

```
## Manual-download-and-install
Not preferred.

* Visit to get the latest wheel: http://10.228.32.103:8888/workloader/

* Download the latest tool: http://10.228.32.103:8888/workloader/workLoader.py


```bash
sudo pip install workloader
```

----
# Usage
## Use-the-workloader

**This is the preferred way of using workloader.**

Top level arguments:

```bash
C:\workloader>python workloader.py -u username -p password -h
usage: workloader.py [-h] [-d IP] -u USERNAME -p PASSWORD
                     {generator,workload,testbed,test} ...

positional arguments:
  {generator,workload,testbed,test}
                        Workloader Command help
    generator           Generator Module
    workload            Workloads Module
    testbed             Testbeds Module
    test                Tests Module

optional arguments:
  -h, --help            show this help message and exit
  -d IP, --ip IP        WorkloadWisdom IP
  -u USERNAME, --username USERNAME
                        WorkloadWisdom Username
  -p PASSWORD, --password PASSWORD
                        WorkloadWisdom Password
```

Generator Module

```bash
C:\workloader>python workloader.py -u username -p password generator -h
usage: workloader.py generator [-h] {list,show} ...

positional arguments:
  {list,show}  Action to perform
    list       List of generators
    show       Show a generator

optional arguments:
  -h, --help   show this help message and exit
```

Workload Module

```bash
C:\workloader>python workloader.py -u username -p password workload -h
usage: workloader.py workload [-h] {list,private,show,delete,clone} ...

positional arguments:
  {list,private,show,delete,clone}
                        Action to perform
    list                List of workloads
    private             Private a workload
    show                Show a workload
    delete              Delete a workload
    clone               Clone a workload

optional arguments:
  -h, --help            show this help message and exit
```

Testbed Module

```bash
C:\workloader>python workloader.py -u username -p password testbed -h
usage: workloader.py testbed [-h] {list,private,show,delete,clone} ...

positional arguments:
  {list,private,show,delete,clone}
                        Action to perform
    list                List of testbeds
    private             Private a testbed
    show                Show a testbed
    delete              Delete a testbed
    clone               Clone a testbed

optional arguments:
  -h, --help            show this help message and exit
```

Test Module

```bash
C:\workloader>python workloader.py -u username -p password test -h
usage: workloader.py test [-h] {list,show,start,stop} ...

positional arguments:
  {list,show,start,stop}
                        Action to perform
    list                List of tests
    show                Show a test
    start               Start a test
    stop                Stop a test

optional arguments:
  -h, --help            show this help message and exit
```

Composite Workload Module

```bash
C:\workloader>python workloader.py -u username -p password composite -h
usage: workloader.py composite [-h] {list,private,show,delete,clone} ...

positional arguments:
  {list,private,show,delete,clone}
                        Action to perform
    list                List of composite workloads
    private             Private a composite workload
    show                Show a composite workload
    delete              Delete a composite workload
    clone               Clone a composite workload

optional arguments:
  -h, --help            show this help message and exit
```


Iteration Suite Module

```bash
C:\workloader>python workloader.py -u username -p password iteration -h
usage: workloader.py iteration [-h] {list,show,start,stop} ...

positional arguments:
  {list,show,start,stop}
                        Action to perform
    list                List of Iteration suites
    show                Show an Iteration suite
    start               Start an Iteration test suite
    stop                Stop a Iteration test suite

optional arguments:
  -h, --help            show this help message and exit
```


Examples:
```bash
python workloader.py -u username -p password generator list
python workloader.py -u username -p password generator show -name 'xxx'

python workloader.py -u username -p password workload list
python workloader.py -u username -p password workload show -name 'xxx'
python workloader.py -u username -p password workload clone -old 'xxx' -new 'yyy'

python workloader.py -u username -p password testbed show -name 'aaa'
python workloader.py -u username -p password testbed clone -old 'xxx' -new 'yyy'

python workloader.py -u username -p password test show -id 'bbb'
python workloader.py -u username -p password test start -project 'name' -testbed 'name' -duration 100

python workloader.py -u username -p password composite list
python workloader.py -u username -p password composite show -name 'xxx'
python workloader.py -u username -p password composite clone -old 'xxx' -new 'yyy'

python workloader.py -u username -p password iteration list
python workloader.py -u username -p password iteration show -name 'xxx'
python workloader.py -u username -p password iteration start -name 'xxx' -testbed 'yyy'
python workloader.py -u username -p password iteration stop -id 'xxx'
python workloader.py -u username -p password iteration stop -name 'xxx'
```

----
## Use-the-lib-only

Not suggested, but here are the examples:

```python
from workloader.workloadwidsom import WorkloadWisdom
    
ww = WorkloadWisdom('http://10.123.123.123', 'username', 'password')
# show version
ww.get_version()
# list appliances
appliance = ww.get_appliance_by_name(name='dur_app_003')

# list test_beds
ww.list_testbeds()

# get a test_bed by name
tb = ww.get_testbed_by_name("Stephen_LDX_005_VLAN590_OB-D1494")

# change test_bed privacy
ww.set_testbed_privacy("5ba0a41d421aa90bfaa7e322", private=True)

# clone a test_bed
tb_new = ww.clone_testbed(tb['id'], new_name='STEPHEN')

# delete a test_bed
ww.delete_testbed(testbed_id=tb_new['id'])

# list of tests
ww.list_tests()

# show a test
ww.show_test("5bbed2b6421aa947292321de")

# stop a test
ww.stop_test("5bbed2b6421aa947292321de")

# list of projects
list = ww.list_projects()

# list of library projects
ww.list_projects(library=True)

# get a project by name
proj = ww.get_project_by_name("OB-D1494_800GB_MUP", list)

# clone a project
proj_new = ww.clone_project(proj['id'], "OB-D1494_automation_debug_clone")

# start a test by test name and test_bed name
test = ww.start_test_by_name("OB-D1494_automation_debug_clone", "Stephen_LDX_005_VLAN590_OB-D1494", "600")

# wait until test complete
ww.wait_until_test_complete(test['id'])

# save all available test results into files, e.g. logs, trace, summary, export_charts, config
ww.save_all_test_results(test)

# delete projects
ww.delete_project(proj["id"])
```

----
# Documentation
[API Doc](http://10.228.32.103:8888/src/docs/build/html/genindex.html)