#!/usr/bin/env python2
import os
import socket
from collections import OrderedDict


am_host = os.getenv('AM_HOST', socket.gethostname())
am_master_host = os.getenv('AM_MASTER_HOST')

variable_map = OrderedDict()
variable_map['SERVER_URL'] = 'AM_SERVER_URL'
variable_map['DEPLOYMENT_URI'] = 'AM_DEPLOYMENT_URI'
variable_map['BASE_DIR'] = 'AM_BASE_DIR'
variable_map['locale'] = 'AM_LOCALE'
variable_map['PLATFORM_LOCALE'] = 'AM_PLATFORM_LOCALE'
variable_map['AM_ENC_KEY'] = 'AM_ENC_KEY'
variable_map['ADMIN_PWD'] = 'AM_ADMIN_PASSWORD'
variable_map['AMLDAPUSERPASSWD'] = 'AM_URL_AGENT_PASSWORD'
variable_map['COOKIE_DOMAIN'] = 'AM_COOKIE_DOMAIN'
variable_map['ACCEPT_LICENSES'] = 'AM_ACCEPT_LICENSES'

variable_map['DATA_STORE'] = 'AM_DATA_STORE_TYPE'
variable_map['DIRECTORY_SSL'] = 'AM_DATA_STORE_SSL'
variable_map['DIRECTORY_SERVER'] = 'AM_DATA_STORE_HOST'
variable_map['DIRECTORY_PORT'] = 'AM_DATA_STORE_PORT'
variable_map['DIRECTORY_ADMIN_PORT'] = 'AM_DATA_STORE_ADMIN_PORT'
variable_map['DIRECTORY_JMX_PORT'] = 'AM_DATA_STORE_JMX_PORT'
variable_map['ROOT_SUFFIX'] = 'AM_DATA_STORE_ROOT_SUFFIX'
variable_map['DS_DIRMGRDN'] = 'AM_DATA_STORE_MANAGER_DN'
variable_map['DS_DIRMGRPASSWD'] = 'AM_DATA_STORE_MANAGER_PASSWORD'

variable_map['DS_EMB_REPL_FLAG'] = 'AM_DATA_STORE_REPLICATION'
variable_map['DS_EMB_REPL_REPLPORT1'] = 'AM_DATA_STORE_REPLICATION_PORT'
variable_map['DS_EMB_REPL_HOST2'] = 'AM_DATA_STORE_REPLICATION_EXISTING_SERVER_HOST'
variable_map['DS_EMB_REPL_ADMINPORT2'] = 'AM_DATA_STORE_REPLICATION_EXISTING_SERVER_PORT'
variable_map['existingserverid'] = 'AM_DATA_STORE_REPLICATION_EXISTING_SERVER_ID'

variable_map['USERSTORE_TYPE'] = 'AM_USER_STORE_TYPE'
variable_map['USERSTORE_SSL'] = 'AM_USER_STORE_SSL'
variable_map['USERSTORE_DOMAINNAME'] = 'AM_USER_STORE_DOMAIN_NAME'
variable_map['USERSTORE_HOST'] = 'AM_USER_STORE_HOST'
variable_map['USERSTORE_PORT'] = 'AM_USER_STORE_PORT'
variable_map['USERSTORE_SUFFIX'] = 'AM_USER_STORE_SUFFIX'
variable_map['USERSTORE_MGRDN'] = 'AM_USER_STORE_MANAGER_DN'
variable_map['USERSTORE_PASSWD'] = 'AM_USER_STORE_MANAGER_PASSWORD'

variable_map['LB_SITE_NAME'] = 'AM_LB_SITE_NAME'
variable_map['LB_PRIMARY_URL'] = 'AM_LB_PRIMARY_URL'

am_config = OrderedDict()
am_config['SERVER_URL'] = os.getenv('AM_SERVER_URL', None if am_host is None else 'http://%s:8080' % am_host)
am_config['DEPLOYMENT_URI'] = os.getenv('AM_DEPLOYMENT_URI', '/openam')
am_config['BASE_DIR'] = os.getenv('AM_BASE_DIR', os.path.join(os.getcwd(), 'config'))
am_config['locale'] = os.getenv('AM_LOCALE', 'en_US')
am_config['PLATFORM_LOCALE'] = os.getenv('AM_PLATFORM_LOCALE', 'en_US')
am_config['AM_ENC_KEY'] = os.getenv('AM_ENC_KEY')
am_config['ADMIN_PWD'] = os.getenv('AM_ADMIN_PASSWORD')
am_config['AMLDAPUSERPASSWD'] = os.getenv('AM_URL_AGENT_PASSWORD')
am_config['COOKIE_DOMAIN'] = os.getenv('AM_COOKIE_DOMAIN')
am_config['ACCEPT_LICENSES'] = os.getenv('AM_ACCEPT_LICENSES', 'true')

missing_vars = []

for key, value in am_config.iteritems():
    if value is None:
        missing_vars.append(variable_map[key])

