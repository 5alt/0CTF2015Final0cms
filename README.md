# 0CTF2015Final_0cms

This program is used for 0CTF 2015 Final named 0cms.
Use this only for code auditing practice and avoid being accessed by other people.

## installation

```
sudo pip install rsa
sudo pip install web.py
```

## ussage

If you are using ubuntu, just run:

`sh restart.sh`

For mac or other platform, you need to modify `settings.py` and set `WEB_URL` based on your own ip address instead of using `get_local_ip()` function.

For cheker, you need to modify `0cms_full_check.py` and set variable `flag` base your own flag.(I just use an api to get real flag.)

## acknowledgement

0cms is based on `webpyCMS0.1`
https://github.com/taogogo/webpyCMS

Thanks taogogo for developing such good blog management system!

## contact

http://5alt.me

md5_salt [AT] qq.com

Hope you enjoy this! :)
