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

import logging
import argparse

from workloader.workloadwisdom import WorkloadWisdom

LOGGING_FORMAT = u'%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
DATE_FORMAT = u'%a, %d %b %Y %H:%M:%S'


def _get_workload_wisdom(args):
    logging.debug(args)
    url = u"http://" + args.ip
    username = args.username
    password = args.password
    ww = WorkloadWisdom(url, username, password)

    return ww


def _workloads_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of workloads")
    ww.list_projects()


def _workloads_private(args):
    ww = _get_workload_wisdom(args)
    logging.info("set workload %s privacy", args.name)
    project = ww.get_project_by_name(args.name)
    ww.set_project_privacy(project['id'], args.yes)


def _workloads_show(args):
    ww = _get_workload_wisdom(args)
    logging.info("show workload %s", args.name)
    ww.get_project_by_name(args.name)


def _workloads_delete(args):
    ww = _get_workload_wisdom(args)
    logging.info("delete a workload %s", args.name)
    project = ww.get_project_by_name(args.name)
    ww.delete_project(project['id'])


def _workloads_clone(args):
    ww = _get_workload_wisdom(args)
    logging.info("clone workload %s to %s", args.old, args.new)
    old = ww.get_project_by_name(args.old)
    ww.clone_project(project_id=old['id'], new_name=args.new)


def _generator_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of generators")
    ww.list_appliances()


def _generator_show(args):
    ww = _get_workload_wisdom(args)
    logging.info("show generator: %s", args.name)
    ww.get_appliance_by_name(args.name)


def _testbed_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of testbeds")
    ww.list_testbeds()


def _testbed_show(args):
    ww = _get_workload_wisdom(args)
    logging.info("show testbed: %s", args.name)
    ww.get_testbed_by_name(args.name)


def _testbed_delete(args):
    ww = _get_workload_wisdom(args)
    logging.info("delete testbed: %s", args.name)
    testbed = ww.get_testbed_by_name(args.name)
    ww.delete_testbed(testbed['id'])


def _testbed_clone(args):
    ww = _get_workload_wisdom(args)
    logging.info("clone testbed %s to %s", args.old, args.new)
    old = ww.get_testbed_by_name(args.old)
    ww.clone_testbed(testbed_id=old['id'], new_name=args.new)


def _testbed_private(args):
    ww = _get_workload_wisdom(args)
    logging.info("set testbed privacy: %s", args.name)
    testbed = ww.get_testbed_by_name(args.name)
    ww.set_testbed_privacy(testbed['id'], args.yes)


def _test_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of tests")
    ww.list_tests()


def _test_show(args):
    ww = _get_workload_wisdom(args)
    logging.info("show test: %s", args.id)
    test = ww.show_test(args.id)
    complete = ww.wait_until_test_complete(test['id'])
    ww.save_all_test_results(complete, args.path)


def _test_start(args):
    ww = _get_workload_wisdom(args)
    logging.info("starting project %s on testbed %s", args.project, args.testbed)
    test = ww.start_test_by_name(
        project_name=args.project,
        testbed_name=args.testbed,
        duration=args.duration
    )

    complete = ww.wait_until_test_complete(test['id'])
    ww.save_all_test_results(complete, args.path)


def _test_stop(args):
    ww = _get_workload_wisdom(args)

    if args.id:
        logging.info("stop test by id: %s", args.id)
        test = ww.stop_test(test_id=args.id)
    elif args.project:
        logging.info("stop test by project name: %s", args.project)
        test = ww.stop_test_by_project_name(project_name=args.project)

    if test:
        ww.save_all_test_results(test, args.path)


def _composite_workload_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of composite workloads")
    ww.list_composite_workloads()


def _composite_workload_private(args):
    ww = _get_workload_wisdom(args)
    logging.info("set composite workload %s privacy", args.name)
    composite = ww.get_composite_workload_by_name(args.name)
    ww.set_project_privacy(composite['id'], args.yes)


