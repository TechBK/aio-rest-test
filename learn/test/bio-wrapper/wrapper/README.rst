==========================
Nguyen Quang "TechBK" Binh
==========================

.. contents::


Idea
====

1. Create file job.sh, job_defile.json
    - job.sh: la cac dong bash ma job phai thuc hien.
    - job_define.json:
        + first: if True, this job is maybe first. if False, nguoc lai
        + parameters: define number of parameters

2.


API
===

The following section describes the available resources in bio-wrapper JSON API.

/runtask/
---------
Create a job.

* Supported Request Methods: POST
* Parameters:
    - user (string, required): username
    - key (string, required): password
    - tenant (string, required): tenant name
    - container_name (string, unrequited):
    - authurl (string, required):
    - file_name (string, required): if None, it's firt step on WorkFlow

Example request:
::

    http://localhost:8080/runtask/

Example response:
::

    when ok:
    {"status": true, "job_id": "2"}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}

/job/
-----
Get statement of job.

* Supported Request Methods: GET
* Parameters:
    - job_id (string, required): id of job.

Example request:
::

    http://localhost:8080/job/

Example response:
::

    when ok:
    {"job_id": "2", "job_done": true, "error": "", "status": true, "job_error": false,
    "out": "total 56\n-rw-rw-r-- 1 techbk techbk   82 Th01  6 23:33 config.py"}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}

/listjobs/
----------
Get list of jobs.

* Supported Request Methods: GET
* Parameters: None

Example request:
::

    http://localhost:8080/listjobs/

Example response:
::

    when ok:
    {"status": true, "empty": false, "jobs": ["2", "3"]}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}


/canceljob/
-----------
Cancel job.

* Supported Request Methods: POST
* Parameters:
    - job_id (string, required): id of job.

Example request:
::

    http://localhost:8080/canceljob/

Example response:
::

    when ok and job is running:
    {"job_id": "2", "prevstatus": true, "status": true}

    when ok and job is done:
    {"job_id": "2", "prevstatus": false, "status": true}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}


Settup
======

SwiftClient
-----------
::

    $ sudo pip3 install python-swiftclient


Practice
========

1. Khong can phai @asyncio.coroutine cac ham trong class SwiftManager: Vi chi can cac method handle @asyncio.coroutine
la du


Docker Images
=============
Bio-wrapper images is available at https://hub.docker.com/r/techbk/bio-wrapper/

Install:
::

    docker pull techbk/bio-wrapper:0.0.4

