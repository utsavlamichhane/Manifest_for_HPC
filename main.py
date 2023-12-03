
#dependencies for the script
import pandas as pd
import os

#a premanifest file is required

""" Constructing the Preliminary Manifestation Record: Initiate the generation of the pre_manifest by meticulously enumerating the filenames, inclusive of their respective extensions, as individual entries within the rows of a newly formulated spreadsheet. """

# Read the Excel file without header- as the pre_manifest is without header
df = pd.read_excel('pre_manifest.xlsx', header=None)

# the file path is for the file in my mac, change it based on the location of the sequence file
base_path = "/utsav_mac/Desktop/Buccal_microbiome/rumen_and_fecal/Rumen/FASTQ_RumenBuccalOverlap"

# Create a dictionary to hold the data
manifest_data = {
    "sample-id": [],
    "forward-absolute-filepath": [],
    "reverse-absolute-filepath": []
}

# Iterate through the rows in the dataframe
for index, row in df.iterrows():
    filename = row[0]
    parts = filename.split('_')
    sample_id = parts[0] + '_' + parts[1]  #NOTE: my code assumes the file with FASTQ title followed by _ and 

    # Determine the type (forward or reverse) based on R1 or R2 in the filename
    if '_R1_' in filename:
        manifest_data["sample-id"].append(sample_id)
        manifest_data["forward-absolute-filepath"].append(os.path.join(base_path, filename))
        manifest_data["reverse-absolute-filepath"].append('')  # Empty string for reverse paths
    elif '_R2_' in filename:
        # Finding the corresponding forward entry and append the reverse file path
        for i, sid in enumerate(manifest_data["sample-id"]):
            if sid == sample_id:
                manifest_data["reverse-absolute-filepath"][i] = os.path.join(base_path, filename)
                break

# Create a new DataFrame with the manifest data
manifest_df = pd.DataFrame(manifest_data)

# Write the new DataFrame to an Excel file with headers
manifest_df.to_excel('manifest.xlsx', index=False)

print('Manifest file has been created.')
