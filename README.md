[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/j-sulliman/iabg)

# iABG - Intersight AsBuilt Generator - CLI Edition

Automatic generation of base AsBuilt documents for Intersight.

*This is a custom version of iABG that only use the CLI.*

Reports on:
* Firmware
* Blade and rackmount servers
* Hyperflex
* FC and Ethernet Interfaces
* Service Profiles
* Management Interfaces

Overview: 
* Uses the intersight_rest API to pull data from Intersight.
* Data retrieved from API call is stored in a dataframe using the pandas module.
* Dataframes then written to an excel workbook.

# Setup

*Virtual Environment Windows*
```powershell
python -m venv venv
.\venv\Scripts\activate
```
*Virtual Environment Linux*
```bash
$ virtualenv venv
$ source venv/bin/activate
```

*Pull the repo from git*
```bash
git init
git pull https://github.com/rlilaud/iabg.git

# Install the required dependencies:
cd is
pip install -r ./requirements.txt
```

# How to use?

*Configuration of the API key*
* Put your public API key in `./is/key/key.txt`
* Put your private API key in `./is/key/SecretKey.txt`

NOTE: When you create your API key on Intersight, you need to choose: "*API key for OpenAPI schema version 2*"

To run iABG, you only need to run the `./is/main.py` script. You will then get a prompt asking if you want to change the default address of Intersight. Leave it blank to use the default address.

```bash
# Example

~$ python ./main.py
#######################################
#                                     #
# iABG - Intersight AsBuilt Generator #
#                                     #
#######################################

Leave blank to choose the default address - "https://intersight.com"
==> INTERSIGHT ADDRESS:

HOST: https://intersight.com

Status code 200, for resource path /compute/Blades
Status code 200, for resource path /compute/PhysicalSummaries
Status code 200, for resource path /compute/RackUnits
Status code 200, for resource path /ether/PhysicalPorts
Status code 200, for resource path /fc/PhysicalPorts
Status code 200, for resource path /firmware/RunningFirmwares
Status code 200, for resource path /hyperflex/Clusters
Status code 200, for resource path /hyperflex/Nodes
Status code 200, for resource path /hyperflex/Healths
Status code 200, for resource path /server/Profiles
Status code 200, for resource path /management/Interfaces

Result save in "export/intersight_output.xlsx"
```

Excel Workbook:
![alt text](https://github.com/j-sulliman/j-sulliman.github.io/blob/master/images/excel.PNG?raw=true)