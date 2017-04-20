# cul2tfa
Read IT+ telegrams using CUL (www.busware.de) and decode the info

When cul is set to mode "Nf2" it starts receiving raw packets.
A received packet looks like this (at least on my device):

	N029385566A32EACFA72A48800A

On http://fredboboss.free.fr/articles/tx29.php is an excelent
information on the 1st 5 bytes (pr 10 nibbles) of the packet - thus
we know

	N029385566A32EACFA72A48800A
        !!!!--------!!------------!
        !!!     +           +--------- unknown to me
        !!!     +
        !!!     +--------------------- decoded using the info from fred
        !!!
        !!+--------------------------- ID-info from CUL

At the moment I have no idea about the last 7 bytes.

With that info decoding results in:

        SensorID:    14
        New battery: no
        low battery: no
        Temp:        15.6
        humidity:    NaN

        sensorid:14 newbat:0 lowbat:0 temp:15.6 humidity:-1

The last line is suitable for some other tools like cacti or
nagios to postprocess the info.

Juergen
