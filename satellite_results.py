#!/usr/bin/python

import xmlrpclib

LOGINS = [("https://spacewalk.example.org/rpc/api", "admin", "password")]


def do_action(login, action_id):
    client = xmlrpclib.Server(login[0], verbose=0)
    key = client.auth.login(login[1], login[2])

    results = client.system.getScriptResults(key, action_id)
    for result in results:
        sid = result['serverId']
        sname = client.system.getName(key, int(sid))['name']
        ip = client.system.getNetwork(key, int(sid))['ip']

        if result['returnCode'] == 0:
            print "Server %s(%s) executed the command succesfully" % (sname, ip)
        else:
            print "Server %s(%s) had problems executing the command: %s" % (
                sname,
                ip,
                result['output'])

    client.auth.logout(key)

action_id = '12345'

for login in LOGINS:
    do_action(login, action_id)
