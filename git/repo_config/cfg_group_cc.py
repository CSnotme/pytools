from git.repo_config.base_config import CodeUpRepoConfig

# 拉取到本地目录
__DEFAULT_LOCAL_DIR = "/Users/caoyongfei/workspace/go/src/projects/xwx/test"

# cc配置中心，一共5个仓库
GROUP_CONFIG_CC = [
    CodeUpRepoConfig("xxx",  __DEFAULT_LOCAL_DIR, 'master'),
]