def _composite_workload_show(args):
    ww = _get_workload_wisdom(args)
    logging.info("show composite workload %s", args.name)
    ww.get_composite_workload_by_name(args.name)


def _composite_workload_delete(args):
    ww = _get_workload_wisdom(args)
    logging.info("delete a composite workload %s", args.name)
    composite = ww.get_composite_workload_by_name(args.name)
    ww.delete_composite_workload(composite['id'])


def _composite_workload_clone(args):
    ww = _get_workload_wisdom(args)
    logging.info("clone composite workload %s to %s", args.old, args.new)
    old = ww.get_composite_workload_by_name(args.old)
    ww.clone_composite_workload(workload_id=old['id'], new_name=args.new)


def _iteration_suites_list(args):
    ww = _get_workload_wisdom(args)
    logging.info("list of iteration test suites")
    ww.list_iteration_suite()

def _iteration_suites_show(args):
    ww = _get_workload_wisdom(args)
    if args.id:
        logging.info("show iteration test suite by id: %s", args.id)
        ww.show_iteration_suite(args.id)
    elif args.name:
        logging.info("show iteration test suite by name: %s", args.name)
        ww.get_iteration_suite_by_name(args.name)

def _iteration_test_suites_start(args):
    ww = _get_workload_wisdom(args)

    logging.info("starting an iteration test suite %s on testbed %s", args.name, args.testbed)
    iteration = ww.start_iteration_test_suite_by_name(
        iteration_suite_name=args.name,
        testbed_name=args.testbed,
    )

    ww.wait_until_iteration_complete(iteration['id'])

