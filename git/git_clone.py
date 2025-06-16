import os
import subprocess


# 是否有git命令
def is_has_git():
    ret = os.popen('git --version')
    output = ret.read()
    if "git version" in output:
        return True
    return False


# clone 项目
def clone_app(root_dir, git_url, app_name=None):
    print("[开始] git clone项目 {} 至 {}".format(git_url, root_dir))
    if not os.path.exists(root_dir):
        print("root路径:{}不存在".format(root_dir))
        return
    if app_name:
        shell = "cd {} && git clone {} {}".format(root_dir, git_url, app_name)
    else:
        shell = "cd {} && git clone {}".format(root_dir, git_url)
    ret = os.popen(shell)
    if not ret.readlines():
        print("[完成] git clone项目 {} 至 {}".format(git_url, root_dir))
    else:
        print("[异常] git clone项目 {} 至 {}".format(git_url, root_dir))


"""
aly-codeup-http地址替换为git地址
"https://codeup.aliyun.com/6528ab78940b4e1cb0ce7abb/xxx/aaa" => "git@codeup.aliyun.com:6528ab78940b4e1cb0ce7abb/xxx/aaa.git"
"""
def transfer_to_git_path(codeup_url):
    git_url = codeup_url.replace("https://codeup.aliyun.com/", "git@codeup.aliyun.com:", 1) + ".git"
    return git_url


# 进入某目录，本地创建线上同名分支并关联线上分支
def checkout_branch(dir_path, branch_name):
    if not os.path.exists(dir_path):
        print("项目目录:{}不存在".format(dir_path))
        return

    if not os.path.isabs(dir_path):
        print("项目目录:{}非绝对路径， 请传入绝对路径".format(dir_path))
        return

    create_branch_shell = "cd {}; git checkout -b {} origin/{}".format(dir_path, branch_name, branch_name)
    checkout_branch_shell = "cd {}; git checkout {}".format(dir_path, branch_name)

    # 进入目录并执行创建分支关联远程分支
    process1 = subprocess.Popen(create_branch_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout1, stderr1 = process1.communicate()
    if process1.returncode != 0:
        ret = stderr1.decode()
        if "'{}' already exists".format(branch_name) in ret:
            process2 = subprocess.Popen(checkout_branch_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout2, stderr2 = process2.communicate()
            if process2.returncode != 0:
                print("异常!!! 项目:{}, 切换分支:{}, 异常:{}".format(dir_path, branch_name, ret))
            else:
                print("项目:{}, 切换分支:{}, [完成]".format(dir_path, branch_name))
        else:
            print("异常!!! 项目:{}, 切换分支:{}, 异常:{}".format(dir_path, branch_name, ret))
    else:
        print("项目:{}, 切换分支:{}, [完成]".format(dir_path, branch_name))

# 客服-项目-clone
def customer_service_app_clone():
    dir_path = "/Users/caoyongfei/workspace/go/src/customer_service"
    codeup_urls = []

    for url_info in codeup_urls:
        git_url = transfer_to_git_path(url_info[0])
        if url_info[1]:
            clone_app(dir_path, git_url, url_info[1])
        else:
            clone_app(dir_path, git_url)


if __name__ == '__main__':
    # is_has_git()
    # transfer_to_git_path('')

    # yk_anchor_app_clone()
    customer_service_app_clone()
    # xwx_deployment_ls_app_clone()

    # dir_name = "/Users/caoyongfei/workspace/go/src/deployment_ls"
    # branch_name = "release"
    # app_list = os.listdir(dir_name)
    # for app_name in app_list:
    #     app_dir_path = os.path.join(dir_name, app_name)
    #     checkout_branch(app_dir_path, branch_name)
