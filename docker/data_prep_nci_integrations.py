#!/usr/bin/env python3

import pandas as pd
import numpy as np
import glob
import os.path
import argparse
import logging
import subprocess
    

def process_data(nci_path, output_path):
    pd.set_option('display.max_columns', 500)
    integrations = pd.DataFrame(columns = ['name']
                                + ['integration_' + s for s in map(str, range(1,101))] + ['total_integration'])
    logging.debug("Processing files")
    for n in glob.glob(os.path.join(nci_path, '*-integrated.dat')):
        logging.debug("Processing {}".format(n))
        basename = os.path.basename(n)
        vals = np.fromfile(n, dtype=float, sep=" ")
        vals = vals.tolist()
        vals = [basename.rstrip('-integrated.dat') + '.pdb'] + vals
        integrations.loc[len(integrations)] = vals

    logging.debug("Saving to csv")
    integrations.to_csv(output_path)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("nci_path", help="Path to directory with processed pdb data files",
                        type=str)
    parser.add_argument("output_path", help="File path were integrated csv will be written",
                        type=str)

    args = parser.parse_args()

    if not os.path.isdir(args.nci_path):
        logging.error("Given nci_path is not a directory: {}".format(args.nci_path))
        exit(1)

    output_directory = os.path.dirname(args.output_path)
    if len(output_directory) > 0 and not os.path.isdir(output_directory):
        logging.error("Directory for given output_path does not exist: {}".format(args.output_path))
        exit(1)
    
    process_data(args.nci_path, args.output_path)
    
