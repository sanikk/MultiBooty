## SysFS system

### /sys/block

Examples here use /sys/block/sdc/*

#### Disk

Listed under /sys/block/sdX/ where X is a,b,c,...

##### Sectors

/sys/block/sdc/size gives number of sectors.
/sys/block/sdc/queue/hw_sector_size gives sector size.

##### Vendor
/sys/block/sdX/device/vendor

##### Model
/sys/block/sdX/device/model

##### device_busy

/sys/block/sdX/device/device_busy

Ok if this is over 0 there's still activity going on. Polling this should work.

##### removable

/sys/block/sdc/removable

1 or 0
##### label

Nope

##### fstype

Nope


#### Partitions

Listed under /sys/block/sdc/sdcX/ where X is partition number.

/sys/block/sdc/sdc1/size
/sys/block/sdc/sdc1/start

inflight gives number of read and write operations going on like this:
    0      0
or
    1      5
should be very very up-to-date



