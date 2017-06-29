git本质是一个分布式的版本库

# 对象库：内容寻址系统

`git ls-files`列出文件

`git ls-files -s`列出暂存区(stage area)中的文件对象

`git cat-file`查看文件

`git cat-file -p`美观排版显示文件内容

`git hash-object`计算文件的hash码

`git write-tree`根据当前索引中的内容创建树对象

# git文件管理

## Git中的文件分类，分为3类：

```
已追踪的（tracked）：已经在版本库中，或者已经使用git add命令添加至索引中的文件
被忽略的（Igored）：在版本库中通过“忽略文件列表”明确声明为被忽略的文件
未追踪的（untracked）：上述两类之外的其它文件
```

## 增

`git add`暂存文件

## 查

`git ls-files`默认显示索引中的文件列表的原始文件名

`git ls-files -s`显示暂存的文件信息：权限、对象名、暂存号及原始文件名

`git ls-files -o`显示未被追踪的文件

## 删

`git rm`删除工作目录中的文件，及索引中的映射；当文件和映射文件不同时不允许删除，需要`git add FILENAME`同步更改情况

`git rm --cached`只删除索引中的映射；

## 改

`git mv`改变工作目录中的文件名，及索引中的映射；


# Git提交：

`git commit`提交

`git log`查看提交日志

## 提交的标识

引用：ID， reference, SHA1, 绝对提交名；

符号引用：symbolic reference, symref；

本地特性分支名称、远程跟踪分支名称、标签名；

名称：

refs/heads/REF：本地特性分支名称

refs/remotes/REF：远程跟踪分支名称

refs/tags/REF：标签名

Git会自动维护几个特定目的的特殊符号引用：

HEAD：始终指向当前分支的最近提交；或检出到其它分支时，目标分支的最近提交；

ORIG_HEAD：合并操作时，新生成的提交之前的提交保存于此引用中；

FETCHED_HEAD:

MERGE_HEAD：合并操作时，其它分支的上一次提交；

相对提交名：
^：C6^, C6^2
~：C6~, C6~2

`git diff`比较提交、索引及工作目录；

--color：

`git reset`撤消此前的操作；

--soft：将HEAD引用指向给定的提交，但不影响索引和工作目录；

--mixed：将HEAD引用指向给定的提交，并将索引内容改变为指定提交的快照；但不改变工作目录；

--hard：将HEAD引用指向给定的提交、将索引内容改变为指定提交的快照，并改变工作目录中的内容反映指定提交的内容；


# Git分支:

分支命名法则：

```
可以使用/，但不能以/结尾；
不能以-开头；
以位于/后面的组件，不能以.开头；
不能使用连续的...；
不能使用空白字符；
不能使用^, ~, ?, *，[等；
```

必须惟一；分支名字的名字始终指向目标分支的最近一次提交；

`git branch`列出、创建及删除分支；

git branch BRANCH_NAME [START_COMMIT]

git branch -d BRANCH_NAME

`git branch -a`列出所有分支，包括远程分支

`git show-branch`查看分支及其相关的提交；

`git checkout`

`git checkout <branch>`拣出分支；

`git checkout -b python_mail.skin origin/python_mail.skin`拣出远程分支

## 分支合并

合并基础：要合并的分支的最近一次的共同提交；

我们的版本：当前分支的最近一次提交；

他们的版本：要合并进来的分支的最近一次提交；

### 无冲突合并：

```
$ git checkout master
$ git status
$ git merge BRANCH_NAME
$  git log --graph --pretty=oneline --abbrev-commit
```

### 有冲突合并：

手动解决冲突,解决完成之后：

```
git add  
git commit
```

### 变基操作

git rebase

```
$ git checkout dev
$ git rebase master
$ git checkout master
$ git merge -m "MSG"
```


# Git：分布式版本控制系统；

基于网络协议：http, https, ssh, git

## 克隆操作：
`git clone`

git clone默认会把远程仓库整个给clone下来;

但只会在本地默认创建一个master分支

如果远程还有其他的分支，此时用`git branch -a`查看所有分支

## Git通信协议

协议：本地协议（local）、HTTP/HTTPS协议、SSH协议、Git协议；

### 本地协议：

URL：

/path/to/repo.git

file:///path/to/repo.git

### Git协议
由git-daemon程序提供，监听在tcp的9418端口；仅支持“读”操作，无任何认证功能；

URL：

git://host/path/to/repo.git

git://host/~user/path/to/repo.git

### SSH协议
URL

ssh://[USER@]host[:port]/path/to/repo.git

ssh://[USER@]host[:port]/~USERNAME/path/to/repo.git

URL2

[USER@]hostpath/to/repo.git

### HTTP/HTTPS协议

1.6.5-：哑http协议

1.6.6+：智能http协议

读/写/认证

URL：

http://host/path/to/repo.git

`git fetch`取回远程服务器的更新；

`git pull`取回远程服务器更新，而后与本地的指定分支合并；

git pull <远程主机名> <远程分支名>:<本地分支名>

`git push`将本地的更新推送到远程主机；

git push  <远程主机名>  <本地分支名>:<远程分支名>

# 服务器

git-daemon：
	git://

```
<VirtualHost *:80>
	ServerName git.magedu.com
	SetEnv GIT_PROJECT_ROOT /var/www/git
	SetEnv GIT_HTTP_EXPORT_ALL
	ScriptAlias /git/ /usr/libexec/git-core/git-http-backend/
	<Directory "/usr/libexec/git-core/">
		Options ExecCGI Indexes
		Require all granted
	</Directory>
	<LocationMatch "^/git/.*/git-receive-pack$">
		AuthType Basic
		AuthName "Private Git Repo"
		AuthUserFile /etc/httpd/conf/.htpasswd
		Require valid-user
	</LocationMatch>
</VirtualHost>
```

man git-http-backend
