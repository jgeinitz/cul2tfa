# cul2tfa
Read IT+ telegrams using CUL (www.busware.de) and decode the info

When cul is set to mode "Nf2" it starts receiving rav packets.
A received telegram looks like this (at least on my device):

	N029385566A32EACFA72A48800A

On http://fredboboss.free.fr/articles/tx29.php is an excelent
information on the 1st 5 bytes of the packet - thus

	N029385566A32EACFA72A48800A
        !!!!---------!!-----------!
        !!!     +           +--------- unknown to me
        !!!     +
        !!!     +--------------------- decoded using the info from fred
        !!!
        !!+--------------------------- ID-info from CUL

With that info decoding results in:
SensorID:    14
New battery: no
low battery: no
Temp:        15.6
humidity:    NaN

sensorid:14 newbat:0 lowbat:0 temp:15.6 humidity:-1

The last line is suitable for some other tools like cacti or
nagios to postprocess the info


