# panoramix-server

## Install

### From sources

To use panoramix-server from sources:

```
$ sudo apt-get install libvips-tools
$ git clone https://github.com/pblottiere/panoramix-server
$ cd panoramix-server
$ virtualenv -p /usr/bin/python3 venv
$ . venv/bin/activate
(venv)$ pip install -e .
```

## How to prepare images and database

### IIPImage

The image server currently tested is IIPImage. To work with this server, we
need tiled multi-resolution TIF images.

If you have jpeg images, the *vips* command line tool is made for you. The
python script named *pxvips.sh* is justa a wrapper shell script using *vips*
and allowing to convert a full directory of images:

```
$ ./tools/pxvips.sh --input <input_dir> --output <output_dir>
```

## How to run

panoramix-server has been tested with uWSGI, Nginx and IIPImage.

Once files *pxserver.uwsgi.yml* and *pxserver.yml* are well configurated for your
environment, you can run panoramix-server:

```
(venv)$ pip install uwsgi
(venv)$ uwsgi --yml conf/pxserver.uwsgi.yml
spawned uWSGI worker 1 (pid: 5984, cores: 1)

```

To test your installation:

```
$ curl http://localhost:5000/infos/online
"Congratulation, panoramix-server is online!!!"
```
``

## License

panoramix-server is distributed under LPGL2 or later.
