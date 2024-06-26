# TRACULA Tutorial Alhusaini Lab
This is a tutorial to running TRACULA to process white matter tract data using DTI images. We will be using OSCAR clusters.

## Getting started
First, download the example data that we will be using here: https://drive.google.com/drive/folders/1nPOkant5Vr7Kmf_4V3p1ebO-uE7nHNl1?usp=sharing

You want to SSH into your cluster. You can do it through the GUI (https://ood.ccv.brown.edu/pun/sys/dashboard) or through your terminal. I recommend using the terminal as it is less glitchy and easier to copy and paste functions.

To SSH, please use the following instructions: https://docs.ccv.brown.edu/oscar/connecting-to-oscar/ssh

As an example using my login:
```
ssh -X dkim39@ssh.ccv.brown.edu
```
This will prompt a password:
```
(dkim39@ssh.ccv.brown.edu) Password: *******
```
We are now connected to the OSCAR clusters via SSH. 

## Loading the Dependencies
Type in the following:
```
module load freesurfer
module load fsl
module load ants
```

Second, we define where our data is stored:
```
export SUBJECTS_DIR=/users/dkim39/data/dkim39/maddata/PD/data/reconall_output
```
Freesurfer will use the variable name SUBJECTS_DIR to see where the preprocessed data from recon_all is. In this example, it will be the file path to the /data/reconall_output.

Next, we initialize FreeSurfer and set a pointer to the appropriate subjects directory, perform the following steps:
1. type "csh" into the terminal and press enter
2. type
```
source $FREESURFER_HOME/SetUpFreeSurfer.csh
```
3. This activated the Freesurfer application. We can exit csh but pressing CTL+D

## Creating the Config File
Open the check_if_metadata_present.py file in ./create_config.

Change the data_dir variable to where the DTI images are in line 5.
```
data_dir = "/users/dkim39/data/dkim39/maddata/PD/data/DTI"
```
Include the scans that you want to process. In this example, we are processing patients 3102 and 3105.
```
scans_to_look_at = ['3102', '3105']
```
This script goes through all of the listed patients and checks if the needed metadata, such as epifactor, mandwidth, rows, and columns, are present.

The script the you will be actually be running is ./make_TRACULA_config_multiple_DTI.py. This script calls the ./check_if_metadata_present.py file. Change the subjects_dir, dtroot, and dti_data file paths as appropriate. This script collects all of the metadata in how the DTI images were acquired and writes them into a config file, which TRACULA will use. For information on how to create this config script manually, visit https://surfer.nmr.mgh.harvard.edu/fswiki/dmrirc. This script just automates this process. While there is a way to have one config file for many patients, I prefer having one config file per patient to accomodate the different acquisition parameters, as usually the data is coming from multiple sources. Doing each of these manually will be tedious.

In our example, we are using the PPMI dataset. For information on how this data was acquired, reference the ./PPMI_manual.pdf.

Now we run the ./create_config/make_TRACULA_config_multiple_DTI.py file and the config files will be present in ./creaet_config/config_files.
```
python3 make_TRACULA_config_multiple_DTI.py
```

## Running TRACULA
Go to the folder where the config file is
```
cd ./create_config/config_files
```

You can now use this config file to run TRACULA scripts. There are three steps -prep, -bedp, and -path. For more information on each of these steps, visit https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Tracula. Technically, you can just run
```
trac-all -prep -c name_of_your_config_file
trac-all -bedp -c name_of_your_config_file
trac-all -path -c name_of_your_config_file
```
However, this will be very slow. Even when optimized, all of the scripts together will take at leasat 48 hours. Therefore, we want to run a batch script to use optimal resources and to also process multiple patients at the same time or in parallel.

```
sbatch -n 1 -t 36:00:00 --mem=4G -o slurm-identifier_ -%j.out insert_command_here
```
This runs your command with 1 core, for a maximum of 36 hours, with 4G of RAM, and sends any error logs to your slurm-identifier.out. You can have a maximum of 32 cores used, so technically 32 images being processed at the same time. The %j will be a random identifier assigned to the job. 

As an example:
```
sbatch -n 1 -t 36:00:00 --mem=4G -o slurm-3102-%j.out trac-all -prep -c tracula_3102.config
```

When you go to your reconall_output data folder, you will know your scripts are working when you see dlabel, dmri, dpath folders. Furthermore, when you run a batch script, the output of the job is written to the slurm-identifier-%j.out, and there should be no errors written here.