# -*- coding: utf-8 -*-

# (c)2018 Wanless Systems Ltd.
# Author: Brian Sidebotham <brian@wanless.systems>

import os
import logging

from salt.states.file import managed as file_managed

log = logging.getLogger(__name__)

def managed_config(
            name,
            source=None,
            source_hash='',
            source_hash_name=None,
            keep_source=True,
            user=None,
            group=None,
            mode=None,
            attrs=None,
            template=None,
            makedirs=False,
            dir_mode=None,
            context=None,
            replace=True,
            defaults=None,
            backup='',
            show_changes=True,
            create=True,
            contents=None,
            tmp_dir='',
            tmp_ext='',
            contents_pillar=None,
            contents_grains=None,
            contents_newline=True,
            contents_delimiter=':',
            encoding=None,
            encoding_errors='strict',
            allow_empty=True,
            follow_symlinks=True,
            check_cmd=None,
            skip_verify=False,
            win_owner=None,
            win_perms=None,
            win_deny_perms=None,
            win_inheritance=True,
            win_perms_reset=False,
            **kwargs):
    """Using the same call convention as a modern Salt file.managed, but not
    everything is available to us. Instead the following are the only things
    currently being passed on to the 2014.1 version of file.managed:

    name,
    source,
    template,
    context
    """

    # This cludge lets us cross-call state functions. In newer versions of
    # Salt this shouldn't really be necessary, but as of right not the VyOS
    # version of Salt is 2014.1 and this requires the kludge to feed the
    # function with the necessary global variables
    for ddict in 'env salt opts grains pillar'.split():
        dd = '__%s__' % ddict
        file_managed.func_globals[dd] = globals()[dd]

    log.debug("__env__: " + str(__env__))

    # Get the current configuration back from VyOS. When we have the
    # current configuration we can save it to a file to know what has
    # changed between the currently running configuration and the new
    # configuration
    cfg = __salt__['vyos.get_config']()

    # If the file exists, save the running configuration to the file
    if os.path.isfile(name):
        with open(name, "w") as f:
            f.write(cfg)

    # Process this as a managed file, and when it's necessary to change the
    # file, use the VyOS execution module functions to do so
    managed = file_managed(name, source=source, template=template, context=context)

    # Make sure we only load (commit and save) the configuration if something
    # has changed...
    if not __opts__['test']:
        if managed['result'] is True:
            log.debug("Loading the configuration from the named file " + name)
            __salt__['vyos.load_config'](name, saltenv=__env__)
    else:
        log.debug("Not managing file because testing")

    # Return the result provided by file.managed
    return managed
