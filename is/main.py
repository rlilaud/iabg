from datetime import datetime
from intersight_get import intersight_get
import pandas as pd
import os
import argparse


# create a form instance and populate it with data from the request:


def createXLSX(host_link, public_api_key, private_api_key, filename):

    # API request:
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
    view_servers = intersight_get(resource_path='/view/Servers',
                                  host=host_link, private_key=private_api_key,
                                  public_key=public_api_key)
    adapter_Units = intersight_get(resource_path='/adapter/Units',
                                   host=host_link, private_key=private_api_key,
                                   public_key=public_api_key)
    equipment_Psus = intersight_get(resource_path='/equipment/Psus',
                                    host=host_link, private_key=private_api_key,
                                    public_key=public_api_key)
    equipment_FanModules = intersight_get(resource_path='/equipment/FanModules',
                                          host=host_link, private_key=private_api_key,
                                          public_key=public_api_key)
    storage_PhysicalDisks = intersight_get(resource_path='/storage/PhysicalDisks',
                                           host=host_link, private_key=private_api_key,
                                           public_key=public_api_key)
    storage_Controllers = intersight_get(resource_path='/storage/Controllers',
                                         host=host_link, private_key=private_api_key,
                                         public_key=public_api_key)
    memory_Units = intersight_get(resource_path='/memory/Units',
                                  host=host_link, private_key=private_api_key,
                                  public_key=public_api_key)
    equipment_Chasses = intersight_get(resource_path='/equipment/Chasses',
                                       host=host_link, private_key=private_api_key,
                                       public_key=public_api_key)
    capability_ChassisDescriptors = intersight_get(resource_path='/capability/ChassisDescriptors',
                                                   host=host_link, private_key=private_api_key,
                                                   public_key=public_api_key)
    equipment_IoCards = intersight_get(resource_path='/equipment/IoCards',
                                       host=host_link, private_key=private_api_key,
                                       public_key=public_api_key)
    fabric_ElementIdentities = intersight_get(resource_path='/fabric/ElementIdentities',
                                              host=host_link, private_key=private_api_key,
                                              public_key=public_api_key)
    asset_DeviceContractInformations = intersight_get(resource_path='/asset/DeviceContractInformations',
                                                      host=host_link, private_key=private_api_key,
                                                      public_key=public_api_key)
    network_ElementSummaries = intersight_get(resource_path='/network/ElementSummaries',
                                              host=host_link, private_key=private_api_key,
                                              public_key=public_api_key)
    equipment_tpms = intersight_get(resource_path='/equipment/Tpms',
                                    host=host_link, private_key=private_api_key,
                                    public_key=public_api_key)
    cond_HclStatusDetails = intersight_get(resource_path='/cond/HclStatusDetails',
                                           host=host_link, private_key=private_api_key,
                                           public_key=public_api_key)
    processor_units = intersight_get(resource_path='/processor/Units',
                                     host=host_link, private_key=private_api_key,
                                     public_key=public_api_key)

    # Clean data:
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

    view_servers_df = pd.DataFrame.from_dict(view_servers['Results'])
    view_servers_df = view_servers_df.filter(
        items=['AccountMoid', 'AssetDeviceContractInformation', 'AvailableMemory', 'ConnectionStatus', 'DeviceMoId', 'Dn', 'HardwareUuid', 'KvmIpAddresses', 'ManagementMode', 'MemorySpeed', 'MgmtIpAddress', 'Model', 'Moid', 'Name', 'PlatformType', 'Serial', 'ServerProfile', 'Uuid', 'ChassisId', 'SlotId'])

    adapter_Units_df = pd.DataFrame.from_dict(adapter_Units['Results'])
    adapter_Units_df = adapter_Units_df.filter(
        items=['AccountMoid', 'AdapterId', 'BaseMacAddress', 'DeviceMoId', 'Dn', 'Model', 'Moid', 'Presence', 'Serial'])

    equipment_Psus_df = pd.DataFrame.from_dict(equipment_Psus['Results'])
    equipment_Psus_df = equipment_Psus_df.filter(items=['AccountMoid', 'Description', 'DeviceMoid', 'Dn', 'Model',
                                                 'Moid', 'Name', 'OperState', 'Presence', 'PsuFwVersion', 'PsuId', 'PsuType', 'PsuWattage', 'Serial', 'Sku'])

    equipment_FanModules_df = pd.DataFrame.from_dict(
        equipment_FanModules['Results'])
    equipment_FanModules_df = equipment_FanModules_df.filter(
        items=['AccountMoid', 'Description', 'DeviceMoid', 'Dn', 'Model', 'ModuleId', 'Moid', 'OperState', 'Presence', 'Serial', 'Sku'])

    storage_PhysicalDisks_df = pd.DataFrame.from_dict(
        storage_PhysicalDisks['Results'])
    storage_PhysicalDisks_df = storage_PhysicalDisks_df.filter(items=['AccountMoid', 'DeviceMoid', 'DiskId', 'DiskState', 'Dn', 'DriveFirmware', 'DriveState',
                                                               'EncryptionStatus', 'FailurePredicted', 'Model', 'Moid', 'Name', 'OperPowerState', 'Pid', 'Presence', 'Protocol', 'Serial', 'Size', 'Type', 'Vendor'])

    storage_Controllers_df = pd.DataFrame.from_dict(
        storage_Controllers['Results'])
    storage_Controllers_df = storage_Controllers_df.filter(items=['AccountMoid', 'ControllerId', 'ControllerStatus', 'DeviceMoid', 'Dn', 'HwRevision', 'InterfaceType',
                                                           'InventoryDeviceInfo', 'Model', 'Moid', 'Name', 'OperState', 'PciAddr', 'PciSlot', 'Presence', 'RaidSupport', 'Serial', 'Type', 'Vendor'])

    memory_Units_df = pd.DataFrame.from_dict(memory_Units['Results'])
    memory_Units_df = memory_Units_df.filter(items=['AccountMoid', 'Capacity', 'Clock', 'DeviceMoid', 'Dn', 'FormFactor',
                                             'Location', 'MemoryId', 'Model', 'Moid', 'OperState', 'Operability', 'Presence', 'Serial', 'Type', 'Vendor'])

    equipment_Chasses_df = pd.DataFrame.from_dict(equipment_Chasses['Results'])
    equipment_Chasses_df = equipment_Chasses_df.filter(items=['AccountMoid', 'ChassisId', 'Description', 'DeviceMoid', 'Dn', 'ManagementInterface',
                                                       'ManagementMode', 'Model', 'Moid', 'Name', 'OperSate', 'PartNumber', 'Pid', 'ProductName', 'Serial', 'Sku', 'Vendor'])

    capability_ChassisDescriptors_df = pd.DataFrame.from_dict(
        capability_ChassisDescriptors['Results'])
    capability_ChassisDescriptors_df = capability_ChassisDescriptors_df.filter(
        items=['AccountMoid', 'Description', 'Model', 'Moid', 'Vendor', 'Version'])

    equipment_IoCards_df = pd.DataFrame.from_dict(equipment_IoCards['Results'])
    equipment_IoCards_df = equipment_IoCards_df.filter(items=['AccountMoid', 'DcSupported', 'Description', 'DeviceMoid', 'Dn', 'InbandIpAddresses',
                                                       'Model', 'ModuleId', 'Moid', 'OperState', 'PartNumber', 'Pid', 'Presence', 'ProductName', 'Serial', 'Side', 'Sku', 'Vendor', 'Version'])

    fabric_ElementIdentities_df = pd.DataFrame.from_dict(
        fabric_ElementIdentities['Results'])
    fabric_ElementIdentities_df = fabric_ElementIdentities_df.filter(
        items=['AccountMoid', 'Domain', 'Model', 'Moid', 'Serial', 'Vendor'])

    asset_DeviceContractInformations_df = pd.DataFrame.from_dict(
        asset_DeviceContractInformations['Results'])
    asset_DeviceContractInformations_df = asset_DeviceContractInformations_df.filter(
        items=['AccountMoid', 'Contract', 'ContractStatus', 'ContractUpdatedTime', 'DeviceId', 'DeviceType', 'EndCustomer', 'EndUserGlobalUltimate', 'IsValid', 'ItemType', 'Moid', 'PlatformType', 'PurchaseOrderNumber', 'SalesOrderNumber', 'Description', 'ServiceEndDate', 'ServiceStartDate', 'StateContract', 'WarrantyEndDate', 'WarrantyType'])

    network_ElementSummaries_df = pd.DataFrame.from_dict(
        network_ElementSummaries['Results'])
    network_ElementSummaries_df = network_ElementSummaries_df.filter(items=['AccountMoid', 'AdminInbandInterfaceState', 'BundleVersion', 'Chassis', 'ConnectionStatus', 'DeviceMoid', 'Dn', 'EthernetSwitchingMode', 'FcSwitchingMode', 'Firmware', 'FirmwareVersion', 'InbandIpAddress', 'InbandIpGateway',
                                                                     'InbandIpMask', 'InbandVlan', 'Ipv4Address', 'ManagementMode', 'Model', 'Moid', 'Name', 'NumEtherPorts', 'Operability', 'OutOfBandIpAddress', 'OutOfBandIpGateway', 'OutOfBandIpMask', 'OutOfBandMac', 'PartNumber', 'Serial', 'Status', 'SwitchType', 'SystemUpTime', 'Vendor', 'Version'])

    equipment_tpms_df = pd.DataFrame.from_dict(equipment_tpms['Results'])
    equipment_tpms_df = equipment_tpms_df.filter(items=['AccountMoid', 'ActivationStatus', 'AdminState', 'DeviceMoid',
                                                 'Dn', 'FirmwareVersion', 'InventoryDeviceInfo', 'Model', 'Moid', 'Presence', 'Serial', 'TpmId', 'Vendor', 'Version'])

    cond_HclStatusDetails_df = pd.DataFrame.from_dict(
        cond_HclStatusDetails['Results'])
    cond_HclStatusDetails_df = cond_HclStatusDetails_df.filter(items=['AccountMoid', 'HardwareStatus', 'HclCimcVersion', 'HclDriverName', 'HclDriverVersion', 'HclFirmwareVersion',
                                                               'HclModel', 'InvCimcVersion', 'InvDriverName', 'InvDriverVersion', 'InvFirmwareVersion', 'InvModel', 'Moid', 'Reason', 'SoftwareStatus', 'Status'])

    processor_units_df = pd.DataFrame.from_dict(processor_units['Results'])
    processor_units_df = processor_units_df.filter(items=['AccountMoid', 'Architecture', 'DeviceMoId', 'Dn', 'Model', 'Moid', 'NumCores',
                                                   'NumCoresEnabled', 'NumThreads', 'OperPowerState', 'OperState', 'Presence', 'ProcessorId', 'Serial', 'SocketDesignation', 'Speed', 'Vendor'])

    # Creation of the Excel sheet:
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
        compute_summary_df.to_excel(writer, sheet_name='compute_summary')
        blade_server_df.to_excel(writer, sheet_name='blade_server')
        view_servers_df.to_excel(writer, sheet_name='view_servers')
        adapter_Units_df.to_excel(writer, sheet_name='adapter_Units')
        equipment_Psus_df.to_excel(writer, sheet_name='psus')
        equipment_FanModules_df.to_excel(writer, sheet_name='FanModules')
        storage_PhysicalDisks_df.to_excel(writer, sheet_name='PhysicalDisks')
        storage_Controllers_df.to_excel(
            writer, sheet_name='storage_Controllers')
        memory_Units_df.to_excel(writer, sheet_name='memory_Units')
        equipment_Chasses_df.to_excel(writer, sheet_name='chassis')
        capability_ChassisDescriptors_df.to_excel(
            writer, sheet_name='ChassisDescriptors')
        equipment_IoCards_df.to_excel(writer, sheet_name='equipment_IoCards')
        fabric_ElementIdentities_df.to_excel(
            writer, sheet_name='fabric_ElementIdentities')
        asset_DeviceContractInformations_df.to_excel(
            writer, sheet_name='DeviceContract')
        network_ElementSummaries_df.to_excel(
            writer, sheet_name='network_Element')
        equipment_tpms_df.to_excel(
            writer, sheet_name='tpms')
        cond_HclStatusDetails_df.to_excel(
            writer, sheet_name='HclStatusDetails')
        processor_units_df.to_excel(
            writer, sheet_name='processor')

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
    # print(f"\nPUBLIC KEY: \n{public_api_key}")
    # print(f"\nPRIVATE KEY: \n{private_api_key}")
    print("")

    createXLSX(arguments[0], public_api_key, private_api_key, filename)
