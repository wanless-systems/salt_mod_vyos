#!/bin/bash
# Obtain session environment
session_env=$(cli-shell-api getSessionEnv $PPID)


# Evaluate environment string
eval $session_env

# Setup the session
cli-shell-api setupSession

export vyos_libexec_dir=/usr/libexec/vyos
export vyos_cfg_templates=/opt/vyatta/share/vyatta-cfg/templates
export vyatta_htmldir=/opt/vyatta/share/html
export vyatta_datadir=/opt/vyatta/share
export vyos_libdir=/opt/vyatta/lib
export vyatta_op_templates=/opt/vyatta/share/vyatta-op/templates
export vyos_op_scripts_dir=/usr/libexec/vyos/op_mode
export vyos_prefix=/opt/vyatta
export vyos_datarootdir=/opt/vyatta/share
export vyatta_sysconfdir=/opt/vyatta/etc
export vyos_configdir=/opt/vyatta/config
export vyatta_sharedstatedir=/opt/vyatta/com
export vyos_validators_dir=/usr/libexec/vyos/validators
export vyos_completion_dir=/usr/libexec/vyos/completion
export vyatta_cfg_templates=/opt/vyatta/share/vyatta-cfg/templates
export VYATTA_CFG_GROUP_NAME=vyattacfg
export vyos_datadir=/opt/vyatta/share
export vyos_conf_scripts_dir=/usr/libexec/vyos/conf_mode
export vyatta_bindir=/opt/vyatta/bin
export VYATTA_USER_LEVEL_DIR=/opt/vyatta/etc/shell/level/admin
export vyos_sbin_dir=/usr/sbin
export vyatta_libdir=/opt/vyatta/lib
export vyos_op_templates=/opt/vyatta/share/vyatta-op/templates
export vyatta_localstatedir=/opt/vyatta/var
export VTYSH_PAGER=/bin/cat
export vyos_bin_dir=/usr/bin
export vyatta_libexecdir=/opt/vyatta/libexec
export vyatta_prefix=/opt/vyatta
export vyatta_datarootdir=/opt/vyatta/share
export vyatta_configdir=/opt/vyatta/config
export vyatta_infodir=/opt/vyatta/share/info
export vyatta_localedir=/opt/vyatta/share/local
export vyatta_sbindir=/opt/vyatta/sbin

SET=${vyatta_sbindir}/my_set

DELETE=${vyatta_sbindir}/my_delete

COPY=${vyatta_sbindir}/my_copy

MOVE=${vyatta_sbindir}/my_move

RENAME=${vyatta_sbindir}/my_rename

ACTIVATE=${vyatta_sbindir}/my_activate

DEACTIVATE=${vyatta_sbindir}/my_activate

COMMENT=${vyatta_sbindir}/my_comment

COMMIT=${vyatta_sbindir}/my_commit

DISCARD=${vyatta_sbindir}/my_discard

SAVE=${vyatta_sbindir}/vyatta-save-config.pl



cli-shell-api inSession
if [ $? -ne 0 ]; then
    echo "Something went wrong!"
fi


cli-shell-api getPreCommitHookDir
cli-shell-api loadFile "$1"
$COMMIT


if [ $? -eq 0 ] ; then

$SAVE

fi


function atexit() {
    cli-shell-api teardownSession
}
trap atexit EXIT
