#!/usr/bin/env python

import glob
import os
import pandas as pd
import argparse as ap 

import f90nml 
from IPython import embed

# This script isn't general enough... Maybe I should make a new 
# script for making an AVAILABLE output file for the processed
# output?

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='''Find all available output 
                                files in a given top directory and write relative paths to file''')
    parser.add_argument('path', help='Path to top directory containing FLEXPART output', nargs='+')
    parser.add_argument('--outpath', '--op', help='path where file containting path info should be stored', 
                            default='')
    parser.add_argument('--no_readme', '--rd', 
            help='Atomatically create readme file, work only for default FLEXPART output folder', default='store_false')
    args = parser.parse_args()
    paths = args.path
    gen_readme = args.no_readme
    cwd = os.getcwd()
    for path in paths:
        try: 
            os.chdir(path)
        except FileNotFoundError:
            os.chdir(cwd + '/' + path)
        outfiles = glob.glob('**/output/*.nc', recursive=True)
        
        outpaths = ['/'.join(ncfile.split('/')[:-1]) for ncfile in outfiles]
        ncfiles = [ncfile.split('/')[-1] for ncfile in outfiles]
        ncfiles.sort()
        outpaths.sort()
        date_index = [pd.to_datetime(date.split('_')[-1].split('.')[0]) for date in ncfiles]
        df = pd.DataFrame(data={'dir_paths':outpaths,'ncfiles':ncfiles}, index=date_index)

        df.to_csv('AVAILABLE_OUTPUT', date_format='%Y%m%d-%H')

        files = os.listdir(outpaths[0])
        stime = date_index[0].strftime('%Y%d%m-%H')
        etime = date_index[-1].strftime('%Y%d%m-%H')
        if gen_readme:
            with open(outpaths[0] + '/header_txt') as headerfile:
                headerfile.readline()
                version = headerfile.readline().split('   ')[-1].strip()
                info = headerfile.readlines()
            files = os.listdir(outpaths[0])
            specfnames = glob.glob(outpaths[0]+'/SPECIES_*')
            specf = f90nml.read(specfnames[0])

            with open('README', 'w') as ofile:
                ofile.write("This Folder contains FLEXPART {} model output files {} - {} \n".format(version[2:],stime, etime))
                ofile.write("The FLEXPART setup files for each model run is available in /options/ \n")
                ofile.write("If output is from a backward FLEXPART simulation, (check ldirect='-1),' \n")
                ofile.write("output is stored in spec001_mr variable in the netcdf file, receptor points\n")
                ofile.write("are accessed through indexing the pointspec dimmension.\n")
                ofile.write("All available output files are listed in AVAIALBLE_OUTPUT.\n")
                if 'trajectories.txt' in files:
                    ofile.write("Centroid plume information is available in the trajectories.txt files in\n")
                    ofile.write("**/output/trajectories.txt\n")
                ofile.write('\n')
                ofile.write('# GENERAL information read from header_txt:\n')
                for line in info[:9]:
                    ofile.write(line)
                for line in info[11:]:
                    ofile.write(line)
                ofile.write('=========================================================================\n')
                ofile.write('                                 SPECIES-INFO\n')
                ofile.write('PCRAIN_AERO = {} below-cloud scavenging rain collection efficiency\n'.format(specf['species_params']['pcrain_aero']))
                ofile.write('PCSNOW_AERO = {} rain collection efficiency moderator for snow \n'.format(specf['species_params']['pcsnow_aero']))
                ofile.write('PCCN_AERO = {} cloud condensation nuclei efficiency\n'.format(specf['species_params']['pccn_aero']))
                ofile.write('PIN_AERO = {} in-cloud scavenging, ice nuclei efficiency\n'.format(specf['species_params']['pin_aero']))
                ofile.write('PDENSITY = {} particle density [kg/m^3]\n'.format(specf['species_params']['pdensity']))
                ofile.write('PSPECIES = {}\n'.format(''.join(specf['species_params']['pspecies'])))
                ofile.write('PDQUER = {} particle mean diameter [m] \n'.format(specf['species_params']['pdquer']))

        

        
        
        

