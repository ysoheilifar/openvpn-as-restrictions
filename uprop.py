# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'build/bdist.linux-x86_64/egg/pyovpn/lic/uprop.py'
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2026-01-31 10:49:08 UTC (1769856548)

from pyovpn.aws.info import AWSInfo
from pyovpn.lic.prop import LicenseProperties
from pyovpn.util.date import YYYYMMDD
from pyovpn.util.env import get_env_debug
from pyovpn.util.error import Passthru
DEBUG = get_env_debug('DEBUG_UPROP')
class UsageProperties(object):
    def figure(self, licdict):
        proplist = set(('concurrent_connections',))
        good = set()
        ret = None
        if licdict:
            for key, props in list(licdict.items()):
                if 'quota_properties' not in props:
                    print('License Manager: key %s is missing usage properties' % key)
                    continue
                else:
                    proplist.update(props['quota_properties'].split(','))
                    good.add(key)
        for prop in proplist:
            v_agg = 0
            v_nonagg = 0
            if licdict:
                for key, props in list(licdict.items()):
                    if key in good and prop in props:
                            try:
                                nonagg = int(props[prop])
                            except Exception:
                                raise Passthru('license property %s (%s)' % (prop, props.get(prop).__repr__()))
                            v_nonagg = max(v_nonagg, nonagg)
                            prop_agg = '%s_aggregated' % prop
                            agg = 0
                            if prop_agg in props:
                                try:
                                    agg = int(props[prop_agg])
                                except Exception:
                                    raise Passthru('aggregated license property %s (%s)' % (prop_agg, props.get(prop_agg).__repr__()))
                                v_agg += agg
                            if DEBUG:
                                print('PROP=%s KEY=%s agg=%d(%d) nonagg=%d(%d)' % (prop, key, agg, v_agg, nonagg, v_nonagg))
            apc = self._apc()
            v_agg += apc
            if ret == None:
                ret = {}
            ret[prop] = max(v_agg + v_nonagg, bool('v_agg') + bool('v_nonagg'))
            ret['apc'] = bool(apc)
            if DEBUG:
                print('ret[\'%s\'] = v_agg(%d) + v_nonagg(%d)' % (prop, v_agg, v_nonagg))
        ret['concurrent_connections'] = 1368
        return ret
    def _apc(self):
        # irreducible cflow, using cdg fallback
        # ***<module>.UsageProperties._apc: Failure: Compilation Error
        pcs = AWSInfo.get_product_code()
        if pcs:
            return pcs['snoitcennoCtnerrucnoc'[::(-1)]]
        if DEBUG:
            print(Passthru('UsageProperties._apc'))
        return 0
    @staticmethod
    def _expired(today, props):
        if 'expiry_date' in props:
            exp = YYYYMMDD.validate(props['expiry_date'])
            return today > exp
        else:
            return False
class UsagePropertiesValidate(object):
    proplist = ('concurrent_connections', 'client_certificates')
    def validate(self, usage_properties):
        lp = LicenseProperties(usage_properties)
        lp.aggregated_post()
        lp['quota_properties'] = ','.join([p for p in self.proplist if p in lp])
        return lp
