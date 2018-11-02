# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (C) 2018 Wanless Systems Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

'''
Module for managing VyOS using the native salt client.
'''

# Import Python libs
import logging
import salt

# Import Salt libs
from salt.exceptions import CommandExecutionError
log = logging.getLogger(__name__)


def _verify_run(out, cmd=None):
    '''
    Crash to the log if command execution was not successful.
    '''
    if out.get("retcode", 0) and out['stderr']:
        if cmd:
            log.debug('Command: "%s"', cmd)

        log.debug('Return code: %s', out.get('retcode'))
        log.debug('Error output:\n%s', out.get('stderr', "N/A"))

        raise CommandExecutionError(out['stderr'])


def get_config():
    '''
    Get configuration from device.

    CLI Example:

    .. code-block:: bash

        salt '*' vyos.get_config
    '''
    out = __salt__['cmd.run_all']("cli-shell-api showCfg --show-show-defaults",
                                    shell='/bin/vbash',
                                    python_shell=True )
    if out.get('stderr'):
        raise CommandExecutionError(out['stderr'])
    return out['stdout'] + "\n"


def load_config(configfile, saltenv=u'base'):
    '''
    Load a configuration file to use as running config
    '''
    out = __salt__['cmd.script']("salt://vyos_load_config.sh", args=configfile, shell='/bin/bash', saltenv=saltenv)

    if out['retcode'] == 0:
        return out['stdout']
    else:
        raise CommandExecutionError(out['stdout'] + "\n" + out['stderr'])


def diff_config(configfile, saltenv=u'base'):
    '''
    Get the current configuration difference between the ``configfile``
    file and the running configuration
    '''
    out = __salt__['cmd.script']("salt://vyos_diff_config.sh", args=configfile,
                                 shell='/bin/bash', saltenv=saltenv)

    if out['retcode'] == 0:
        return out['stdout']
    else:
        raise CommandExecutionError(out['stdout'] + "\n" + out['stderr'])


def get_version():
    '''
    Get current interface configuration from device.

    CLI Example:

    .. code-block:: bash

        salt '*' vyos.get_version
    '''
    out = __salt__['cmd.run_all']("/usr/libexec/vyos/op_mode/version.py",
                                    shell='/bin/vbash',
                                    python_shell=True )
    if out.get('stderr'):
        raise CommandExecutionError(out['stderr'])
    return out['stdout']
