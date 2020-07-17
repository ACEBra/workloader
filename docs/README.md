```bash
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
```
Workload Wisdom REST API based on 6.0.0-Build.71.97facf49

```
Resources

Analysis actions
Resource	                                            Description
GET /api/analysis_actions	                            List of Analysis Actions
GET /api/analysis_actions/:id	                            Show an analysis action

Generators (formerly Appliances)
Resource	                                            Description
GET /api/appliances	                                    List of Generators
GET /api/appliances/:id	                                    Show a Generator
POST /api/appliances/:id/upgrade_firmware	            Upgrade Generator firmware

Application
Resource	                                            Description
GET /api/version	                                    LDX-E version

Composite workloads
Resource	                                            Description
POST /api/composite_workloads/:id/clone	                    Clone one Composite Workload
PUT /api/composite_workloads/:id/privacy	            Change private settings for Composite Workload
GET /api/composite_workloads	                            List of Composite Workloads
GET /api/composite_workloads/:id	                    Show a composite workload
POST /api/composite_workloads	                            Create a composite workload
PUT /api/composite_workloads/:id	                    Update a composite workload
DELETE /api/composite_workloads/:id	                    Destroy a composite workload

Conditions
Resource	                                            Description
POST /api/conditions/:id/clone	                            Clone one Condition
GET /api/conditions	                                    List of Conditions
GET /api/conditions/:id	                                    Show a condition

Iteration suites
Resource	                                            Description
POST /api/iteration_suites/:id/clone	                    Clone one Iteration Suite
PUT /api/iteration_suites/:id/privacy	                    Change private settings for Iteration Suite
GET /api/iteration_suites	                            List of Iteration Suites
GET /api/iteration_suites/:id	                            Show an iteration suite
POST /api/iteration_suites	                            Create an iteration suite
PUT /api/iteration_suites/:id	                            Update an iteration suite
GET /api/iteration_suites/iteration_parameters	            Iteration parameters for a workload
DELETE /api/iteration_suites/:id	                    Destroy an iteration suite

Iteration test suites
Resource	                                            Description
GET /api/iteration_test_suites	                            List of Iteration Test Suites
GET /api/iteration_test_suites/:id	                    Show an iteration test suite
GET /api/iteration_test_suites/:id/iteration_results	    Iteration results in csv format
POST /api/iteration_test_suites	                            Start an iteration test suite
PUT /api/iteration_test_suites/:id/stop	                    Stop an iteration test suite


Workload Suites (formerly Project Suites)
Resource	                                            Description
POST /api/project_suites/:id/clone	                    Clone one Workload Suite
PUT /api/project_suites/:id/privacy	                    Change private settings for Workload Suite
GET /api/project_suites	                                    List of Workload Suites
GET /api/project_suites/:id	                            Show a workload suite


Workloads (formerly Projects)
Resource	                                            Description
POST /api/projects/:id/clone	                            Clone one Workload
PUT /api/projects/:id/privacy	                            Change private settings for Workload
GET /api/projects	                                    List of Workloads
GET /api/projects/library	                            Workload library list
GET /api/projects/:id	                                    Show a workload
GET /api/projects/:id/export                        	    Download a workload
POST /api/projects	                                    Create a workload
PUT /api/projects/:id                               	    Update a workload
GET /api/projects/:id/as_is_config                  	    Get saved configuration of as is config
DELETE /api/projects/:id	                            Destroy a Workload

Report templates
Resource	                                            Description
GET /api/report_templates	                            List of Report Templates
GET /api/report_templates/:id	                            Show a report template

Test beds
Resource	                                            Description
POST /api/test_beds/:id/clone	                            Clone one Test Bed
PUT /api/test_beds/:id/privacy	                            Change private settings for Test Bed
GET /api/test_beds	                                    List of Test Beds
GET /api/test_beds/:id	                                    Show a test bed
DELETE /testbeds/:id                                        Delete a test bed

Test suites
Resource	                                            Description
GET /api/test_suites	                                    List of Test Suites
GET /api/test_suites/:id                            	    Show a test suite
PUT /api/test_suites/:test_suite_id/stop	            Stop a test suite
POST /api/test_suites	                                    Start a test suite

Tests
Resource	                                            Description
GET /api/tests	                                            List of Tests
GET /api/tests/:id	                                    Show a test
PUT /api/tests/:test_id/stop	                            Stop a test
POST /api/tests	                                            Start a test from workload
POST /api/tests/start_config	                            Start a test from config
POST /api/tests/start_as_is	                            Start a test from workload as is
GET /api/tests/:test_id/config	                            Config for a test
GET /api/tests/:test_id/export_charts	                    Export all charts in CSV
GET /api/tests/:test_id/series/ports/:port_id/:stat_string  Specific statistic results for port
GET /api/tests/:test_id/stats/ports/:port_id	            Statistics results for port
GET /api/tests/:test_id/files/config	                    Config file for a test
GET /api/tests/:test_id/files/ports/:port_id/log	    Log file for port
GET /api/tests/:test_id/files/ports/:port_id/summary	    Summary file for port
GET /api/tests/:test_id/files/ports/:port_id/trace	    Trace file for port
GET /api/tests/:test_id/logs	                            Show logs for a test

Users
Resource	                                            Description
POST /api/users/auth	                                    Check email/password pair

```