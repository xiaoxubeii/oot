__author__ = 'tardis'
from opadaptor.resource import tenant
from dalek.api.auth import context
from dalek import utils as dalek_utils


def clean_resource(context, tenant_id, types):
    """
    :param context:
    :param tenant_id:
    :param types: values in ['server', 'network', 'volume', 'image']
    :return:
    """
    root_package = 'opadaptor.resource'
    rs = {}
    for t in types:
        rs[t] = '%s.%s.%s' % (root_package, t, t.capitalize())

    if 'server' in types:
        index = types.index('server')
        types.insert(index, 'server_snapshot')
        rs['server_snapshot'] = '%s.%s.%s' % (root_package, 'server_snapshot', 'ServerSnapshot')

    if 'network' in types:
        index = types.index('network')
        types.insert(index, 'security_group')
        rs['security_group'] = '%s.%s.%s' % (root_package, 'security_group', 'SecurityGroup')
        types.insert(index, 'floatingip')
        rs['floatingip'] = '%s.%s.%s' % (root_package, 'floating_ip', 'FloatingIP')

    if 'volume' in types:
        index = types.index('volume')
        types.insert(index, 'volume_backup')
        rs['volume_backup'] = '%s.%s.%s' % (root_package, 'volume_backup', 'VolumeBackup')
        types.insert(index, 'volume_snapshot')
        rs['volume_snapshot'] = '%s.%s.%s' % (root_package, 'volume_snapshot', 'VolumeSnapshot')

    for t in types:
        try:
            client = dalek_utils.import_class(rs[t])
            client = client()
            resources = client.list(context)

            if isinstance(resources, dict):
                resources = resources.get('%ss' % t)

            for r in resources:
                id = None
                if isinstance(r, dict):
                    id = r.get('id')
                else:
                    id = getattr(r, 'id')

                try:
                    client.delete(context, id)
                except Exception as e:
                    print e

        except Exception as e:
            print e

context = context.RequestContext('admin', user_password='openstack',
                                 project_name='admin',
                                 auth_url='http://192.168.101.10:35358/v2.0')
t = tenant.Tenant()
ts = t.list(context)

for ten in ts:
    clean_resource(context, ten.id, ['network'])

