from git.repo_config.base_config import CodeUpRepoConfig

# 拉取到本地目录
__DEFAULT_LOCAL_DIR = "/Users/caoyongfei/workspace/go/src/projects/xwx/test"

# cc配置中心，一共5个仓库
GROUP_CONFIG_CC = [
    CodeUpRepoConfig("/xue/bigclass_jichujiagou_common/config-sdk-go",  __DEFAULT_LOCAL_DIR, 'xwx_syh'),
    CodeUpRepoConfig("/xue/bigclass_jichujiagou_common/config-sdk",     __DEFAULT_LOCAL_DIR, 'xwx_syh'),
    CodeUpRepoConfig("/xue/bigclass_jichujiagou_common/configure-web",  __DEFAULT_LOCAL_DIR, 'xwx_syh'),
    CodeUpRepoConfig("/xue/bigclass_jichujiagou_common/configureadmin", __DEFAULT_LOCAL_DIR, 'xwx_syh'),
    CodeUpRepoConfig("/xue/bigclass_jichujiagou_common/config-server",  __DEFAULT_LOCAL_DIR, 'xwx_syh'),
]
