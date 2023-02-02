from datetime import datetime
from intersight_get import intersight_get
import pandas as pd
import os
import argparse


# create a form instance and populate it with data from the request:


def createXLSX(host_link, public_api_key, private_api_key, filename):
    blade_server = intersight_get(resource_path='/compute/Blades',
                                  host=host_link, private_key=private_api_key, public_key=public_api_key)

    compute_summary = intersight_get(
        resource_path='/compute/PhysicalSummaries',
        host=host_link, private_key=private_api_key, public_key=public_api_key,
        query_params={
            "$select": "AvailableMemory,CpuCapacity,Dn,Firmware,Model,Name,OperPowerState,OperState"
        })
    rack_server = intersight_get(resource_path='/compute/RackUnits',
                                 host=host_link, private_key=private_api_key, public_key=public_api_key)
    physical_ports = intersight_get(
        resource_path='/ether/PhysicalPorts',
        host=host_link, private_key=private_api_key, public_key=public_api_key,
        query_params={
            "$filter": "OperState eq 'up'",
            "$orderby": "Dn",
            "$select": "AggregatePortId,Mode,Dn,OperSpeed,OperState,PeerDn,TransceiverType"
        })
    fc_ports = intersight_get(resource_path='/fc/PhysicalPorts',
                              host=host_link, private_key=private_api_key,
                              public_key=public_api_key,
                              query_params={
                                  "$filter": "OperState eq 'up'",
                                  "$orderby": "Dn",
                                  "$select": "PortChannelId,OperSpeed,Dn,Mode,OperState,Wwn"
                              })
    firmware_running = intersight_get(resource_path='/firmware/RunningFirmwares',
                                      host=host_link, private_key=private_api_key,
                                      public_key=public_api_key,
                                      query_params={
                                          "$orderby": "Type",
                                          "$select": "Dn,Type,Version,PackageVersion,ObjectType,Component"})
    hyperflex_cluster = intersight_get(resource_path='/hyperflex/Clusters',
                                       host=host_link, private_key=private_api_key,
                                       public_key=public_api_key,
                                       query_params={
                                           "$select": "Summary"})
    hyperflex_node = intersight_get(resource_path='/hyperflex/Nodes',
                                    host=host_link, private_key=private_api_key,
                                    public_key=public_api_key,
                                    query_params={
                                        "$select": "DisplayVersion,HostName,Ip,ModelNumber,Role,SerialNumber,Status,Version"})
    hyperflex_health = intersight_get(resource_path='/hyperflex/Healths',
                                      host=host_link, private_key=private_api_key,
                                      public_key=public_api_key,
                                      query_params={"$select": "ResiliencyDetails"})

    # Due to new call in the API, ls/ServiceProfiles is deprecated
    # service_profile = intersight_get(resource_path='/ls/ServiceProfiles',
    #     host=host_link, private_key=private_api_key,
    #     public_key=public_api_key,
    #                     query_params={"$filter": "AssignState eq 'assigned'", "$orderby": "OperState"})
    service_profile = intersight_get(resource_path='/server/Profiles',
                                     host=host_link, private_key=private_api_key,
                                     public_key=public_api_key,
                                     query_params={"$filter": "AssignedServer ne 'null'",
                                                   "$orderby": "ModTime"})
    management_address = intersight_get(resource_path='/management/Interfaces',
                                        host=host_link, private_key=private_api_key,
                                        public_key=public_api_key,
                                        query_params={
                                            "$select": "Dn,Ipv4Address,Ipv4Mask,Ipv4Gateway,MacAddress"})

    # if firmware_running == None:
    #    return render(request, 'is_abg/broke.html')

    management_df = pd.DataFrame.from_dict(
        management_address['Results'])
    management_df = management_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    service_profile_df = pd.DataFrame.from_dict(
        service_profile['Results'])
    service_profile_df = service_profile_df.drop(columns=['ClassId', 'Moid', 'ObjectType',
                                                          'Owners', 'DeviceMoId', 'DomainGroupMoid',
                                                          'CreateTime', 'PermissionResources',
                                                          'RegisteredDevice', 'Rn', 'SharedScope', 'Tags',
                                                          'ModTime', 'AccountMoid'], errors='ignore')
    hyperflex_health_df = pd.DataFrame.from_dict(
        hyperflex_health['Results'])
    hyperflex_node_df = pd.DataFrame.from_dict(
        hyperflex_node['Results'])
    hyperflex_node_df = hyperflex_node_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    hyperflex_cluster_df_list = []
    for i in hyperflex_cluster['Results']:
        # pp.pprint(i['Summary'])
        hyperflex_cluster_df = pd.DataFrame.from_dict(i['Summary'])
        hyperflex_cluster_df = hyperflex_cluster_df.drop(columns=['ClassId', 'ObjectType', 'Boottime',
                                                                  'CompressionSavings',
                                                                  'DeduplicationSavings', 'Downtime',
                                                                  'HealingInfo',
                                                                  'ResiliencyDetails', 'ResiliencyInfo',
                                                                  'ResiliencyDetailsSize', 'TotalSavings'],
                                                         errors='ignore')
        hyperflex_cluster_df.drop_duplicates()
        hyperflex_cluster_df_list.append(hyperflex_cluster_df)

    firmware_running_df = pd.DataFrame.from_dict(
        firmware_running['Results'])
    firmware_running_df = firmware_running_df.drop(columns=['ClassId', 'Moid', 'ObjectType'],
                                                   errors='ignore')
    fc_ports_df = pd.DataFrame.from_dict(fc_ports['Results'])
    fc_ports_df = fc_ports_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    physical_ports_df = pd.DataFrame.from_dict(
        physical_ports['Results'])
    physical_ports_df = physical_ports_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    rack_server_df = pd.DataFrame.from_dict(rack_server['Results'])
    compute_summary_df = pd.DataFrame.from_dict(
        compute_summary['Results'])
    compute_summary_df = compute_summary_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    blade_server_df = pd.DataFrame.from_dict(blade_server['Results'])

    firmware_running_df = pd.DataFrame.from_dict(
        firmware_running['Results'])
    firmware_running_df = firmware_running_df.drop(columns=['ClassId', 'Moid', 'ObjectType'],
                                                   errors='ignore')
    fc_ports_df = pd.DataFrame.from_dict(fc_ports['Results'])
    fc_ports_df = fc_ports_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    physical_ports_df = pd.DataFrame.from_dict(
        physical_ports['Results'])
    physical_ports_df = physical_ports_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    rack_server_df = pd.DataFrame.from_dict(rack_server['Results'])
    compute_summary_df = pd.DataFrame.from_dict(
        compute_summary['Results'])
    compute_summary_df = compute_summary_df.drop(
        columns=['ClassId', 'Moid', 'ObjectType'], errors='ignore')
    blade_server_df = pd.DataFrame.from_dict(blade_server['Results'])

    with pd.ExcelWriter(rf'export/{filename}') as writer:
        management_df.to_excel(writer, sheet_name='management')
        service_profile_df.to_excel(
            writer, sheet_name='service_profile')
        hyperflex_health_df.to_excel(
            writer, sheet_name='hyperflex_health')
        hyperflex_node_df.to_excel(writer, sheet_name='hyperflex_node')
        for hyperflex_cluster_unit_df in hyperflex_cluster_df_list:
            sheet_name = 'hyperflex_cluster_' + \
                hyperflex_cluster_unit_df["Name"].values[0]
            hyperflex_cluster_unit_df.to_excel(
                writer, sheet_name=sheet_name)
        firmware_running_df.to_excel(
            writer, sheet_name='firmware_running')
        fc_ports_df.to_excel(writer, sheet_name='fc_ports')
        physical_ports_df.to_excel(writer, sheet_name='physical_ports')
        rack_server_df.to_excel(writer, sheet_name='rack_server')
        compute_summary_df.to_excel(
            writer, sheet_name='compute_summary')
        blade_server_df.to_excel(writer, sheet_name='blade_server')

    print(f"\nResult save in \"export/{filename}\"")


