import os
import shutil

input_dir = './3-The_Curated_SRS_Dataset'
output_file = 'merged_output.txt'


with open(output_file, 'w') as outfile:
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'): 
            with open(os.path.join(input_dir, filename)) as infile:
                               
                # Get the file name without extension
                name = os.path.splitext(filename)[0]
                
                # Split on '-' and get the first part
                name_prefix = name.split('-')[0]
            
                # Read the file content and split into lines
                content = infile.read()
                lines = content.split("\n")
                
                # Filter out any empty lines
                cleaned_lines = [line for line in lines if line.strip() != ""]


                outfile.write("CASE: " + name_prefix + "\n\n")
                outfile.write("\n".join(cleaned_lines)+ "\n")
                outfile.write('\n=================================================================\n')

print('Files merged successfully!')
