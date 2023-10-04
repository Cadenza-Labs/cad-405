import re
from pathlib import Path      
  
def get_all_sweep_paths(output_filepath: str):
    paths = []
    # Open the file and read each line
    with open(output_filepath, 'r') as file:
        for line in file:
            # Use Regex to find the path
            match = re.search(r'Saving results to (.*$)', line)
            if match is not None:
                # if a match is found, convert the path string to pathlib object and add to list
                paths.append(Path(match.group(1)))

    # Return the list of all paths found.
    return paths
