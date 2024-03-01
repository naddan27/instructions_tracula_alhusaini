import os
import pydicom
from glob import glob

data_dir = "/users/dkim39/data/dkim39/maddata/PD/data/DTI"
scans_to_look_at = [
'3102', '3105'
]

scan_dict = dict()
for x in scans_to_look_at:
	scan_dict[x] = {"epifactor": [], "bandwidthperpixelphaseencode": [], "Manufacturer": [], "Rows": [], "Columns": [], "TE": []}

for x in scans_to_look_at:
	file_names = glob(os.path.join(data_dir, x, "DTI", "*", "*", "*_1_S*"))
	for fn in file_names:
		ds = pydicom.filereader.dcmread(fn)
		scan_dict[x]["TE"].append(ds[0x0018,0x0081].value)
		scan_dict[x]["epifactor"].append(ds[0x0018,0x0089].value)
		
		try:
			scan_dict[x]["bandwidthperpixelphaseencode"].append(ds[0x0019,0x1028].value)
		except:
			scan_dict[x]["bandwidthperpixelphaseencode"].append(24.284) # mode of values
		
		scan_dict[x]["Manufacturer"].append(ds[0x0008,0x0070].value)
		scan_dict[x]["Rows"].append(ds[0x0028,0x0010].value)
		scan_dict[x]["Columns"].append(ds[0x0028,0x0011].value)

for k in scan_dict.keys():
	print(k, ":", scan_dict[k])	
