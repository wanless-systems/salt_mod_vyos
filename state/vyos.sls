
managed_vyos_config:
    vyos.managed_config:
        - name: /config/config.boot.salt
        - source: salt://vyos_config.j2
        - template: jinja

