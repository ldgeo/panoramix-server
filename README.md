# panoramix-server

**panoramix-server** is a server of metadatas for panoramics images. Thanks to
these metadatas, a client is then able to retrieve images on an image server
like IIPImage.

## Install

### From sources

To use panoramix-server from sources:

```
$ git clone https://github.com/pblottiere/panoramix-server
$ cd panoramix-server
$ virtualenv -p /usr/bin/python3 venv
$ . venv/bin/activate
(venv)$ pip install -e .
```


## How to prepare images and database

### IIPImage

The image server currently tested is IIPImage. To work with this server, we
need tiled multi-resolution TIFF images with *GPSInfo* EXIF tags.

If you have jpeg images, the *convert* command line tool from *ImageMagick* is
made for you. The script named *pxconvert* is just a a wrapper shell script using
*convert* and *exiftool* to convert a full directory of images retaining all EXIF
tags:

```
$ sudo apt-get install graphicsmagick-imagemagick-compat libimage-exiftool-perl
$ ./tools/pxconvert --input <input_dir> --output <output_dir>
```


### Database

To build the database and fill it accordingly, you can use the *px2pg*
script. But firstly you have to edit a configuration file to fit to your
environment (postgres password and so on). For example the *pxserver.yml*:

```
flask:
    PROPAGATE_EXCEPTIONS: True
    DEBUG: True
    PG_HOST: localhost
    PG_NAME: panoramix
    PG_PORT: 5432
    PG_USER: myusername
    PG_PASSWORD: mypassword
    PG_TABLE: metadatas
```

Then, you can run the *px2pg* script by indicating the yaml file with postgtres
configuration, the input directory with tif images and the kind of images
(*equi* or *cube*). But firstly, you have to create the database and activate
the postgis extension:

```
$ createdb panoramix
$ psql panoramix
psql (9.5.1)
Type "help" for help.

panoramix=# create extension postgis;
CREATE EXTENSION
panoramix=#\q
$
$ ./tools/px2pg pxserver.yml equi <images_tiff_dir>
```


## How to run

panoramix-server has been tested with uWSGI, Nginx and IIPImage.

Once files *pxserver.uwsgi.yml* and *pxserver.yml* are well configurated for
your environment, you can run panoramix-server:

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


## License

panoramix-server is distributed under LPGL2 or later.


## Example

TODO
