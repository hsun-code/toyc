import argparse
import os
import sys
import json
import subprocess

golden_data_filename = "golden.data.json"
ut_info = [
    ['token', '/tmp/toyc.lex'],
    ['ast', '/tmp/toyc.ast']
]


def check_result(output_filename, golden_checksum):
    with open(output_filename, 'r') as output_file:
        lines = output_file.readlines()
        first_line = lines[0]
        if first_line == golden_checksum:
            return True
        else:
            print('checksum: %s' % first_line)
            print('expected checksum: %s' % golden_checksum)
            return False


def do_test(toyc_file, chk_flag, work_dir, output_filename):
    # read golden data
    golden_data = {}
    with open(os.path.join(work_dir, golden_data_filename), 'r') as golden_file:
        golden_data = json.load(golden_file)
        golden_file.close()

    # for each C file in work_dir
    print("work dir is %s" % work_dir)
    for cfile in os.listdir(work_dir):
        cfile_path = os.path.join(work_dir, cfile)
        if os.path.isfile(cfile_path) and cfile[-2:] == '.c':
            print('test case: %s' % cfile)
            if cfile not in golden_data.keys():
                print('ERROR: not golden data.')
                sys.exit()

            # remove the old outout file if there is
            if os.path.exists(output_filename):
                os.remove(output_filename)

            # compile this file and new checksum would be written into output_file
            cmd_str = 'python3 ' + toyc_file + ' -i ' + \
                cfile_path + ' --opt --chk ' + chk_flag
            subprocess.call(cmd_str, shell=True)

            # compare the checksums
            if check_result(output_filename, golden_data[cfile]):
                print('pass.')
            else:
                print('fail')
                print('Please re-run the command to reproduced the error.')
                print('\t%s' % cmd_str)
                sys.exit()


def main():
    '''
    Command Option:
        python test.py [--src SRC_DIR]
        Input: the location of TOYC source code. [Optional. Default is PWD]
    '''
    arg_parser = argparse.ArgumentParser(
        description="Test framework for TOYC")
    arg_parser.add_argument('--src', default='.', dest='src_dir',
                            help='The location of TOYC source code. Default is $PWD')

    # get options
    args = arg_parser.parse_args()
    src_dir = args.src_dir

    # check whether the directory is accessable or not
    if not os.path.exists(src_dir):
        print("ERROR: Directory %s is not found." % src_dir)
        sys.exit()
    toyc_file = os.path.join(src_dir, 'toyc.py')

    # start the ut
    ut_dir = os.path.join(src_dir, 'test')
    print('Unit test dir is %s' % ut_dir)

    for inx in range(len(ut_info)):
        chk_flag = str(inx + 1)
        ut_type = ut_info[inx][0]
        output_filename = ut_info[inx][1]
        work_dir = os.path.join(ut_dir, ut_type)
        print('Testing %s' % ut_type)
        do_test(toyc_file, chk_flag, work_dir, output_filename)

    print('UT finished now.')


if __name__ == '__main__':
    main()
