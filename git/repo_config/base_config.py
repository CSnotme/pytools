
import os


class RepoConfig(object):

    def __init__(self, git_pull: str, local_dir: str, checkout_branches: str, local_alias='', is_pull=True,
                 is_go_dep=False, is_php_dep=False):
        # 远程仓库的git拉取地址
        self.git_pull = git_pull
        # 要放置的本地目录
        self.local_dir = local_dir
        # 本地仓库别名
        self.local_alias = local_alias

        # 是否拉取
        self.is_pull = is_pull
        # 是否切分支
        self.checkout_branches = checkout_branches

        # 是否拉取go依赖
        self.is_go_dep = is_go_dep

        # 是否拉取php依赖
        self.is_php_dep = is_php_dep

    def set_git_pull(self, git_pull):
        self.git_pull = git_pull
        return self

    def to_array(self):
        cfg = [
            self.git_pull,
            self.local_dir,
            self.local_alias,
            self.is_pull,
            self.checkout_branches,
            self.is_go_dep,
            self.is_php_dep,
        ]

        return cfg

    def __parse_name(self):
        prefix, suffix = os.path.split(self.git_pull)
        return suffix.split('.')[0]


class CodeUpRepoConfig(RepoConfig):
    # 阿里云code域名
    host = "https://codeup.aliyun.com"

    # 仓库前缀
    prefix = {
        "xwx": "61e54b0e0bb300d827e1ae27",  # xwx仓库前缀
        "yk": "6528ab78940b4e1cb0ce7abb",  # yk仓库前缀
    }

    def __init__(self, remote_repo_path: str, local_dir: str, checkout_branches: str, local_alias='', is_pull=True,
                 is_go_dep=False, is_php_dep=False, use_prefix="xwx"):
        if use_prefix not in self.prefix.keys():
            raise Exception("请传入正确的仓库前缀")

        # 使用哪个仓库前缀
        self.use_prefix = use_prefix

        # 远程仓库的页面地址的path
        self.remote_repo_path = remote_repo_path

        git_pull = self.__gen_git_pull(remote_repo_path, use_prefix)

        super().__init__(git_pull, local_dir, local_alias, checkout_branches, is_pull, is_go_dep, is_php_dep)

    def switch_xwx(self):
        self.use_prefix = "wxw"
        return self.__switch_prefix(self.use_prefix)

    def switch_yk(self):
        self.use_prefix = "yk"
        return self.__switch_prefix(self.use_prefix)

    def get_codeup_urls(self):
        return "{}/{}{}".format(self.host, self.prefix[self.use_prefix], self.remote_repo_path)

    def __switch_prefix(self, prefix):
        return self.set_git_pull(self.__gen_git_pull(self.remote_repo_path, prefix))

    def __gen_git_pull(self, remote_repo_path, use_prefix):
        return "git@codeup.aliyun.com:{}{}.git".format(self.prefix[use_prefix], remote_repo_path)
