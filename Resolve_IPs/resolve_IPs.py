
import socket
import argparse
import sys

parser = argparse.ArgumentParser(description="Resolve required AMP Addresses to IPs.")
parser.add_argument('--NAM', action="store_true", help="Display IPs for AMP North America.")
parser.add_argument('--EU', action="store_true", help="Display IPs for AMP Europe.")
parser.add_argument('--APJC', action="store_true", help="Display IPs for AMP Asia/Pacific.")
parser.add_argument('--TGNAM', action="store_true", help="Display IPs for Threatgrid North America.")
parser.add_argument('--TGEU', action="store_true", help="Display IPs for Threatgrid Europe.")
args = parser.parse_args()

class AMPIPs():

    def print_info(self, name, IPList):

        print(f"\n {'*'*50}\n")
        print(f"IP List for {name}:\n")
        [print(IP) for IP in IPList]
        print(f"\n {'*'*50}\n")

    def resolveAddresses(self, name, AddressList):
        
        IPList = []
        for addr in AddressList:
            try:
                results = socket.getaddrinfo(addr,0,0,0,0)
            except socket.gaierror as e:
                print(f"Unable to resolve address {addr}.")
            for result in results:
                IPList.append(result[-1][0])
        self.print_info(name, list(set(IPList)))


NAMAddressList = [
    "cloud-ec.amp.cisco.com",
    "cloud-ec-asn.amp.cisco.com",
    "cloud-ec-est.amp.cisco.com",
    "console.amp.cisco.com",
    "mgmt.amp.cisco.com",
    "intake.amp.cisco.com",
    "policy.amp.cisco.com",
    "crash.amp.cisco.com",
    "tetra-defs.amp.cisco.com",
    "clam-defs.amp.cisco.com",
    "custom-signatures.amp.cisco.com",
    "rff.amp.cisco.com",
    "android.amp.sourcefire.com",
    "cloud-ios-asn.amp.cisco.com",
    "cloud-ios-est.amp.cisco.com",
    "cloud-pc.amp.sourcefire.com",
    "cloud-pc-est.amp.cisco.com",
    "cloud-pc-asn.amp.cisco.com",
    "cloud-pc.amp.cisco.com",
    "packages.amp.sourcefire.com",
    "packages-v2.amp.sourcefire.com",
    "pc-packages.amp.cisco.com",
    "support-sessions.amp.sourcefire.com",
    "cloud-dc.amp.sourcefire.com",
    "cloud-sa.amp.sourcefire.com",
    "cloud-sa.amp.cisco.com",
    "export.amp.sourcefire.com",
    "export.amp.cisco.com",
    "api.amp.sourcefire.com",
    "api.amp.cisco.com",
    "api.amp.sourcefire.com",
    "intel.api.sourcefire.com",
    "panacea.threatgrid.com",
    "fmc.api.threatgrid.com",
    "cloud-sa.amp.cisco.com",
    "cloud-sa.amp.sourcefire.com",
    "panacea.threatgrid.com",
    "cloud-meraki-asn.amp.cisco.com",
    "cloud-meraki-est.amp.cisco.com",
    "orbital.amp.cisco.com",
    "ncp.orbital.amp.cisco.com",
    "update.orbital.amp.cisco.com"
    ]

EUAddressList = [
    "cloud-ec.eu.amp.cisco.com",
    "cloud-ec-asn.eu.amp.cisco.com",
    "cloud-ec-est.eu.amp.cisco.com",
    "console.eu.amp.cisco.com",
    "mgmt.eu.amp.cisco.com",
    "intake.eu.amp.cisco.com",
    "policy.eu.amp.cisco.com",
    "upgrades.eu.amp.cisco.com",
    "crash.eu.amp.cisco.com",
    "ioc.eu.amp.cisco.com",
    "tetra-defs.eu.amp.cisco.com",
    "clam-defs.eu.amp.cisco.com",
    "custom-signatures.eu.amp.cisco.com",
    "rff.eu.amp.cisco.com",
    "android.eu.amp.sourcefire.com",
    "cloud-ios-asn.eu.amp.cisco.com",
    "cloud-ios-est.eu.amp.cisco.com",
    "cloud-pc.eu.amp.sourcefire.com",
    "cloud-pc-est.eu.amp.cisco.com",
    "cloud-pc-asn.eu.amp.cisco.com",
    "cloud-pc.eu.amp.cisco.com",
    "packages.amp.sourcefire.com",
    "packages-v2.amp.sourcefire.com",
    "pc-packages.amp.cisco.com",
    "support-sessions.amp.sourcefire.com",
    "cloud-dc.eu.amp.sourcefire.com",
    "cloud-sa.eu.amp.sourcefire.com",
    "cloud-sa.eu.amp.cisco.com",
    "export.eu.amp.sourcefire.com",
    "export.eu.amp.cisco.com",
    "api.amp.sourcefire.com",
    "api.eu.amp.sourcefire.com",
    "api.amp.sourcefire.com",
    "api.eu.amp.cisco.com",
    "intel.api.sourcefire.com",
    "panacea.threatgrid.eu",
    "fmc.api.threatgrid.eu",
    "cloud-sa.eu.amp.cisco.com",
    "cloud-sa.eu.amp.sourcefire.com",
    "panacea.threatgrid.eu",
    "cloud-meraki-asn.eu.amp.cisco.com",
    "cloud-meraki-est.eu.amp.cisco.com",
    "orbital.eu.cisco.com",
    "ncp.orbital.eu.amp.cisco.com",
    "update.orbital.eu.amp.cisco.com"
]

