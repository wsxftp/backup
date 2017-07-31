# yum源配置
devcdrom=`grep '/dev/cdrom /media/cdrom iso9660 defaults 0 0' /etc/fstab`
[ -z $devcdrom ] && echo '/dev/cdrom /media/cdrom iso9660 defaults 0 0' >> /etc/fstab
sed -i s/enabled=0/enabled=1/ /etc/yum.repos.d/CentOS-Media.repo
cat > /etc/yum.repos.d/epel.repo <<EOF


# 命令行补全，安装git，安装nfs挂载支持，安装iftop，用于网络监控，用于传输文件，x11转发支持
yum -y install bash-completion git nfs-utils iftop vim lrzsz xorg-x11-xauth
# 安装编译环境
yum groupinstall "Development Tools" "Server Platform Deveopment" -y

# 停止防火墙，关闭selinux
systemctl stop firewalld.service
sed -i s/SELINUX=enforcing/SELINUX=disabled/ /etc/selinux/config
```