data_store_config = OrderedDict()
data_store_config['DATA_STORE'] = os.getenv('AM_DATA_STORE_TYPE', 'embedded')
data_store_config['DIRECTORY_SSL'] = os.getenv('AM_DATA_STORE_SSL', 'SIMPLE')
data_store_config['DIRECTORY_SERVER'] = os.getenv('AM_DATA_STORE_HOST', am_host)
data_store_config['DIRECTORY_PORT'] = os.getenv('AM_DATA_STORE_PORT', '50389')

if data_store_config['DATA_STORE'] == 'embedded':
    data_store_config['DIRECTORY_ADMIN_PORT'] = os.getenv('AM_DATA_STORE_ADMIN_PORT', '4444')
    data_store_config['DIRECTORY_JMX_PORT'] = os.getenv('AM_DATA_STORE_JMX_PORT', '1689')

data_store_config['ROOT_SUFFIX'] = os.getenv('AM_DATA_STORE_ROOT_SUFFIX', 'dc=openam,dc=forgerock,dc=org')
data_store_config['DS_DIRMGRDN'] = os.getenv('AM_DATA_STORE_MANAGER_DN', 'cn=Directory Manager')
data_store_config['DS_DIRMGRPASSWD'] = os.getenv('AM_DATA_STORE_MANAGER_PASSWORD')

for key, value in data_store_config.iteritems():
    if value is None:
        missing_vars.append(variable_map[key])

am_config.update(data_store_config)

config_store_repl_config = OrderedDict()

if data_store_config['DATA_STORE'] == 'embedded':
    config_store_repl_config['DS_EMB_REPL_FLAG'] = os.getenv('AM_DATA_STORE_REPLICATION',
                                                             'embReplFlag' if am_master_host is not None else None)
    if config_store_repl_config['DS_EMB_REPL_FLAG'] == 'embReplFlag':
        config_store_repl_config['DS_EMB_REPL_REPLPORT1'] = os.getenv('AM_DATA_STORE_REPLICATION_PORT', '58989')
        config_store_repl_config['DS_EMB_REPL_HOST2'] = os.getenv('AM_DATA_STORE_REPLICATION_EXISTING_SERVER_HOST',
                                                                  am_master_host)
        config_store_repl_config['DS_EMB_REPL_ADMINPORT2'] = os.getenv('AM_DATA_STORE_REPLICATION_EXISTING_SERVER_ADMIN_PORT',
                                                                       '4444')
        config_store_repl_config['DS_EMB_REPL_REPLPORT2'] = os.getenv('AM_DATA_STORE_REPLICATION_EXISTING_SERVER_PORT',
                                                                      '50889')
        config_store_repl_config['existingserverid'] = os.getenv('AM_DATA_STORE_REPLICATION_EXISTING_SERVER_ID',
                                                                 None if am_master_host is None else 'http://%s:8080/openam' % am_master_host)
        for key, value in config_store_repl_config.iteritems():
            if value is None:
                missing_vars.append(variable_map[key])

        am_config.update(config_store_repl_config)

if data_store_config['DATA_STORE'] != 'embedded':
    user_store_config = OrderedDict()
    user_store_config['USERSTORE_TYPE'] = os.getenv('AM_USER_STORE_TYPE', 'LDAPv3ForODSEE')
    user_store_config['USERSTORE_SSL'] = os.getenv('AM_USER_STORE_SSL', 'SIMPLE')
    if user_store_config['USERSTORE_TYPE'] == 'LDAPv3ForADDC':
        user_store_config['USERSTORE_DOMAINNAME'] = os.getenv('AM_USER_STORE_DOMAIN_NAME', 'addc.example.com')
    user_store_config['USERSTORE_HOST'] = os.getenv('AM_USER_STORE_HOST')
    user_store_config['USERSTORE_PORT'] = os.getenv('AM_USER_STORE_PORT', '389')
    user_store_config['USERSTORE_SUFFIX'] = os.getenv('AM_USER_STORE_SUFFIX', 'dc=openam,dc=forgerock,dc=org')
    user_store_config['USERSTORE_MGRDN'] = os.getenv('AM_USER_STORE_MANAGER_DN', 'cn=Directory Manager')
    user_store_config['USERSTORE_PASSWD'] = os.getenv('AM_USER_STORE_MANAGER_PASSWORD')

    for key, value in user_store_config.iteritems():
        if value is None:
            missing_vars.append(variable_map[key])

    am_config.update(user_store_config)

lb_config = OrderedDict()
lb_config['LB_SITE_NAME'] = os.getenv('AM_LB_SITE_NAME')
lb_config['LB_PRIMARY_URL'] = os.getenv('AM_LB_PRIMARY_URL')  # 'http://lb.example.com:80/openam'
if lb_config['LB_SITE_NAME'] is not None or lb_config['LB_PRIMARY_URL'] is not None:
    for key, value in lb_config.iteritems():
        if value is None:
            missing_vars.append(variable_map[key])

    am_config.update(lb_config)

if len(missing_vars) > 0:
    raise RuntimeError("Missing vars: %s" % ', '.join(missing_vars))

for key, value in am_config.iteritems():
    print '%s=%s' % (key, value)
