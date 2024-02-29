# bypass OpenVPN Access Server restrictions

> [!CAUTION]
> This method for educational purposes.

### What is OpenVPN Access Server
OpenVPN Access Server is a convenient tool that is installed on the server in a couple of commands and allows you to comfortably work with clients: change subnets, profiles, passwords and other settings. Doing all this manually would be much more difficult.

The free version of OpenVPN Access Server has a connection limit: only two clients can connect at a time. A paid license, in addition to being expensive, is now impossible to physically pay for.

> [!NOTE]
> This method work on server running [ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/) or [debian 10](https://releases.ubuntu.com/focal/](https://cdimage.debian.org/debian-cd/project/build/10.13.0/)https://cdimage.debian.org/debian-cd/project/build/10.13.0/)
> because to do this, we will use the uncompyle6 utility, which works great with Python versions 2.7, 3.7, 3.8.

### Let's Start
#### 1. Install prerequisites
```bash
apt install zip unzip
apt install python3-pip
pip install uncompyle6
```
#### 2. Unzip `pyovpn-2.0-py3.8.egg` file
```bash
cd /usr/local/openvpn_as/lib/python
unzip pyovpn-2.0-py3.8.egg
cd /usr/local/openvpn_as/lib/python/pyovpn/lic
uncompyle6 uprop.pyc > uprop.py
```
#### 3. Edit `uprop.py` file
add `ret['concurrent_connections'] = 1368` line to the file
```bash
vi uprop.py
...
            apc = self._apc()
            v_agg += apc
            if ret == None:
                ret = {}
            ret[prop] = max(v_agg + v_nonagg, bool('v_agg') + bool('v_nonagg'))
            ret['apc'] = bool(apc)
            if DEBUG:
                print("ret['%s'] = v_agg(%d) + v_nonagg(%d)" % (prop, v_agg, v_nonagg))
        ret['concurrent_connections'] = 1368
        return ret
    def _apc(self):
...
```
#### 4. Compile file
```bash
python3 -m compileall uprop.py
rm uprop.pyc uprop.py
cp __pycache__/uprop.cpython-38.pyc ./uprop.pyc
rm -Rf __pycache__
sudo rm /usr/local/openvpn_as/lib/python/pyovpn-2.0-py3.8.egg
zip pyovpn pyovpn-2.0-py3.8.egg
```
#### 5. Restart service and remove log files
```bash
service openvpnas stop
rm /var/log/openvpnas.log
touch /var/log/openvpnas.log
service openvpnas start
cat /var/log/openvpnas.log
```
