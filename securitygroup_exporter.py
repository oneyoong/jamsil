# -----------------------------------------------------------------------
#
# Security Group Exporter
#
# This script exports the current security group in AWS.
# The exported format is *.csv, for administartor's convenience.
#
# MJ Kim, SDS, 2012.12
#
# Dependencies : Python 2.7.x, boto 2.6.0
#
# -----------------------------------------------------------------------

#! /usr/bin/env python

import boto, re, datetime
from boto.ec2.connection import EC2Connection

# -----------------------------------------------------------------------
# AWS Crendentials
#
# Be aware of the security threaten if these keys would be leaked to bad people
# -----------------------------------------------------------------------

import account

# -----------------------------------------------------------------------
# AWS Regions
# -----------------------------------------------------------------------

# The orders
#
# NA (Virginia, California, Oregon)
# EU (Ireland)
# AP (Singapore, Tokyo, Sydney)
# SA (Sao Paulo)

aws_regions = ['us-east-1', 'us-west-1', 'us-west-2',
               'eu-west-1',
               'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2',
               'sa-east-1']

# -----------------------------------------------------------------------
# print format
#
# REGION_NAME || SECURITY_GROUP_NAME || INBOUND_PROTOCOL || INBOUND_PORT || INBOUND_IPS || OUTBOUND_PROTOCOL || OUTBOUND_PORT || OUTBOUND_IPS || ASSOICATED_INSTANCES
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# Utility function for iterate the permissions list
# -----------------------------------------------------------------------

def iter_permissions(permissions, output_list):
    for current_permission in permissions:
        protocol = str(current_permission.ip_protocol)

        # '-1' is all source ips
        if protocol == '-1':
            protocol = 'all'
        
        port = str(current_permission.from_port) + '-' + str(current_permission.to_port)

        grant_ips = current_permission.grants
        for ip in grant_ips:
            # Delete the owner id if the ip indicates other security group
            ip = str(ip)
            is_security_group = re.findall(r'sg', ip)
            if len(is_security_group) > 0:
                ip = ip[:10]
            output_list.append(protocol + ',' + port + ',' + ip)

# -----------------------------------------------------------------------
# Start to process
# -----------------------------------------------------------------------

# For naming the output file
today = datetime.date.today()
today = today.strftime("%y-%m-%d")

# For each account
for idx_account in range(len(account.account_list)):

    # Get credentials
    credentials = account.aws_credentials[account.account_list[idx_account]]
    accesskey = credentials['ACCESS_KEY']
    secretkey = credentials['SECRET_KEY']

    # Final result
    result_list = []
    
    # For each region
    for idx_region in range(len(aws_regions)):

        # Connect and get all security groups in this region
        ec2_conn = boto.ec2.connect_to_region(aws_regions[idx_region], aws_access_key_id=accesskey, aws_secret_access_key=secretkey)
        security_groups = ec2_conn.get_all_security_groups()

        # This is only for printing. It prints Region name at first line only.
        is_first_sg = True

        for sg in security_groups:

            sgname = str(sg.name)

            # Step 1. Retrieve all inbound rules
            inbound_permissions = sg.rules
            inbound_list = []
            iter_permissions(inbound_permissions, inbound_list)

            # Step 2. Retrieve all outbound rules
            outbound_permissions = sg.rules_egress
            outbound_list = []
            iter_permissions(outbound_permissions, outbound_list)

            # Step 3. Merging the two result list
            # Each length of two lists can be different
            merged_list = []
            len_inbound_list = len(inbound_list)
            len_outbound_list = len(outbound_list)

            for idx in range(max(len_inbound_list, len_outbound_list)):
                merging_string = ''
                if idx < len_inbound_list:
                    merging_string += inbound_list[idx]
                else:
                    merging_string += ',,'
                
                merging_string += ','

                if idx < len_outbound_list:
                    merging_string += outbound_list[idx]
                else:
                    merging_string += ',,'

                merged_list.append(merging_string)

            # Write down the current security groups infomation into *.csv format 
            for idx in range(len(merged_list)):
                if is_first_sg == True:
                    if idx == 0:
                        result_list.append(aws_regions[idx_region] + ',' + sgname + ',' + merged_list[idx] + '\n')
                        is_first_sg = False
                    else:
                        result_list.append(',,' + merged_list[idx] + '\n')
                else:
                    if idx == 0:
                        result_list.append(',' + sgname + ',' + merged_list[idx] + '\n')
                        is_first_sg = False
                    else:
                        result_list.append(',,' + merged_list[idx] + '\n')

    # End of each region

    # File output
    output_file = open('result-' + account.account_list[idx_account] + '-' + today + '.csv', 'w')

    # Header line
    header = 'Region,SG name,Inbound Protocol,Inbound Port,Inbound IPs,Outbound Protocol,Outbound Port, Outbound IPs\n'
    output_file.write(header)

    # Write the real contents
    for idx in range(len(result_list)):
        output_file.write(result_list[idx])

    #print result_list
    print account.account_list[idx_account] + ' was exported.'
    output_file.close()

# End of each account



