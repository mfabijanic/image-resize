# Dependencies

Install dependencies in virtualenv "otobo"

Create virtualenv "otobo" in $HOME/.virtualenv
```
mkdir ~/.virtualenv
cd ~/.virtualenv
virtualenv -p python3 otobo
```

Activate virtualenv otobo
```
source $HOME/.virtualenv/otobo/bin/activate
```

Install filetype and Pillow
```sh
pip3 install filetype
pip3 install Pillow
```


# How to use
```sh
cp find-and-resize.ini.example find-and-resize.ini
cp logging.ini.example logging.ini
```

Change configuration files

Set Directory PATH

    find-and-resize.ini
```
path = /custom/directory/path
```

Change log file PATH. Default is in /dev/shm (RAM disk).

    logging.ini
```
[handler_fileHandlerResize]
args = ('/custom/log/path/find-and-resize.log',)
```
