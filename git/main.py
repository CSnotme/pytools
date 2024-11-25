from git.repo_config.cfg_group_cc import *
from repo import *


def run(cfg):
    r = Repo.init_by_codeup_repo_config(cfg)
    if cfg.is_pull:
        r.pull()
    if cfg.is_php_dep:
        r.run_composer_update()
    if cfg.is_go_dep:
        r.run_go_mod()


def xwx_cc():
    for cfg in GROUP_CONFIG_CC:
        cfg.switch_xwx()
        run(cfg)




def main():
    xwx_cc()





if __name__ == '__main__':
    pass