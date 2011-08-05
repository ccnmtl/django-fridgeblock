Refrigerator Magnet Game Pageblock

install as per usual for pageblocks:

* install module
* add to INSTALLED_APPS and PAGEBLOCKS
* add to urls.py:

    (r'^fridge/',include('fridgeblock.urls')),

* manage.py syncdb
* copy fridgeblock/media/ directory into /media/fridge/ (or otherwise
  make available via site_media)



