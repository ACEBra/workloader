#!/usr/bin/env python
#
#                      __   .__                    .___
# __  _  _____________|  | _|  |   _________     __| _/___________
# \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
#  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
#   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
#                          \/               \/      \/    \/
#
# Copyright (c) 2018 Stephen Shao <sjh311@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

"""``WorkloadWisdom`` module to operate Workload Wisdom through REST API

**Classes**

    WorkloadWisdom
"""

import logging
import time
import re

from workloader import util

LOGGER = logging.getLogger(__name__)


class WorkloadWisdom(object):
    """A Workload Wisdom.

    Provides operations to testbeds, tests, appliances on it

    """

    PORT_STATUS_RUNNING = 'running'
    PORT_STATUS_IDLE = 'idle'
    TEST_ACTIVE_STATES = ['starting', 'waiting', 'running', 'stopping']
    # skipped is the finished status for pre-test only workload
    TEST_FINISHED_STATES = ['failed', 'finished', 'aborted_by_user', 'skipped']

    def __init__(self, url, username, password):
        self._url = url
        self._username = username
        self._password = password
        self._version = None
        self._appliances = []
        self.get_version()

    def __del__(self):
        pass


    def get_version(self, api="/api/version"):
        """Get version of WorkloadWisdom.

        :param api: REST API to get WorkloadWisdom version
        :return: :string: version of the WorkloadWisdom
        :rtype: string
        """

        resp = util.rest_get(self._url+api, self._username, self._password)
        self._version = resp['version']
        LOGGER.debug("WorkloadWisdom Version: %s", self._version)

        return self._version


    # Generator(formerly Appliances) related API
    def list_appliances(self, api="/api/appliances/"):
        """List all appliances managed by this WorkloadWisdom.

        :param api: REST API to list all appliances managed by this WorkloadWisdom
        :return: :list: list of appliance dicts
        :rtype: list
        """

        list_url = self._url+api
        LOGGER.debug("list all appliances: %s", list_url)

        appliance_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(appliance_list)

        for generator in appliance_list:
            appliance = self.get_appliance(appliance_id=generator['id'])
            self._appliances.append(appliance)

        """
            {
                "id": "5bae33e6421aa95fab49c579",
                "name": "Dur LDX 9024082"
            },
            {
                "id": "58d2ded222314e308a940a0d",
                "name": "LDX_001"
            }
        """

        return self._appliances

    def get_appliance(self, appliance_id, api="/api/appliances/"):
        """Get a appliances JSON object by id.

        :param appliance_id: id of the appliance, e.g. '58d2ded222314e308a940a0d'
        :param api: REST API to get a appliance by given id
        :return: :dict: dict of the appliance
        :rtype: dict
        """

        show_url = self._url+api+appliance_id
        LOGGER.debug("get appliance details: %s", show_url)

        appliance = util.rest_get(show_url, self._username, self._password)
        util.dump_json(appliance)

        return appliance

    def get_appliance_by_name(self, name):
        """Get a appliance JSON object by its name.

        :param name: appliance name, e.g. 'LDX_003'
        :return: :dict: dict of the appliance
        :rtype: dict
        """

        appliance = None
        if not self._appliances:
            self._appliances = self.list_appliances()
        for gen in self._appliances:
            if gen['name'] == name:
                LOGGER.debug("got appliance: %s", name)
                appliance = gen
                break

        if not appliance:
            LOGGER.error("appliance %s not found", name)
            exit()

        util.dump_json(appliance)
        return appliance

    def get_appliance_port_status(self, appliance_id, port_id):
        """Return the specified port status by id.

        :param appliance_id: id of the appliance
        :param port_id: id of the port
        :return: :str: status of the port, 'idle', 'running'
        :rtype: str
        """

        appliance = self.get_appliance(appliance_id)

        for port in appliance['ports']:
            if port_id == port['port_id']:
                LOGGER.debug("appliance %s port %s status: %s", appliance_id, port_id, port['state'])
                return port['state']

        raise ValueError('invalid port_id')

    # Test beds related API
    def list_testbeds(self, api="/api/test_beds/"):
        """List all testbeds managed by this WorkloadWisdom.

        :param api: REST API to list all testbeds managed by this WorkloadWisdom
        :return: :list: list of testbeds dict
        :rtype: list
        """

        list_url = self._url+api
        LOGGER.debug("list all testbeds: %s", list_url)

        testbed_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(testbed_list)

        return testbed_list

    def create_testbed(self, testbed_file, api="/api/test_beds/"):
        #TODO: low priority
        LOGGER.error("low priority, pls create online")
        exit()


    def get_testbed(self, testbed_id, api="/api/test_beds/"):
        """Get a testbed JSON object by id.

        :param testbed_id: id of the testbed, e.g. '58d2ded222314e308a940a0d'
        :param api: REST API to get a testbed by given id
        :return: :dict: dict of the testbed
        :rtype: dict
        """

        rest_url = self._url+api+testbed_id
        LOGGER.debug("get testbed details: %s", rest_url)

        testbed = util.rest_get(rest_url, self._username, self._password)
        util.dump_json(testbed)

        return testbed

    def get_testbed_by_name(self, name, testbed_list=None):
        """Get a testbed JSON object by its name.

        :param name: testbed name, e.g. '1042_VLAN593_Greg_iSCSI_NFS_CIFS'
        :param testbed_list: return of list_testbeds(), memory data might be out of date
        :return: :dict: dict of the testbed
        :rtype: dict
        """

        if not testbed_list:
            tb_list = self.list_testbeds()
        else:
            tb_list = testbed_list

        testbed = None
        for item in tb_list:
            if item['name'] == name:
                LOGGER.debug("got testbed: %s", name)
                testbed = item
                break

        if not testbed:
            LOGGER.error("%s not found", name)
            exit()

        return self.get_testbed(testbed['id'])

    def clone_testbed(self, testbed_id, new_name, api="/api/test_beds/"):
        """Clone a testbed to a new one.

        :param testbed_id: id of the testbed, e.g. '58d2ded222314e308a940a0d'
        :param new_name: new name of new clone testbed
        :param api: REST API to clone a testbed by given id
        :return: :dict: dict of the clone testbed
        :rtype: dict
        """

        LOGGER.debug("clone testbed %s to %s", testbed_id, new_name)

        clone_url = self._url+api+testbed_id+"/clone"

        data = {
            'test_bed_id' : testbed_id,
            'name' : new_name
        }

        testbed = util.rest_post(clone_url, self._username, self._password, data)
        util.dump_json(testbed)
        LOGGER.info("cloned a new testbed: %s", testbed['name'])

        return testbed

    def delete_testbed(self, testbed_id, api="/test_beds/"):
        """Delete a testbed by id.

        :param testbed_id: id of the testbed, e.g. '58d2ded222314e308a940a0d'
        :param api: REST API to clone a testbed by given id
        """

        delete_url = self._url+api+testbed_id
        LOGGER.debug("delete testbed: %s", delete_url)

        body = util.rest_delete(delete_url, self._username, self._password)
        """
            {
                "redirect": "http://10.228.56.32/test_beds"
            }
        """
        util.dump_json(body)
        LOGGER.info("deleted testbed: %s", testbed_id)

    def set_testbed_privacy(self, testbed_id, private=True, api="/api/test_beds/"):
        """Set the privacy of a testbed by id.

        :param testbed_id: id of the testbed, e.g. '58d2ded222314e308a940a0d'
        :param private: boolean
        :param api: REST API to clone a testbed by given id
        """

        LOGGER.debug("set testbed privacy: %s", private)
        privacy_url = self._url+api+testbed_id+"/privacy"

        # WorkloadWisdom REST API recognize lowercase string only
        if private:
            value = 'true'
        else:
            value = 'false'

        data = {
            'private': value
        }

        testbed = util.rest_put(privacy_url, self._username, self._password, data)
        util.dump_json(testbed)
        LOGGER.info("set testbed: %s privacy=%s success", testbed['name'], testbed['private'])



    # Tests related API, one projects(workloads) can have multiple tests(runs)
    def list_tests(self, api="/api/tests/"):
        """List of tests on the WorkloadWisdom.

        :param api: REST API to list of tests on the WorkloadWisdom
        :return: :list: list of WorkloadTest id
        :rtype: list
        """

        list_url = self._url+api
        LOGGER.debug("list of tests: %s", list_url)

        """
        [
            {
                "id": "5bbd544d421aa9472922ca09"
            },
            {
                "id": "5bbd40ec421aa950e522dc16"
            }
        ]
        """

        tests_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(tests_list)

        return tests_list

    def show_test(self, test_id, api="/api/tests/"):
        """Show a test on the WorkloadWisdom.

        :param test_id: id of test to show
        :param api: REST API to show a test
        :return: :dict: dict of a WorkloadTest JSON
        :rtype: dict
        """

        show_url = self._url+api+test_id
        LOGGER.debug("show a test: %s", show_url)

        test = util.rest_get(show_url, self._username, self._password)
        util.dump_json(test)

        return test

    def wait_until_test_complete(self, test_id, interval=60):
        """Wait until test complete.

        :param test_id: workload test id
        :param interval: query interval
        :return: :dict: dict of a WorkloadTest JSON
        :rtype: dict
        """

        while True:
            test = self.show_test(test_id)
            LOGGER.debug('test id %s state: %s', test['id'], test['state'])
            for port in test['ports']:
                resp = self.get_test_port_state(test['id'], port['id'])
                if len(resp['tests']) == 0:
                    LOGGER.warn("Stats not available for test %s, port %s", test['id'], str(port['id']))
                else:
                    for item in resp['tests']:
                        if item['stat_string'] == "load.scenarios.attempts":
                            attempts = str(item['value'])
                        if item['stat_string'] == "load.scenarios.succeeds":
                            succeeds = str(item['value'])
                        if item['stat_string'] == "load.scenarios.fails":
                            fails = str(item['value'])
                        if item['stat_string'] == "load.scenarios.aborts":
                            aborts = str(item['value'])
                    LOGGER.info("-"*120)
                    LOGGER.info("test id = %s, port = %s, state = %s, duration planned = %s, duration actual = %s",
                                test['id'], str(port['id']), test['state'],
                                test['duration_planned'], test['duration_actual'])
                    LOGGER.info("Attempts = " + attempts + ",Succeeds = " + succeeds
                                + ", Fails = " + fails + ", Aborts = " + aborts)
                    LOGGER.info("-"*120)

            if test['state'] not in self.TEST_FINISHED_STATES:
                LOGGER.debug('sleep %s seconds', interval)
                time.sleep(interval)
            else:
                break

        # fix a bug, passing latest result to save_all_test_results
        return test

    def wait_until_iteration_complete(self, iteration_suite_id, interval=60):
        """Wait until an iteration test suite complete.

        :param iteration_suite_id: workload test id
        :param interval: query interval
        :return: :dict: dict of a WorkloadTest JSON
        :rtype: dict
        """

        while True:
            iteration = self.show_iteration_test_suite(iteration_suite_id)
            LOGGER.info("-"*120)
            LOGGER.info("iteration_test_suite id = %s, name = %s, state = %s, iteration_duration = %s, created_at = %s",
                        iteration['id'], iteration['name_cache'], iteration['state'],
                        iteration['iteration_duration'], iteration['created_at'])
            LOGGER.info("-"*120)

            if iteration['state'] not in self.TEST_FINISHED_STATES:
                LOGGER.debug('sleep %s seconds', interval)
                time.sleep(interval)
            else:
                break

        return iteration


    def stop_test_by_project_name(self, project_name, project_list=None):
        """Stop a test its associated project name.

        :param project_name: project name, e.g. 'STEPHEN_BBT_FILE_11NFSv3FSper_SP_Deduplication_Compression'
        :param project_list: return of list_projects(), memory data might be out of date
        :return: :dict: dict of a stopped WorkloadTest JSON
        :rtype: dict
        """

        project = self.get_project_by_name(project_name, project_list)
        LOGGER.info("id of project %s is: %s", project_name, project['id'])

        '''
            "tests": [
                {
                    "id": "5c0fc55f421aa9426841d6e9"
                },
                {
                    "id": "5c0f9017421aa922e8cf268a"
                }
            ]
        '''
        for item in project['tests']:
            test = self.show_test(item['id'])
            # stop the test if not in finished state
            if test['state'] not in self.TEST_FINISHED_STATES:
                LOGGER.info("stopping %s", test['id'])
                return self.stop_test(test['id'])

        LOGGER.debug("nothing to stop")
        return None

    def stop_test(self, test_id, api="/api/tests/"):
        """Stop a test on the WorkloadWisdom.

        :param test_id: id of test to stop
        :param api: REST API to stop a test
        :return: :dict: dict of a stopped WorkloadTest JSON
        :rtype: dict
        """

        stop_url = self._url+api+test_id+"/stop"
        LOGGER.debug("stop a test: %s", stop_url)

        data = {
            'test_id' : test_id
        }

        test = util.rest_put(stop_url, self._username, self._password, data)
        util.dump_json(test)
        LOGGER.info("stopping test: %s and wait until complete", test_id)

        while True:
            test = self.show_test(test_id)
            state = test["state"]

            LOGGER.debug("test_id=%s, state=%s", test["id"], test["state"])
            # break if already stopped
            if state not in self.TEST_ACTIVE_STATES:
                break
            time.sleep(2)

        return test

    def start_test_by_id(self, project_id, testbed_id, duration):
        """Start a test on the WorkloadWisdom by id.

        :param project_id: id of project to create a test from
        :param testbed_id: id of test bed it to start a test on
        :param duration: duration of the test in seconds
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        project = self.show_project(project_id)
        testbed = self.get_testbed(testbed_id)

        return self.start_test(project, testbed, duration)

    def start_test_by_name(self, project_name, testbed_name, duration):
        """Start a test on the WorkloadWisdom by name.

        :param project_name: id of project to create a test from
        :param testbed_name: id of test bed it to start a test on
        :param duration: duration of the test in seconds
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        project = self.get_project_by_name(project_name)
        testbed = self.get_testbed_by_name(testbed_name)
        return self.start_test(project, testbed, duration)

    def start_test(self, project, testbed, duration, api="/api/tests"):
        """Start a test on the WorkloadWisdom.

        :param project: project JSON object
        :param testbed: testbed JSON object
        :param duration: duration of the test in seconds
        :param api: REST API to start a test
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        if not (type(project) is dict and type(testbed) is dict):
            raise TypeError("non dict param")

        for client in testbed['clients']:
            state = self.get_appliance_port_status(client['appliance_id'], client['port'])
            if state != WorkloadWisdom.PORT_STATUS_IDLE:
                LOGGER.error("port_id %s is %s, unable to start test", client['port'], state)
                raise RuntimeError("port in use")

        start_url = self._url+api
        LOGGER.debug("start a test: %s", start_url)

        data = {
            'projectid': project['id'],
            'test_bed_id': testbed['id'],
            'duration': duration
        }

        test = util.rest_post(start_url, self._username, self._password, data)
        util.dump_json(test)

        return test

    def get_test_port_state(self, test_id, port_id, api="/api/tests/", dump=False):
        """Get statistics results for a port of a test on the WorkloadWisdom.

        :param test_id: test id
        :param port_id: port id
        :param api: REST API to get config for a test
        :param dump: dump json or not, it may cause log file very big

        :return: :dict: dict of a WorkloadTest JSON config
        :rtype: dict
        """

        get_url = self._url+api+test_id+"/stats/ports/"+str(port_id)
        LOGGER.debug("get state for test: %s", get_url)

        state = util.rest_get(get_url, self._username, self._password)
        if dump:
            util.dump_json(state)

        return state


    def get_test_config(self, test_id, api="/api/tests/"):
        """Get config for a test on the WorkloadWisdom.

        :param test_id: test id
        :param api: REST API to get config for a test
        :return: :dict: dict of a WorkloadTest JSON config
        :rtype: dict
        """

        get_url = self._url+api+test_id+"/config"
        LOGGER.debug("get config for test: %s", get_url)

        config = util.rest_get(get_url, self._username, self._password)
        util.dump_json(config)

        return config

    def show_test_log(self, test_id, api="/api/tests/"):
        """Show logs for a test on the WorkloadWisdom.

        :param test_id: test id
        :param api: REST API to show logs for a test
        :return: :dict: dict of a WorkloadTest test log
        :rtype: dict
        """

        get_url = self._url+api+test_id+"/logs"
        LOGGER.debug("show logs for a test: %s", get_url)

        logs = util.rest_get(get_url, self._username, self._password)
        '''
            "tests": [
                    {
                        "time": "2018-10-16T04:39:19.925Z",
                        "status": "info",
                        "message": "Downloading summary for port 10.228.56.21:0 completed successfully"
                    },
                    {
                        "time": "2018-10-16T04:39:19.823Z",
                        "status": "info",
                        "message": "Downloading summary for port 10.228.56.21:0"
                    }
            ]
        '''
        util.dump_json(logs)

        return logs

    def save_test_result(self, test_id, uri, api="/api/tests/", dir="./"):
        """Save test result into a file

        :param test_id: test id
        :param uri: log, summary or trace:
            files/ports/:port_id/summary
            files/ports/:port_id/trace
            files/ports/:port_id/log
        :param api: REST API for a test
        :param dir: path to save test result
        :return: :str: file name containing full path
        :rtype: str
        """

        get_url = self._url+api+str(test_id)+"/"+uri
        m = re.match(r"files/ports/(\d)/(summary|log|trace)", uri)
            # GET /api/tests/:test_id/files/ports/:port_id/log
        if m.group(2) == 'log':
            postfix = ".log"
        elif m.group(2) == 'summary':
            # GET /api/tests/:test_id/
            postfix = ".sum"
        elif m.group(2) == 'trace':
            postfix = ".pcap"
        else:
            LOGGER.error("invalid uri: %s", uri)

        LOGGER.info("get %s file for test", get_url)
        log_name = dir+str(test_id)+"_port_"+str(m.group(1))+postfix

        content = util.rest_get(get_url, self._username, self._password, json=False)
        # ./5bc054af421aa92b599bcbf4_port_0.log

        LOGGER.debug("full log name: %s", log_name)
        # summary & trace are not readable
        if 'log' in postfix:
            LOGGER.debug("%s", content)
        util.save_to_file(log_name, content)

        return log_name

    def export_test_charts(self, test_id, api="/api/tests/", path="./"):
        """Export test charts into a file

        :param test_id: test id
        :param api: REST API for a test
        :param path: path to save test result
        :return: :str: file name containing full path
        :rtype: str
        """

        # GET /api/tests/:test_id/export_charts
        export_url = self._url+api+test_id+"/export_charts"
        LOGGER.info("export all charts to CSV for test: %s", export_url)
        postfix = ".zip"
        log_name = path + str(test_id) + postfix

        content = util.rest_get(export_url, self._username, self._password, json=False)
        # ./5bc054af421aa92b599bcbf4.zip
        LOGGER.debug("full log name: %s", log_name)
        util.save_to_file(log_name, content)

        return log_name

    def save_all_test_results(self, test, path="./"):
        """Save all available test results to path

        :param test: test JSON dict
        :param path: path to save test result
        """

        self.show_test(test['id'])
        LOGGER.info("save test results for: %s", test['id'])
        util.dump_json(test)

        if test['state'] not in WorkloadWisdom.TEST_FINISHED_STATES:
            LOGGER.error('%s is %s', test['id'], test['state'])
            raise ValueError("test not finished yet")

        '''
            "result_files": {
                "config": "files/config",
                "logs": [
                    "files/ports/0/log"
                ],
                "summary": [
                    "files/ports/0/summary"
                ],
                "traces": [
                    "files/ports/0/trace"
                ]
            }
        '''
        config = test['result_files']['config']
        logs = test['result_files']['logs']
        summaries = test['result_files']['summary']
        traces = test['result_files']['traces']

        for log in logs:
            LOGGER.info("save log file: %s", log)
            self.save_test_result(test['id'], log, dir=path)
        for summary in summaries:
            LOGGER.info("save summary file: %s", summary)
            self.save_test_result(test['id'], summary, dir=path)
        for trace in traces:
            LOGGER.info("save trace file: %s", trace)
            self.save_test_result(test['id'], trace, dir=path)

        self.export_test_charts(test['id'], path=path)
        self.get_test_config(test['id'])
        LOGGER.info("completed saving all test results for: %s", test['id'])

    # Workloads(formerly Projects) related API, a workload can have multiple tests
    def list_projects(self, api="/api/projects/", library=False):
        """List all or library projects on the WorkloadWisdom.

        :param api: REST API to list of workloads
        :param library: Boolean, Workload library list or not
        :return: :list: list of dict containing id and name
        :rtype: list
        """

        list_url = self._url + api
        if library:
            list_url += "/library"

        LOGGER.debug("list of projects: %s", list_url)

        """
        [
            {
                "id": "5bbed1ee421aa950e522f9e6",
                "name": "1494_Automation_Debug"
            },
            {
                "id": "5ba929b9421aa95fb64948a7",
                "name": "NFSv4.1 flat Fls100 4000MBFlSz BlckSz128KB 10-90 R-W 90-10 D-MD 0-100 R-S Workload"
            }
        ]
        """

        project_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(project_list)

        return project_list

    def show_project(self, project_id, api="/api/projects/"):
        """Show a project on the WorkloadWisdom.

        :param project_id: project id to show
        :param api: REST API to show a workload
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        show_url = self._url+api+project_id
        LOGGER.debug("show a project: %s", show_url)

        project = util.rest_get(show_url, self._username, self._password)
        util.dump_json(project)

        return project

    def create_project(self, api="/api/projects/"):
        #TODO low priority, normally we clone from a library project
        LOGGER.error("low priority, normally we clone from a library project")
        exit()

    def delete_project(self, project_id, api="/api/projects/"):
        """Delete a project by id on the WorkloadWisdom.

        :param project_id: project id to delete
        :param api: REST API to delete a workload
        """

        del_url = self._url+api+project_id
        LOGGER.debug("delete a project: %s", del_url)

        resp = util.rest_delete(del_url, self._username, self._password)
        util.dump_json(resp)
        LOGGER.info("deleted project: %s", project_id)

    def get_project_by_name(self, name, project_list=None):
        """Get a project JSON object by its name

        :param name: project name, e.g. '1494_Automation_Debug'
        :param project_list: return of list_projects(), memory data might be out of date
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        if not project_list:
            proj_list = self.list_projects()
        else:
            proj_list = project_list

        project = None
        for proj in proj_list:
            if proj['name'] == name:
                LOGGER.debug("got project: %s", name)
                project = proj
                break
        # AR999302 - failed to start composite workload
        if not project:
            LOGGER.error("%s not found, check composite workloads", name)
            project = self.get_composite_workload_by_name(name)

        if not project:
            LOGGER.error("%s not found", name)
            exit()

        return self.show_project(project['id'])


    def clone_project(self, project_id, new_name, api="/api/projects/"):
        """Clone a project to a new one

        :param project_id: id of the project, e.g. '55dc9da98f822bf8cf000b6a'
        :param new_name: name of new project
        :param api: REST API to clone a testbed by given id
        :return: :dict: dict of the clone testbed
        :rtype: dict
        """

        LOGGER.debug("clone project %s to %s", project_id, new_name)

        clone_url = self._url + api + project_id + "/clone"

        data = {
            'project_id': project_id,
            'name': new_name
        }

        project = util.rest_post(clone_url, self._username, self._password, data)
        util.dump_json(project)
        LOGGER.info("cloned a new project: %s", project['name'])

        return project

    def set_project_privacy(self, project_id, private=True, api="/api/projects/"):
        """Set the privacy of a project by id

        :param project_id: id of the testbed, e.g. '55dc9da98f822bf8cf000be1'
        :param private: boolean
        :param api: REST API to change private settings for workload by given id
        """

        LOGGER.debug("set project privacy: %s", private)
        privacy_url = self._url+api+project_id+"/privacy"

        # WorkloadWisdom REST API recognize lowercase string only
        if private:
            value = 'true'
        else:
            value = 'false'

        data = {
            'private': value
        }

        project = util.rest_put(privacy_url, self._username, self._password, data)
        util.dump_json(project)
        LOGGER.info("set project: %s privacy=%s success", project['name'], project['private'])


    # Composite workload related API
    def list_composite_workloads(self, api="/api/composite_workloads"):
        """List of composite workloads on the WorkloadWisdom.

        :param api: REST API to list of composite workloads
        :return: :list: list of dict containing id and name
        :rtype: list
        """

        list_url = self._url + api
        LOGGER.debug("list of composite workloads: %s", list_url)

        """
        [
            {
                "id": "5bdbde45421aa90c0177e149",
                "name": "1056_Stephen_VLAN590_NFS3_4_SMB2_Composite"
            },
            {
                "id": "5bbe2a40421aa9472922efc6",
                "name": "1448VLAN590_NFS3_SMB2_Composite"
            }
        ]
        """

        composite_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(composite_list)

        return composite_list

    def show_composite_workload(self, workload_id, api="/api/composite_workloads/"):
        """Show a composite workload on the WorkloadWisdom.

        :param workload_id: composite workload id to show
        :param api: REST API to show a composite workload
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        show_url = self._url+api+workload_id
        LOGGER.debug("show a composite workload: %s", show_url)

        composite = util.rest_get(show_url, self._username, self._password)
        util.dump_json(composite)

        return composite

    def create_composite_workload(self, api="/api/composite_workloads/"):
        #TODO low priority, normally we clone from a library project
        LOGGER.error("low priority, normally we clone from a existing composite workload")
        exit()

    def delete_composite_workload(self, workload_id, api="/api/composite_workloads/"):
        """Delete a composite workload by id on the WorkloadWisdom.

        :param workload_id: composite workload id to delete
        :param api: REST API to delete a composite workload
        """

        del_url = self._url+api+workload_id
        LOGGER.debug("delete a composite workload: %s", del_url)

        resp = util.rest_delete(del_url, self._username, self._password)
        util.dump_json(resp)
        LOGGER.info("deleted composite workload: %s", workload_id)


    def clone_composite_workload(self, workload_id, new_name, api="/api/composite_workloads/"):
        """Clone a composite workload to a new one

        :param workload_id: id of the existing composite workload, e.g. '55dc9da98f822bf8cf000b6a'
        :param new_name: name of new composite workload
        :param api: REST API to clone the composite workload
        :return: :dict: dict of the cloned composite workload
        :rtype: dict
        """

        LOGGER.debug("clone project %s to %s", workload_id, new_name)
        clone_url = self._url + api + workload_id + "/clone"

        data = {
            'composite_workload_id': workload_id,
            'name': new_name
        }

        composite = util.rest_post(clone_url, self._username, self._password, data)
        util.dump_json(composite)
        LOGGER.info("cloned a new composite workload: %s", composite['name'])

        return composite

    def set_composite_workload_privacy(self, workload_id, private=True, api="/api/composite_workloads/"):
        """Set the privacy of a composite workload by id

        :param workload_id: id of the workload_id, e.g. '5bdbde45421aa90c0177e149'
        :param private: boolean
        :param api: REST API to change private settings for composite workload by given id
        """

        LOGGER.debug("set composite workload privacy: %s", private)
        privacy_url = self._url+api+workload_id+"/privacy"

        # WorkloadWisdom REST API recognize lowercase string only
        if private:
            value = 'true'
        else:
            value = 'false'

        data = {
            'private': value
        }

        composite = util.rest_put(privacy_url, self._username, self._password, data)
        util.dump_json(composite)
        LOGGER.info("set composite workload: %s privacy=%s success", composite['name'], composite['private'])

    def get_composite_workload_by_name(self, name, composite_list=None):
        """Get a project JSON object by its name

        :param name: composite workload name, e.g. '1056_Stephen_VLAN590_NFS3_4_SMB2_Composite'
        :param composite_list: return of list_composite_workloads(), memory data might be out of date
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        if not composite_list:
            cw_list = self.list_composite_workloads()
        else:
            cw_list = composite_list

        composite_workload = None
        for item in cw_list:
            if item['name'] == name:
                LOGGER.debug("got composite workload: %s", name)
                composite_workload = item
                break

        if not composite_workload:
            LOGGER.error("%s not found", name)
            exit()

        return self.show_composite_workload(composite_workload['id'])


    # Iteration suites related API
    def list_iteration_suite(self, api="/api/iteration_suites"):
        """List of iteration suites on the WorkloadWisdom.

        :param api: REST API to list of iteration test suites
        :return: :list: list of dict containing id and name
        :rtype: list
        """

        list_url = self._url + api
        LOGGER.debug("list of iteration suites: %s", list_url)

        """
        [
            {
                "id": "5d23029b421aa92501da5160",
                "name": "CCT_LDX_ILD_FAST_PACO_HA_Iteration"
            },
            {
                "id": "5cecf50b421aa95c3076de6e",
                "name": "CCT_LDX_LA_FSN_TSYSTEMS_Iteration"
            }
        ]
        """

        iteration_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(iteration_list)

        return iteration_list

    def show_iteration_suite(self, id, api="/api/iteration_suites/"):
        """Show an iteration suite on the WorkloadWisdom.

        :param id: id of an iteration suite
        :param api: REST API to show a composite workload
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        show_url = self._url+api+id
        LOGGER.debug("show a iteration test suite: %s", show_url)

        iteration_suite = util.rest_get(show_url, self._username, self._password)
        util.dump_json(iteration_suite)

        return iteration_suite

    def get_iteration_suite_by_name(self, iteration_suite_name, iteration_suite_list=None):
        """Get an iteration suite by name

        :param iteration_suite_name: iteration test suite name, e.g. 'CCT_LDX_ILD_FAST_PACO_HA_Iteration'
        :param iteration_suite_list: return of list_iteration_suite(), memory data might be out of date
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        if not iteration_suite_list:
            its_list = self.list_iteration_suite()
        else:
            its_list = iteration_suite_list

        for its in its_list:
            iteration_suite = self.show_iteration_suite(its['id'])
            '''
                {
                    "id": "5d23029b421aa92501da5160",
                    "name": "CCT_LDX_ILD_FAST_PACO_HA_Iteration"
                }
            '''
            if iteration_suite['name'] == iteration_suite_name:
                LOGGER.debug("got iteration suite: %s, id: %s", iteration_suite_name, iteration_suite['id'])
                return iteration_suite

        if not iteration_suite:
            LOGGER.error("%s not found", iteration_suite_name)
            exit()


    # Iteration test suites related API
    def list_iteration_test_suite(self, api="/api/iteration_test_suites"):
        """List of iteration test suites on the WorkloadWisdom.

        :param api: REST API to list of iteration test suites
        :return: :list: list of dict containing id and name
        :rtype: list
        """

        list_url = self._url + api
        LOGGER.debug("list of iteration test suites: %s", list_url)

        """
        [
            {
                "id": "5ce3595c421aa93a7102644c"
            },
            {
                "id": "5ce358f9421aa965f390d1fb"
            }
        ]
        """

        iteration_list = util.rest_get(list_url, self._username, self._password)
        util.dump_json(iteration_list)

        return iteration_list

    def show_iteration_test_suite(self, iteration_id, api="/api/iteration_test_suites/"):
        """Show an iteration test suite on the WorkloadWisdom.

        :param iteration_id: Id of an iteration test suite
        :param api: REST API to show a composite workload
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        show_url = self._url+api+iteration_id
        LOGGER.debug("show a iteration test suite: %s", show_url)

        iteration_test_suite = util.rest_get(show_url, self._username, self._password)
        util.dump_json(iteration_test_suite)

        return iteration_test_suite

    def stop_iteration_test_suite(self, iteration_test_suite_id, api="/api/iteration_test_suites/"):
        """Stop an iteration test suite on the WorkloadWisdom.

        :param iteration_test_suite_id: id of test to stop
        :param api: REST API to stop a test
        :return: :dict: dict of a stopped WorkloadTest JSON
        :rtype: dict
        """

        stop_url = self._url+api+iteration_test_suite_id+"/stop"
        LOGGER.debug("stop an iteration test suite: %s", stop_url)

        data = {
            'iteration_test_suite_id ' : iteration_test_suite_id
        }

        resp = util.rest_put(stop_url, self._username, self._password, data)
        util.dump_json(resp)
        LOGGER.info("stopping iteration test suite: %s and wait until complete", iteration_test_suite_id)

        while True:
            iteration_test_suite = self.show_iteration_test_suite(iteration_test_suite_id)
            state = iteration_test_suite["state"]

            LOGGER.debug("iteration_test_suite_id=%s, state=%s", iteration_test_suite["id"], state)
            # break if already stopped
            if state not in self.TEST_ACTIVE_STATES:
                break
            time.sleep(5)

        return iteration_test_suite

    def stop_iteration_test_suite_by_name(self, iteration_suite_name, iteration_list=None):
        """Stop an iteration test suite by its associated iteration suite name.
        :param iteration_suite_name: iteration test suite name
        :param iteration_list: return of list_iteration_test_suite(), memory data might be out of date
        :return: :dict: dict of a stopped WorkloadTest JSON
        :rtype: dict
        """

        iteration = self.get_iteration_suite_by_name(iteration_suite_name, iteration_list)
        LOGGER.info("id of iteration suite %s is: %s", iteration_suite_name, iteration['id'])
        '''
            "test_suites": [
                {
                    "id": "5d254d45421aa9689cdc6c70",
                    "name_cache": "CCT_LDX_ILD_FAST_PACO_HA_Iteration",
                    "state": "finished",
                    "created_at": "2019-07-10T02:28:22.061Z",
                    "finished_at": "2019-07-10T08:07:13.586Z"
                },
                {
                    "id": "5d254cf1421aa92948dc6c67",
                    "name_cache": "CCT_LDX_ILD_FAST_PACO_HA_Iteration",
                    "state": "finished",
                    "created_at": "2019-07-10T02:26:57.587Z",
                    "finished_at": "2019-07-10T02:27:57.008Z"
                }
            ],
        '''
        for item in iteration['test_suites']:
            test = self.show_iteration_test_suite(item['id'])
            # stop the test if not in finished state
            if test['state'] not in self.TEST_FINISHED_STATES:
                LOGGER.info("stopping %s", test['id'])
                return self.stop_iteration_test_suite(test['id'])

        LOGGER.debug("nothing to stop")
        return None


    def get_iteration_test_suite_by_name(self, iteration_suite_name, iteration_suite_list=None):
        """Get an iteration test suite by its name

        :param iteration_suite_name: iteration test suite name, e.g. 'CCT_LDX_ILD_FAST_PACO_HA_Iteration'
        :param iteration_suite_list: return of list_iteration_suite(), memory data might be out of date
        :return: :dict: dict of project JSON object
        :rtype: dict
        """

        if not iteration_suite_list:
            its_list = self.list_iteration_suite()
        else:
            its_list = iteration_suite_list

        for its in its_list:
            iteration_test_suite = self.show_iteration_test_suite(its['id'])
            '''
                "name_cache": "CCT_LDX_ILD_FAST_PACO_HA_Iteration",
            '''
            if iteration_test_suite['name_cache'] == iteration_suite_name:
                LOGGER.debug("got iteration test suite: %s, id: %s", iteration_suite_name, iteration_test_suite['id'])
                return iteration_test_suite

        if not iteration_test_suite:
            LOGGER.error("%s not found", iteration_suite_name)
            exit()

    def start_iteration_test_suite_by_id(self, iteration_suite_id, testbed_id):
        """Start an iteration test suite by iteration suite id.

        :param iteration_suite_id : id of the iteration test suite to create a test from
        :param testbed_id: id of test bed it to start a test on
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        iteration_test_suite = self.show_iteration_test_suite(iteration_suite_id)
        testbed = self.get_testbed(testbed_id)

        return self.start_iteration_test_suite(iteration_test_suite, testbed)

    def start_iteration_test_suite_by_name(self, iteration_suite_name, testbed_name):
        """Start an iteration test suite by name.

        :param iteration_suite_name: name of the iteration test suite to create a test from
        :param testbed_name: id of test bed it to start a test on
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        iteration_suite = self.get_iteration_suite_by_name(iteration_suite_name)
        testbed = self.get_testbed_by_name(testbed_name)
        return self.start_iteration_test_suite(iteration_suite, testbed)

    def start_iteration_test_suite(self, iteration_suite, testbed, api="/api/iteration_test_suites"):
        """Start a test on the WorkloadWisdom.

        :param iteration_test_suite: iteration test suite JSON object
        :param testbed: testbed JSON object
        :param api: REST API to start a test
        :return: :dict: dict of a started WorkloadTest JSON
        :rtype: dict
        """

        if not (type(iteration_suite) is dict and type(testbed) is dict):
            raise TypeError("non dict param")


        for client in testbed['clients']:
            state = self.get_appliance_port_status(client['appliance_id'], client['port'])
            if state != WorkloadWisdom.PORT_STATUS_IDLE:
                LOGGER.error("port_id %s is %s, unable to start iteration test suite", client['port'], state)
                raise RuntimeError("port in use")

        start_url = self._url+api
        LOGGER.debug("start an iteration test suite: %s", start_url)

        data = {
            'iteration_suite_id': iteration_suite['id'],
            'test_bed_id': testbed['id'],
        }

        iteration = util.rest_post(start_url, self._username, self._password, data)
        util.dump_json(iteration)

        return iteration

    # Workload Suites related API