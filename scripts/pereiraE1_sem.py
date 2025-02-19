import os
import glob
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import ipdb

import utils

EXPT_INFO_PATH = os.path.join(utils.EXPT_INFO_DIR, 'Args_PereiraE1.tsv')
EXPT_ID = 'PereiraE1_sem'
    

def main():
    all_func_paths = defaultdict(list)
    df = pd.read_csv(EXPT_INFO_PATH, sep='\t')
    for _, row in df.iterrows():
        uid = utils.proc_uid(row.UID)
        sid = row.Session
        run = row.Run
        subj_dir = utils.get_subj_dir(uid, sid)
        func_id = utils.get_func_id(uid, sid, run)
        func_dir = os.path.join(subj_dir, 'Parcellate', 'func')
        func_path = os.path.join(func_dir, f'sdwrfunc_run-{func_id}_bold.nii')
        assert os.path.exists(func_path), ipdb.set_trace()
        all_func_paths[uid].append(func_path)
    for uid in tqdm(all_func_paths.keys()):
        func_paths = all_func_paths[uid]
        utils.write_yaml(
            uid,
            func_paths,
            expt_id=EXPT_ID,)
        utils.write_slurm_job(
            uid,
            expt_id=EXPT_ID,)
        

if __name__ == '__main__':
    main()