def _iteration_test_suites_stop(args):
    ww = _get_workload_wisdom(args)

    if args.id:
        logging.info("stop iteration test suite by id: %s", args.id)
        ww.stop_iteration_test_suite(iteration_test_suite_id=args.id)
    elif args.name:
        logging.info("stop iteration test suite by name: %s", args.name)
        ww.stop_iteration_test_suite_by_name(iteration_suite_name=args.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--ip', action="store", default='10.228.56.32', help="WorkloadWisdom IP")
    parser.add_argument('-u', '--username', action="store", required=True, help="WorkloadWisdom Username")
    parser.add_argument('-p', '--password', action="store", required=True, help="WorkloadWisdom Password")

    sub_parser = parser.add_subparsers(help="Workloader Command help")

    # Generator Module
    gen_parser = sub_parser.add_parser('generator', help='Generator Module')
    gen_sub_parser = gen_parser.add_subparsers(help="Action to perform")
    gen_list_parser = gen_sub_parser.add_parser('list', help='List of generators')
    gen_show_parser = gen_sub_parser.add_parser('show', help='Show a generator')
    gen_show_parser.add_argument('-name', action='store', help='Name of the generator')
    gen_list_parser.set_defaults(func=_generator_list)
    gen_show_parser.set_defaults(func=_generator_show)

    # Workload Module
    workload_parser = sub_parser.add_parser('workload', help='Workloads Module')
    workload_sub_parser = workload_parser.add_subparsers(help="Action to perform")
    # list
    workload_list_parser = workload_sub_parser.add_parser('list', help='List of workloads')
    # private
    workload_private_parser = workload_sub_parser.add_parser('private', help='Private a workload')
    workload_private_parser.add_argument('-name', action='store', help='Name of the workload to private')
    workload_private_parser.add_argument('-yes', action='store_true', help='Workload is set to private if specified')
    # show
    workload_show_parser = workload_sub_parser.add_parser('show', help='Show a workload')
    workload_show_parser.add_argument('-name', action='store', help='Name of the workload to show')
    # delete
    workload_del_parser = workload_sub_parser.add_parser('delete', help='Delete a workload')
    workload_del_parser.add_argument('-name', action='store', help='Name of the workload to delete')
    # clone
    workload_clone_parser = workload_sub_parser.add_parser('clone', help='Clone a workload')
    workload_clone_parser.add_argument('-old', action='store', help='Name of the old workload')
    workload_clone_parser.add_argument('-new', action='store', help='Name of the new workload')

    workload_list_parser.set_defaults(func=_workloads_list)
    workload_private_parser.set_defaults(func=_workloads_private)
    workload_show_parser.set_defaults(func=_workloads_show)
    workload_del_parser.set_defaults(func=_workloads_delete)
    workload_clone_parser.set_defaults(func=_workloads_clone)

    # Testbed Module
    tb_parser = sub_parser.add_parser('testbed', help='Testbeds Module')
    tb_sub_parser = tb_parser.add_subparsers(help="Action to perform")
    # list
    tb_list_parser = tb_sub_parser.add_parser('list', help='List of testbeds')
    # private
    tb_private_parser = tb_sub_parser.add_parser('private', help='Private a testbed')
    tb_private_parser.add_argument('-name', action='store', help='Name of the testbed to private')
    tb_private_parser.add_argument('-yes', action='store_true', help='Testbed is set to private if specified')
    # show
    tb_show_parser = tb_sub_parser.add_parser('show', help='Show a testbed')
    tb_show_parser.add_argument('-name', action='store', help='Name of the testbed to show')
    # delete
    tb_del_parser = tb_sub_parser.add_parser('delete', help='Delete a testbed')
    tb_del_parser.add_argument('-name', action='store', help='Name of the testbed to delete')
    # clone
    tb_clone_parser = tb_sub_parser.add_parser('clone', help='Clone a testbed')
    tb_clone_parser.add_argument('-old', action='store', help='Name of the old testbed')
    tb_clone_parser.add_argument('-new', action='store', help='Name of the new testbed')

    tb_list_parser.set_defaults(func=_testbed_list)
    tb_private_parser.set_defaults(func=_testbed_private)
    tb_show_parser.set_defaults(func=_testbed_show)
    tb_del_parser.set_defaults(func=_testbed_delete)
    tb_clone_parser.set_defaults(func=_testbed_clone)

    # Test Module
    test_parser = sub_parser.add_parser('test', help='Tests Module')
    test_sub_parser = test_parser.add_subparsers(help="Action to perform")
    # list
    test_list_parser = test_sub_parser.add_parser('list', help='List of tests')
    # show
    test_show_parser = test_sub_parser.add_parser('show', help='Show a test')
    test_show_parser.add_argument('-id', action='store', help='Id of the test to show')
    test_show_parser.add_argument('-path', action='store', default='./', help='Path to store the test results')
    # start
    test_start_parser = test_sub_parser.add_parser('start', help='Start a test')
    test_start_parser.add_argument('-project', action='store', help='Name of the project to start')
    test_start_parser.add_argument('-testbed', action='store', help='Name of the testbed under test')
    test_start_parser.add_argument('-duration', action='store', help='Duration of the test in seconds')
    test_start_parser.add_argument('-path', action='store', default='./', help='Path to store the test results')
    # stop, either by id or by name
    test_stop_parser = test_sub_parser.add_parser('stop', help='Stop a test')
    group = test_stop_parser.add_mutually_exclusive_group()
    group.add_argument('-id', action='store', help='Id of the test to stop')
    group.add_argument('-project', action='store', help='Name of the project to stop')
    test_stop_parser.add_argument('-path', action='store', default='./', help='Path to store the test results')

    test_list_parser.set_defaults(func=_test_list)
    test_show_parser.set_defaults(func=_test_show)
    test_start_parser.set_defaults(func=_test_start)
    test_stop_parser.set_defaults(func=_test_stop)

    # Composite composite Module
    composite_parser = sub_parser.add_parser('composite', help='Composite workloads Module')
    composite_sub_parser = composite_parser.add_subparsers(help="Action to perform")
    # list
    composite_list_parser = composite_sub_parser.add_parser('list', help='List of composite workloads')
    # private
    composite_private_parser = composite_sub_parser.add_parser('private', help='Private a composite workload')
    composite_private_parser.add_argument('-name', action='store', help='Name of the composite to private')
    composite_private_parser.add_argument('-yes', action='store_true', help='composite workload is set to private if specified')
    # show
    composite_show_parser = composite_sub_parser.add_parser('show', help='Show a composite workload')
    composite_show_parser.add_argument('-name', action='store', help='Name of the composite workload to show')
    # delete
    composite_del_parser = composite_sub_parser.add_parser('delete', help='Delete a composite workload')
    composite_del_parser.add_argument('-name', action='store', help='Name of the composite workload to delete')
    # clone
    composite_clone_parser = composite_sub_parser.add_parser('clone', help='Clone a composite workload')
    composite_clone_parser.add_argument('-old', action='store', help='Name of the old composite workload')
    composite_clone_parser.add_argument('-new', action='store', help='Name of the new composite workload')

    composite_list_parser.set_defaults(func=_composite_workload_list)
    composite_private_parser.set_defaults(func=_composite_workload_private)
    composite_show_parser.set_defaults(func=_composite_workload_show)
    composite_del_parser.set_defaults(func=_composite_workload_delete)
    composite_clone_parser.set_defaults(func=_composite_workload_clone)

    # Iteration Suite Module
    iteration_parser = sub_parser.add_parser('iteration', help='Iteration suite Module')
    iteration_sub_parser = iteration_parser.add_subparsers(help="Action to perform")
    # list
    iteration_list_parser = iteration_sub_parser.add_parser('list', help='List of Iteration suites')
    # show
    iteration_show_parser = iteration_sub_parser.add_parser('show', help='Show an Iteration suite')
    show = iteration_show_parser.add_mutually_exclusive_group()
    show.add_argument('-id', action='store', help='Id of the iteration suite to show')
    show.add_argument('-name', action='store', help='Name of the iteration suite to show')
    # start
    iteration_start_parser = iteration_sub_parser.add_parser('start', help='Start an Iteration test suite')
    '''
        need to use iteration suite id, not iteration test suite id.
        a iteration suite contains multiple iteration test suites.
        iteration suite vs iteration test suites is similar to workload vs test
    '''
    # Iteration test suite part
    iteration_start_parser.add_argument('-name', action='store', help='Name of the Iteration suite to start')
    iteration_start_parser.add_argument('-testbed', action='store', help='Name of the testbed under test')
    # stop, either by id or by name
    iteration_stop_parser = iteration_sub_parser.add_parser('stop', help='Stop a Iteration test suite')
    stop = iteration_stop_parser.add_mutually_exclusive_group()
    stop.add_argument('-id', action='store', help='Id of the iteration test suite to stop')
    # iteration test suite does not has a name
    stop.add_argument('-name', action='store', help='Name of the iteration suite to stop')

    iteration_list_parser.set_defaults(func=_iteration_suites_list)
    iteration_show_parser.set_defaults(func=_iteration_suites_show)
    iteration_start_parser.set_defaults(func=_iteration_test_suites_start)
    iteration_stop_parser.set_defaults(func=_iteration_test_suites_stop)

    args = parser.parse_args()
    args.func(args)


def show_logo(logo_file='/opt/workloader/.workloaderascii'):
    try:
        p = open(logo_file, "r")
        logo = p.read()
        p.close()
        logging.info("\n" + logo)
    except:
        logging.warn("failed to find %s", logo_file)
        return


if __name__ == "__main__":
    log_file = './workloader.log'
    logging.basicConfig(
        format=LOGGING_FORMAT,
        level=logging.DEBUG,
        datefmt=DATE_FORMAT,
        filename=log_file,
        filemode='w'
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(datefmt=DATE_FORMAT, fmt=LOGGING_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    show_logo()
    main()