APJCAddressList = [
    "cloud-ec.apjc.amp.cisco.com",
    "cloud-ec-asn.apjc.amp.cisco.com",
    "cloud-ec-est.apjc.amp.cisco.com",
    "console.apjc.amp.cisco.com",
    "mgmt.apjc.amp.cisco.com",
    "intake.apjc.amp.cisco.com",
    "policy.apjc.amp.cisco.com",
    "upgrades.apjc.amp.cisco.com",
    "crash.apjc.amp.cisco.com",
    "ioc.apjc.amp.cisco.com",
    "tetra-defs.apjc.amp.cisco.com",
    "clam-defs.apjc.amp.cisco.com",
    "custom-signatures.apjc.amp.cisco.com",
    "rff.apjc.amp.cisco.com",
    "android.apjc.amp.cisco.com",
    "cloud-ios-asn.apjc.amp.cisco.com",
    "cloud-ios-est.apjc.amp.cisco.com",
    "cloud-pc.amp.sourcefire.com",
    "cloud-pc-est.amp.cisco.com",
    "cloud-pc-asn.amp.cisco.com",
    "cloud-pc.amp.cisco.com",
    "packages.amp.sourcefire.com",
    "packages-v2.amp.sourcefire.com",
    "pc-packages.amp.cisco.com",
    "support-sessions.amp.sourcefire.com",
    "cloud-dc.apjc.amp.sourcefire.com",
    "cloud-sa.apjc.amp.sourcefire.com",
    "cloud-sa.apjc.amp.cisco.com",
    "export.apjc.amp.sourcefire.com",
    "export.apjc.amp.cisco.com",
    "api.apjc.amp.sourcefire.com",
    "api.amp.sourcefire.com",
    "api.amp.sourcefire.com",
    "api.apjc.amp.cisco.com",
    "cloud-sa.apjc.amp.cisco.com",
    "cloud-sa.apjc.amp.sourcefire.com",
    "cloud-meraki-asn.apjc.amp.cisco.com",
    "cloud-meraki-est.apjc.amp.cisco.com",
    "orbital.apjc.amp.cisco.com",
    "ncp.orbital.apjc.amp.cisco.com",
    "update.orbital.apjc.amp.cisco.com"
]

TGNAMAddressList = [
    "panacea.threatgrid.com",
    "glovebox.mtv.threatgrid.com",
    "glovebox.rcn.threatgrid.com",
    "fmc.api.threatgrid.com"
]

TGEUAddressList = [
    "panacea.threatgrid.eu",
    "glovebox.threatgrid.eu",
    "fmc.api.threatgrid.eu"
]

AddressLists = {
    "AMP NAM":NAMAddressList,
    "AMP EU":EUAddressList,
    "AMP APJC":APJCAddressList,
    "Threatgrid NAM":TGNAMAddressList,
    "Threatgrid EU":TGEUAddressList
    }





if not len(sys.argv) > 1:
    for name, IPList in AddressLists.items():
        AMPIPs().resolveAddresses(name, IPList)

if args.NAM:
    AMPIPs().resolveAddresses("AMP NAM Addresses", AddressLists['AMP NAM'])
if args.EU:
    AMPIPs().resolveAddresses("AMP EU Addresses", AddressLists['AMP EU'])
if args.APJC:
    AMPIPs().resolveAddresses("AMP APJC Addresses", AddressLists['AMP APJC'])
if args.TGNAM:
    AMPIPs().resolveAddresses("Threatgrid NAM Addresses", AddressLists['Threatgrid NAM'])
if args.TGEU:
    AMPIPs().resolveAddresses("Threatgrid EU Addresses", AddressLists['Threatgrid EU'])
