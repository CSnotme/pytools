import pty
import subprocess
import os
import fcntl
import time
from collections import MutableMapping
from git.repo_config.base_config import CodeUpRepoConfig


class Repo(object):
    go_root = "/usr/local/go1.21"
    go_path = "/Users/caoyongfei/workspace/go"

    php_root = "/opt/homebrew/opt/php@7.4"
    composer_bin = "/usr/local/bin"

    def __init__(self, local_dir, pull_git, name="", clone_alias=""):
        # 拉取地址
        self.pull_git = pull_git

        # 本地目录
        self.local_dir = local_dir

        # clone的仓库别名
        self.alias = clone_alias

        self.name = self.__parse_name() if not name else name

        self.dest_path = os.path.join(self.local_dir, self.alias if self.alias else self.name)

    @classmethod
    def set_go_env_path(cls, go_root, go_path):
        cls.go_root = go_root
        cls.go_path = go_path
        return cls

    @classmethod
    def set_php_env_path(cls, php_root, composer_bin):
        cls.php_root = php_root
        cls.composer_bin = composer_bin
        return cls

    def pull(self):
        print("\r拉取仓库:[{}]".format(self.name), end='')

        if not os.path.isdir(self.local_dir):
            print("\r拉取仓库:[{}]失败， 目录不存在:{}".format(self.name, self.local_dir))
            return

        if os.path.exists(self.dest_path) and os.path.isdir(self.dest_path):
            print("\r拉取仓库:[{}], 目录已存在:{}".format(self.name, self.dest_path))
            return

        cmd = ['git', 'clone', self.pull_git]
        if self.alias:
            cmd = ['git', 'clone', self.pull_git, self.alias]

        try:
            for msg in self.__run_cmd_generator(cmd, self.local_dir):
                print("\r拉取仓库:[{}],进度:{}".format(self.name, msg.strip()), end='')
        except Exception as e:
            print("\r拉取仓库:[{}]失败， 错误:{}".format(self.name, e))

        print("\r拉取仓库:[{}]成功， 位置:{}".format(self.name, self.dest_path))

    def checkout(self, branch_name):
        cmd = "cd {} && git fetch && git checkout -b {} origin/{}".format(self.dest_path, branch_name, branch_name)
        ok, output = self.__run_shell(cmd)
        if ok:
            print("仓库:[{}], 切换分支为:[{}]".format(self.name, branch_name))
            return

        if "'{}' already exists".format(branch_name) not in output:
            print("仓库:[{}], 切换分支失败:[{}], 原因:{}".format(self.name, branch_name, output))
            return

        cmd = "cd {} && git checkout {}".format(self.dest_path, branch_name)
        ok, output = self.__run_shell(cmd)
        if ok:
            print("仓库:[{}], 切换分支为:[{}]".format(self.name, branch_name))
            return
        print("仓库:[{}], 切换分支失败:[{}], 原因:{}".format(self.name, branch_name, output))

    def run_composer_update(self):
        if not self.composer_bin:
            print("仓库:[{}], php composer 拉取依赖异常，请设置composer的bin目录！！！".format(self.name))
            return

        print("\r仓库:[{}], php composer 拉取依赖中".format(self.name), end='')

        # 需要设置一下php的环境变量
        env = os.environ.copy()
        env['PATH'] = f"{self.php_root}/bin:{env['PATH']}"
        env['PATH'] = f"{self.php_root}/sbin:{env['PATH']}"
        env['PATH'] = f"{self.composer_bin}:{env['PATH']}"

        cmd = ['composer', 'update', '-vvv']
        try:
            for msg in self.__run_cmd_generator(cmd, self.dest_path, env=env):
                print("\r仓库:[{}], php composer 拉取依赖中, 进度:{}".format(self.name, msg), end='')
        except Exception as e:
            print("\r仓库:[{}], php composer 拉取依赖失败， 错误:{}".format(self.name, e))

    def run_go_mod(self):
        if not self.go_root and not self.go_path:
            print("仓库:[{}], go mod 拉取依赖异常，请设置go_root和go_path ！！！".format(self.name))
            return

        print("\r仓库:[{}], go mod 拉取依赖中".format(self.name), end='')

        # 需要设置一下go的环境变量
        env = os.environ.copy()
        env['PATH'] = f"{self.go_root}/bin:{env['PATH']}"
        env['GOPATH'] = self.go_path

        cmd = ['go', 'mod', 'tidy']
        try:
            for msg in self.__run_cmd_generator(cmd, self.dest_path, env=env):
                print("\r仓库:[{}], go mod 拉取依赖中, 进度:{}".format(self.name, msg), end='')
        except Exception as e:
            print("\r仓库:[{}], go mod 拉取依赖失败， 错误:{}".format(self.name, e))

    def __parse_name(self):
        prefix, suffix = os.path.split(self.pull_git)
        return suffix.split('.')[0]

    # 是否有git命令
    def __has_git(self):
        cmd = "git --version"
        ok, output = self.__run_shell(cmd)

        return ok and "git version" in output

    @classmethod
    def init_by_codeup_repo_config(cls, config:CodeUpRepoConfig):
        return cls(config.local_dir, config.git_pull, config.local_alias)

    @staticmethod
    def __run_cmd_generator(cmd, work_dir, timeout=None, env=None):
        # 设置环境变量
        if env is None or not isinstance(env, MutableMapping):
            env = os.environ.copy()

        # 创建伪终端
        master, slave = pty.openpty()
        # 设置文件描述符为非阻塞
        fcntl.fcntl(slave, fcntl.F_SETFL, os.O_NONBLOCK)

        # 执行命令
        pcs = subprocess.Popen(cmd, stdout=slave, stderr=slave, text=True, cwd=work_dir, env=env)
        # 关闭从终端到子进程的写入通道，防止子进程无限等待输入
        os.close(slave)

        start_time = time.time()
        try:
            # 打开master描述符，读取输出
            output = os.fdopen(master)
            # 循环检查子进程是否执行完成
            while pcs.poll() is None:
                if timeout is not None and (time.time() - start_time) > timeout:
                    pcs.kill()
                    raise TimeoutError

                line = output.readline()
                yield line
        except KeyboardInterrupt:
            pcs.kill()

    @staticmethod
    def __run_shell(shell_cmd, timeout=None, res_check=0, executable="/bin/bash", env=None):
        # 设置环境变量
        if env is None or not isinstance(env, MutableMapping):
            env = os.environ.copy()

        pcs = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable=executable, env=env)

        if isinstance(timeout, int) and timeout > 0:
            stdout, stderr = pcs.communicate(timeout=timeout)
        else:
            stdout, stderr = pcs.communicate()

        if pcs.returncode == res_check:
            return True, stdout
        else:
            return False, stderr


if __name__ == '__main__':
    # go 环境
    go_root = "/usr/local/go1.21"
    go_path = "/Users/caoyongfei/workspace/go"

    # php 环境
    php_root = "/opt/homebrew/opt/php@7.4"
    composer_bin = "/usr/local/bin"

    Repo.set_go_env_path(go_root, go_path).set_php_env_path(php_root, composer_bin)

    # 仓库本地目录
    localDir = "/Users/caoyongfei/workspace/go/src/projects/xwx"
    # 仓库的git clone 的地址
    pullGit = "git@codeup.aliyun.com:61e54b0e0bb300d827e1ae27/backend/scm/deployment_ls/ls-svc.git"
    # pullGit = "git@codeup.aliyun.com:61e54b0e0bb300d827e1ae27/backend/scm/deployment_ls/translate.git"

    r = Repo(localDir, pullGit)

    r.pull()                 # 拉取
    r.checkout("release")    # 切分支
    # r.run_go_mod()           # go拉依赖
    # r.run_composer_update()  # php拉依赖
