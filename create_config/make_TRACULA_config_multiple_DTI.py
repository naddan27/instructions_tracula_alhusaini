import os
import glob
import check_if_metadata_present 
from tqdm import tqdm

subjects_dir = "/users/dkim39/data/dkim39/maddata/PD/data/reconall_output" # T1 images and FreeSurfer segmentations are expected to be found here
dtroot = "/users/dkim39/data/dkim39/maddata/PD/output"  # output directory where trac-all results will be saved
dti_data = "/users/dkim39/data/dkim39/maddata/PD/data/DTI" # directory where the diffusion images are

for x in tqdm(check_if_metadata_present.scans_to_look_at):
	config = open("./config_files/tracula_" + str(x) + ".config", "w+")

	config.write("# T1 images and FreeSurfer segmentations are expected to be found here\n")
	config.write("setenv SUBJECTS_DIR " + str(subjects_dir) + "\n")

	config.write("# Output directory where trac-all results will be saved\n")
	config.write("set dtroot = " + str(dtroot) + "\n\n")

	# find the subjects that you want to run
	# if a subject had multiple scans from a visit, it will repeat this subject name into the list
	all_first_dicom = glob.glob(os.path.join(dti_data, x + "/DTI/*/*/*_1_S*.dcm"))
	all_subjects = [x.split("/")[len(dti_data.split("/"))] for x in all_first_dicom]

	config.write("set subjlist = ( " +  " ".join(all_subjects) + " )\n\n")

	# find the DICOM files
	config.write("Input diffusion DICOMS\n")
	config.write("set dcmlist = (" + " ".join(all_first_dicom) + " )\n")

	# set parameters
	echospacing = round(1000* (1/ (check_if_metadata_present.scan_dict[x]["bandwidthperpixelphaseencode"][0] * 65)),2)
	epifactor = check_if_metadata_present.scan_dict[x]["epifactor"][0]
	
	config.write("set dob0 = 2\n")
	config.write("set echospacing = " + str(echospacing) + "\n")
	config.write("set pedir = ( RL LR )\n")
	config.write("set epifactor = " + str(epifactor) + "\n")
	config.write("set dTE = " + str(check_if_metadata_present.scan_dict[x]["TE"][0]) + "\n")
	config.write("set doeddy = 2\n")
	config.write("set dorotbvecs = 1\n")
	config.write("set intrareg = 3\n")
	config.write("set intradof = 9\n")
	config.write("set intrarot = 90\n")
	config.write("set interreg = 5\n")

	config.close()
