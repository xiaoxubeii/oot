#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth  --useshadow  --enablemd5
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Use text mode install
text
# Firewall configuration
firewall --disable
# Run the Setup Agent on first boot
firstboot --disable
# System keyboard
keyboard us
# System language
lang en_US
# Use network installation
url --url=$tree

# If any cobbler repo definitions were referenced in the kickstart profile, include them here.
$yum_repo_stanza
# Network information
$SNIPPET('network_config')
# Reboot after installation
reboot

#Root password
rootpw --iscrypted $default_password_crypted
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# System timezone
timezone  Asia/Shanghai
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr
# Allow anaconda to partition the system as needed
part /boot --fstype="xfs" --size=200 --asprimary
part / --fstype="xfs" --size=1024 --grow
part swap --fstype="swap" --size=1024

%pre
$SNIPPET('pre_install_network_config')
$SNIPPET('pre_anamon')
%end

%packages
@^graphical-server-environment
%end

%post
$yum_config_stanza
$SNIPPET('post_install_network_config')
$SNIPPET('post_anamon')
%end
