import os
import ipdb

import utils


def main():
    parser = utils.get_parser()
    args = parser.parse_args()
    
    job_dir = os.path.join(utils.PBS_DIR, args.expt_id)
    assert os.path.isdir(job_dir)
    cmds = []
    for path in os.listdir(job_dir):
        cmd = f'sbatch {job_dir}/{path}'
        cmds.append(cmd)
    for cmd in cmds:
        os.system(cmd)
    

if __name__ == '__main__':
    main()

