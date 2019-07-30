# wwnhandler
Simple Python module to decode  Fibre Channel WWN

Inspired by https://github.com/jbrt/devicewwn.git, just in a shorter form (only one file)

Supporting:
- EMC VMAX
- Hitachi
- Netapp E-Series


Create a WWN
------------

At first you have to create your WWN object :

     >>> from wwnhandler.wwn import WWN
     >>> wwn1 = WWN("60000970000296800564533030324346")
     >>> wwn1
     <WWN(60:00:09:70:00:02:96:80:05:64:53:30:30:32:43:46)>
     >>> wwn1.wwn
     '60:00:09:70:00:02:96:80:05:64:53:30:30:32:43:46'
     >>>
     >>>
     >>> wwn2 = WWN("60:06:0e:80:12:b1:6a:00:50:40:b1:6a:00:00:00:02")
     >>> wwn2
     <WWN(60:06:0e:80:12:b1:6a:00:50:40:b1:6a:00:00:00:02)>
     >>> wwn2.no_dots
     '60060e8012b16a005040b16a00000002'


Useful properties
-----------------

For EMC VMAX, Netapp E-Series and Hitachi there are more propertiers supported:

-  oui : extract the OUI (Organization Unique Identifier) of the WWN
-  vendor : extract the vendor 
-  serial : extract the serial number
-  lunid : extract the 'LUN ID'

::

    >>> wwn1.oui
    '00:00:97'
    >>> wwn1.vendor
    'EMC'
    >>> wwn1.serial
    '000296800564'
    >>> wwn1.lunid
    '002CF'
    >>>
    >>> wwn2.vendor
    'Hitachi'
    wwn2.serial
    >>> wwn2.serial
    '45418'
    >>> wwn2.lunid
      '00:02'
