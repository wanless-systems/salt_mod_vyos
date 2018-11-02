#!/bin/sh

# (c)2018 Wanless Systems Ltd.

scriptdir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

module_name=vyos

if [ $# -ne 1 ]; then
    echo "usage: ${0} file_roots_directory" >&2
    exit 1
fi

installdir=${1}

if [ ! -d ${installdir} ]; then
    echo "${installdir} does not exist" >&2
    exit 1
fi

# Install the execution module
if [ ! -d ${installdir}/_modules ]; then
    mkdir -p ${installdir}/_modules
fi

# The vyos execution module goes into the _modules directory to be distributed to the minions
# # You can update these with salt '*' saltutil.sync_modules
rm -f ${installdir}/_modules/${module_name}.py > /dev/null 2>&1
ln -s ${scriptdir}/modules/${module_name}.py ${installdir}/_modules/${module_name}.py

if [ ! -d ${installdir}/_states ]; then
    mkdir -p ${installdir}/_states
fi

# The vyos state functions go into the _states directory to be disributed to the minions.
# You can update these with salt '*' saltutil.sync_states
rm -f ${installdir}/_states/${module_name}.py > /dev/null 2>&1
ln -s ${scriptdir}/state/${module_name}.py ${installdir}/_states/${module_name}.py

rm -f ${installdir}/${module_name}.sls > /dev/null 2>&1
ln -s ${scriptdir}/state/${module_name}.sls ${installdir}/${module_name}.sls

# Make the configuration template available
rm -f ${installdir}/${module_name}_config.j2 > /dev/null 2>&1
ln -s ${scriptdir}/files/${module_name}_config.j2 ${installdir}/${module_name}_config.j2

# Install the scripts that are downloaded by the execution module to run on VyOS
rm -f ${installdir}/vyos_diff_config.sh > /dev/null 2>&1
ln -s ${scriptdir}/files/vyos_diff_config.sh ${installdir}/vyos_diff_config.sh

rm -f ${installdir}/vyos_load_config.sh > /dev/null 2>&1
ln -s ${scriptdir}/files/vyos_load_config.sh ${installdir}/vyos_load_config.sh