def api_key(path):
    f = open(path, "r")
    return f.read()


def api_SecretKey(path):
    f = open(path, "r")
    return f.read()


def forge_filename():
    today = datetime.today().strftime('%Y-%m-%d-%H-%M')
    filename = f"intersight_output_{today}.xlsx"
    return filename


def arguments_cli():
    parser = argparse.ArgumentParser(
        description='iABG - Intersight AsBuilt Generator')
    parser.add_argument(
        '--host', help='Link to Intersight. Default: https://intersight.com')
    parser.add_argument(
        '--public-key', help='Path to the Public API key. Default: ./key/key.txt')
    parser.add_argument(
        '--private-key', help='Path to the Private API key. Default: ./key/SecretKey.txt')

    args = parser.parse_args()

    if args.host == None:
        args.host = "https://intersight.com"
    if args.public_key == None:
        args.public_key = "./key/key.txt"
    if args.private_key == None:
        args.private_key = "./key/SecretKey.txt"

    return [args.host, args.public_key, args.private_key]


if __name__ == '__main__':

    arguments = arguments_cli()
    # arguments[0] -> host
    # arguments[1] -> public api key
    # arguments[2] -> private api key

    print("#######################################\n#                                     #\n# iABG - Intersight AsBuilt Generator #\n#                                     #\n#######################################")

    public_api_key = api_key(arguments[1])
    private_api_key = api_SecretKey(arguments[2])
    filename = forge_filename()

    print(f"\nHOST: {arguments[0]}")
    #print(f"\nPUBLIC KEY: \n{public_api_key}")
    #print(f"\nPRIVATE KEY: \n{private_api_key}")
    print("")

    createXLSX(arguments[0], public_api_key, private_api_key, filename)
