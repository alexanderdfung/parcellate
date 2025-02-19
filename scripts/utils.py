import os
import argparse


ROOT_DIR = '/om2/user/alexfung/repos/parcellate'
EXPT_INFO_DIR = os.path.join(ROOT_DIR, 'expt_info')
CFG_DIR = os.path.join(ROOT_DIR, 'cfg')
PBS_DIR = os.path.join(ROOT_DIR, 'pbs')

SUBJ_DIR = '/mindhive/evlab/u/Shared/SUBJECTS'
PARC_DIR = '/nese/mit/group/evlab/u/alexfung/parcellate'

SAMPLE_ARGS = dict(
    n_samples=256,
    high_pass=0.01,
    low_pass=0.1,
)
ALIGN_ARGS = dict(
    n_alignments=512,
)
LABEL_ARGS = dict(
    reference_atlases='LANG',
)

SEP = '  '
   

def get_parser():
    parser = argparse.ArgumentParser(
            description='Parcellation with functional correlation')
    parser.add_argument(
            '--expt_id', default='PereiraE1_sem', type=str, action='store')
    parser.add_argument(
            '--overwrite', default=False, action='store_true')
    parser.add_argument(
            '--verbose', default=False, action='store_true')
    return parser


def proc_uid(uid):
    if type(uid) == int:
        uid = str(uid)
    assert type(uid) == str
    uid = uid.zfill(3)
    return uid


def get_subj_dir(uid, sid):
    uid = proc_uid(uid)
    return os.path.join(SUBJ_DIR, f'{uid}_{sid}_PL2017')


def get_func_id(uid, sid, run):
    subj_dir = get_subj_dir(uid, sid)
    cfg_path = os.path.join(subj_dir, 'data.cfg')
    with open(cfg_path, 'r') as f:
        cmps = f.read()
    func_idx = cmps.index('#functionals')
    cmps = cmps[func_idx+1:]
    if '#' in ''.join(cmps):
        struct_idx = cmps.index('#')
    func_runs = cmps[:struct_idx].split()
    run = str(run)
    assert run in func_runs
    func_id = str(func_runs.index(run)).zfill(2)
    return func_id


def write_yaml(
        uid,
        func_paths,
        expt_id,
        sample_id='main',
        sample_args=SAMPLE_ARGS,
        align_args=ALIGN_ARGS,
        label_args=LABEL_ARGS,):
    parc_dir = os.path.join(PARC_DIR, uid)
    lines = [
        'sample:',
        f'{SEP}{sample_id}:',
        f'{SEP}{SEP}functional_paths:',
    ] + [f'{SEP}{SEP}{SEP}- {func_path}' for func_path in func_paths] + \
        [f'{SEP}{SEP}{key}: {sample_args[key]}' for key in sample_args.keys()] + [
        'align:',
        f'{SEP}{sample_id}:',
    ] + [f'{SEP}{SEP}{key}: {align_args[key]}' for key in align_args.keys()] + [
        'label:',
        f'{SEP}{sample_id}:',
    ] + [f'{SEP}{SEP}{key}: {label_args[key]}' for key in label_args.keys()] + [
        f'output_dir: {parc_dir}'
    ]
    text = '\n'.join(lines)
    yml_dir = os.path.join(CFG_DIR, expt_id)
    if not os.path.isdir(yml_dir):
        os.makedirs(yml_dir)
    yml_path = os.path.join(yml_dir, f'{uid}.yml')
    with open(yml_path, 'w') as f:
        f.write(text)
        f.close()
        

def write_slurm_job(
        uid,
        expt_id,):
    cmd = f'python -m parcellate.bin.make_jobs {CFG_DIR}/{expt_id}/{uid}.yml ' + \
        f'-t 8 -m 32 -n 1 -e node067,node093 -s {PARC_DIR} --outdir {PBS_DIR}/{expt_id}'
    os.system(cmd)
    