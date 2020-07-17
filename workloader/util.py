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

import requests
import logging
import json

from requests.auth import HTTPBasicAuth

LOGGER = logging.getLogger(__name__)


def save_to_file(local_file, content):
    """Save data into a file.

    :param local_file: file name containing full path
    :param content: data to be write into the file
    """

    try:
        p = open(local_file, "w")
        p.write(content)
        p.close()
        LOGGER.info("saved file to: %s", local_file)
    except:
        LOGGER.error("failed saving log file %s", local_file)
        raise

def dump_json(dict):
    """Dump the dict with formatting.

    :param dict: JSON object to be dumped
    """

    if dict:
        LOGGER.debug(json.dumps(dict, indent=4, sort_keys=True))
    else:
        raise ValueError("input cannot be None")


def rest_get(api, username, password, json=True):
    """Sends a GET request with specific API. Returns :JSON of `Response` object.

    :param api: api for the post request
    :param username: username
    :param password: password
    :param json: return json or raw content
    :rtype: requests.Response.json()
    """

    resp = requests.get(api, auth=HTTPBasicAuth(username, password))
    if resp.ok:
        if json:
            return resp.json()
        else:
            return resp.content
    else:
        LOGGER.error("%s", resp.content)
        raise requests.exceptions.RequestException(resp.reason)


def rest_post(api, username, password, data=None, json=None):
    """Sends a POST request with specific API. Returns :JSON of `Response` object.

    :param api: api for the post request
    :param username: username
    :param password: password
    :param data: data for the post request
    :param json: json for the post request
    :rtype: requests.Response.json()
    """

    resp = requests.post(api, data, json, auth=HTTPBasicAuth(username, password))
    if resp.ok:
        return resp.json()
    else:
        LOGGER.error("%s", resp.content)
        raise requests.exceptions.RequestException(resp.reason)


def rest_delete(api, username, password):
    """Sends a DELETE request with specific API. Returns :JSON of `Response` object.

    :param api: api for the delete request
    :param username: username
    :param password: password
    :rtype: requests.Response.json()
    """

    resp = requests.delete(api, auth=HTTPBasicAuth(username, password))
    if resp.ok:
        return resp.json()
    else:
        LOGGER.error("%s", resp.content)
        raise requests.exceptions.RequestException(resp.reason)


def rest_put(api, username, password, data=None):
    """Sends a PUT request with specific API. Returns :JSON of `Response` object.

    :param api: api for the put request
    :param username: username
    :param password: password
    :param data: data for the put request
    :rtype: requests.Response.json()
    """

    resp = requests.put(api, data, auth=HTTPBasicAuth(username, password))
    if resp.ok:
        return resp.json()
    else:
        LOGGER.error("%s", resp.content)
        raise requests.exceptions.RequestException(resp.reason)