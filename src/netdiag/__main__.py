#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import http.client
import json
import sys
from urllib.parse import quote

import click

from netdiag import config

settings = config.Settings()

@click.group()
def main():
    pass

@click.command()
@click.option('--mrid', help='seed conducting equipment mrid to run downstream trace from')
def incorrect_phases(mrid):
    """Performs downstream trace from seed equipment to find equipments with no equipment container and then
    performs an upstream trace from there to find equipments with no common phases. The implementation has some limitations.
    When doing an upstream trace it only picks the first one out of the list. Also the upstream trace goes into an infinite loop
    when it finds a loop in the network"""
    connection = http.client.HTTPConnection(host=settings.ewb_host, port=settings.ewb_port) if "http" \
        else http.client.HTTPSConnection(host=settings.ewb_host, port=settings.ewb_port)

    payload = {"assets": [{"id": mrid}]}
    json_payload = json.dumps(payload)
    connection.request("POST",
                       '/ewb/network/trace/api/v1/isolation?filter=results.assets(id,equipmentContainers,connections.normalPhases)',
                       json_payload)
    isolation_response = json.loads(connection.getresponse().read().decode('utf-8'))
    if ("errors" in isolation_response and len(isolation_response["errors"]) > 0):
        print(isolation_response["errors"])
        print("If the issue is a parallel feed then pick an equipment more downstream")
        return

    assetsWithNoContainers = []
    for asset in isolation_response["results"][0]["assets"]:
        if len(asset["equipmentContainers"]) == 0:
            phases = asset["connections"][0]["normalPhases"]
            print(f'Identified equipment with no equipment container: {asset["id"]} : {phases}')
            assetsWithNoContainers.append({"id": asset["id"], "phases": phases})

    for asset in assetsWithNoContainers:
        next_asset = asset["id"]

        print("-------------------------------------------------")
        print(asset["id"], asset["phases"])

        while 1:
            connection.request("GET",
                               f'/ewb/network/trace/api/v1/upstream/asset/{quote(next_asset, safe="")}?filter=assets(id,connections.normalPhases)')
            upstream_response = json.loads(connection.getresponse().read().decode('utf8'))

            if ("errors" in upstream_response and len(upstream_response["errors"]) > 0):
                print(upstream_response["errors"])
                break

            upstream_asset = upstream_response["assets"][0]
            upstream_asset_phases = upstream_asset["connections"][0]["normalPhases"]

            if len(list(set(upstream_asset_phases) & set(asset["phases"]))) == 0:
                print(f'Issue asset: {upstream_asset["id"]} {upstream_asset_phases}')
                break

            next_asset = upstream_asset["id"]

        print("-------------------------------------------------")
        return 0

main.add_command(incorrect_phases)

if __name__ == '__main__':
    sys.exit(main())
