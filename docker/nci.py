#!/usr/bin/env python3

"""
what this module should do:
- convert .pdb to .xyz
- generate .nci files
- create .sub scripts

should we do something nice for organization -- ie put outputs in subdir?
"""


# reads a .pbd file to an IR which preserves only the coordinate section
# IR is an array with columns "type x y z" (ie. in .xyz order)
# TODO: more tolerant of differently structured pdb files
def read_pdb(pdb_file):
    lines = []

    for line in pdb_file:
        if line.strip() == 'TER':
            break
        if line.strip()[0] == '#':
            continue

        try:
            x_pos = float(line[30:38])
            y_pos = float(line[38:46])
            z_pos = float(line[46:54])
            spec = line[76:78].strip()

        except IndexError:
            # recover here?
            raise

        lines.append((spec, x_pos, y_pos, z_pos))

    return lines


# takes IR in form described for `read_pdb`
# TODO: fancy formating so the columns look nice
def write_xyz(structure, xyz_file, name=""):
    xyz_file.write(str(len(structure)))
    xyz_file.write("\n" + name + "\n")

    for atom in structure:
        line = atom[0] + " " + " ".join(map(str, atom[1:])) + '\n'
        xyz_file.write(line)


# TODO: inline this?
def pdb_to_xyz(pdb_name, xyz_name):
    with open(pdb_name, 'r') as pdb_file:
        struct = read_pdb(pdb_file)

    with open(xyz_name, 'w') as xyz_file:
        write_xyz(struct, xyz_file)


# TODO: expand with more options and/or a config file
def create_nci(nci_file, xyz_name):
    s = "1\n{}\nINCREMENTS 0.1 0.1 0.1\nOUTPUT -1\n".format(xyz_name)
    nci_file.write(s)


# TODO: more flexable creation needed
def create_sub(name, basenames, main_dir):
    import os
    # these should be setable
    opts = {'mail': "aschankler@haverford.edu", 'uname': "aaron"}

    run_cmd = "/data/aaron/nciplot.v1 {nci_file} {log_file}\n"
    fstring = "#PBS -N {name}\n#PBS -l nodes=1:ppn=1\n#PBS -j oe\n#PBS -V\n" \
              "#PBS -M {mail}\n#PBS -m abe\n#PBS -A {uname}\ncd {base_dir}\n" \
              "export NCIPLOT_HOME=/data/aaron/nciplot-data/\n" \
              "{run_cmds}"

    cmds = "".join([run_cmd.format(**{'nci_file': base + ".nci", 'log_file':
                    base + ".log"}) for base in basenames])

    opts.update({'name': name, 'run_cmds': cmds, 'base_dir': main_dir})
    sub_str = fstring.format(**opts)

    with open(os.path.join(main_dir, "input.sub"), 'w') as sub_file:
        sub_file.write(sub_str)


# creates a .xyz file and a .nci file in `where` directory
# creates a .sub script
def job_setup(pdb_list, where):
    import os
    basenames = []
    for pdb in pdb_list:
        basename = os.path.splitext(os.path.basename(pdb))[0]
        pdb_to_xyz(pdb, os.path.join(where, basename + ".xyz"))
        with open(os.path.join(where, basename + ".nci"), 'w') as nci_file:
            create_nci(nci_file, basename + ".xyz")

        basenames.append(basename)

#    create_sub("nci", basenames, where)


# TODO: better option handling
def main(args):
    import os

    if args[0] == '--create':

        where = os.path.abspath(args[1])
        try:
            pdb_dir = args[2]
        except IndexError:
            pdb_dir = os.getcwd()

        pdb_list = [os.path.join(pdb_dir, p) for p in os.listdir(pdb_dir)]
        pdb_list = filter(lambda p: os.path.isfile(p) and p.endswith('.pdb'), pdb_list)

        job_setup(pdb_list, where)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])

