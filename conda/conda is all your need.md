# conda is all your need

# conda常用操作

## 获取版本 conda --version or -V
    conda update conda

## 查看当前存在哪些虚拟环境
    conda env list 或 conda info -e

## 查看--安装--更新--删除包
    conda list：
    conda search package_name# 查询包
    conda install package_name
    conda install package_name=1.5.0
    conda update package_name
    conda remove package_name


# 虚拟环境
## 创建名为your_env_name的环境
    conda create --name your_env_name
## 创建制定python版本的环境
    conda create --name your_env_name python=2.7
    conda create --name your_env_name python=3.6
## 创建包含某些包（如numpy，scipy）的环境
    conda create --name your_env_name numpy scipy
## 创建指定python版本下包含某些包的环境
    conda create --name your_env_name python=3.6 numpy scipy


# 激活环境

## Linux
    source activate your_env_name

## Windows
    activate your_env_name

# 删除
    conda remove -n your_env_name --all

    conda remove --name your_env_name --all


# 复制某个环境
    conda create --name new_env_name --clone old_env_name


# 在指定环境中管理包
    conda list -n your_env_name
    conda install --name myenv package_name 
    conda remove --name myenv package_name