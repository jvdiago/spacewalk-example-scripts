#!/usr/bin/python

import xmlrpclib

LOGINS = [("https://spacewalk.example.org/rpc/api", "admin", "password")]


def do_action(login, script):
    client = xmlrpclib.Server(login[0], verbose=0)
    key = client.auth.login(login[1], login[2])
    list = client.system.listUserSystems(key)

    for server in list:
        sid = server.get('id')
        print 'Executing script in %s' % server.get('name')
        earliest_occurrence = xmlrpclib.DateTime()
        try:
            client.system.scheduleScriptRun(
                key,
                int(sid),
                "root",
                "root",
                300,
                script,
                earliest_occurrence)
        except:
            print 'Not supported'

    client.auth.logout(key)

script = 'hostname -f'

for login in LOGINS:
    do_action(login, script)
