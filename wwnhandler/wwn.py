#!/usr/bin/env python3

import binascii
import re


class WWNInvalidError(ValueError):
    def __init__(self, value):
        super(WWNInvalidError, self).__init__("Invalid FC address: {0!r}".format(value))


class WWN(object):
    """ Main class of the package - create WWN object """

    def __init__(self, address):
        """ Constructor
            :param address: String representing a WWN object (with ':' or not)
            :type address: str
            :except WWNInvalidError:
        """
        self._address = address.wwn if isinstance(address, WWN) else self._normalize(address)

    def _normalize(self, address):
        """ Method used for nomalize a WWN
            :param address: String to normalize (contains ':' or not)
            :type address: str
            :except WWNInvalidError:
        """

        ### UUID from OS has a leading 3 before the WWN
        if address[0] == '3' and len(address) == 33:
            address = address[1:]
            
        regexps = [re.compile("^([0-9a-fA-F]{16})$"),
                   re.compile("^([0-9a-fA-F]{32})$"),
                   re.compile("^([0-9a-fA-F]{2}|:){15}$"),
                   re.compile("^([0-9a-fA-F]{2}|:){31}$")]

        if  not any(one_regexp.match(address) for one_regexp in regexps):
            raise WWNInvalidError(address)
        elif address[0] != '6':
            raise WWNInvalidError('Till now only NAA 6 is supported!')
        
        self._address = address if ':' in address else ':'.join(re.findall('..', address))

        return self._address.lower()

    def __eq__(self, other):
        # if the other object is a 'str', we try a conversion
        if isinstance(other, str):
            try:
                other = WWN(other)

            except WWNInvalidError:
                return False

        elif not isinstance(other, WWN):
            return False

        return self._address == other._address

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self._address)

    def __str__(self):
        # By convention the NAA5 WWNs are represented with ':', NAA6 not
        return self.wwn if not self._address[0] == '6' else self.wwn_nodots

    @property
    def decode(self):
        """ Extract the data encoded in the WWN
            :return: Data encoded in the WWN
            :rtype: str
        """
        return self._decode

    @property
    def oui(self):
        """ Get the OUI (Organization Unique Identifier) of the WWN
            :return: OUI string
            :rtype: str
        """

        oui = ''
        first_digit = self._address[0]

        if first_digit not in ('1', '2', '5', '6', 'c'):
            raise WWNInvalidError('No normalized NAA')

        if first_digit != '6':
            raise WWNInvalidError('Till now only NAA 6 is supported!')
        else:
            oui = self.wwn_nodots[1:8]

        return ':'.join(re.findall('..', oui))

    @property
    def vendor(self):
        """ Mapping the OUI to the vendor
            :return: vendor string
            :rtype: str
        """
        vendors = {'00:00:97': 'EMC',
                   '00:60:16': 'EMC',
                   '00:60:48': 'EMC',
                   '00:01:44': 'EMC',
                   '00:a0:98': 'Netapp',
                   '0a:98:00': 'Netapp',
                   '00:50:76': 'IBM',
                   '00:60:e8': 'Hitachi',
                   '00:0C:29': 'VMware'}

        try:
            return vendors[self.oui]
        except KeyError:
            return ''

    @property
    def wwn(self):
        """ Get the normalized WWN string """
        return self._address

    @property
    def wwn_nodots(self):
        """ Get the WWN string without colons """
        return self._address.replace(':', '')

    @property
    def wwn_to_binary(self):
        """ Get the WWN encoded to binary form """
        return bin(int(self.wwn_nodots, 16))[2:]
    
    @property
    def serial(self):
        """ Get the serial number"""
        if self.oui == '00:00:97':
            return self.wwn_nodots[8:20]
        elif self.oui == '00:60:e8':
            return str(int(self.wwn_nodots[10:14], 16))
        else:
            return ''
    
    @property
    def lunid(self):
        """ Get the 'LUN ID' """
        if self.oui == '00:00:97':      #EMC VMAX
            return binascii.unhexlify(self.wwn_nodots[-10:]).decode()
        elif self.oui == '00:60:e8':    #Hitachi
            return self._address[-5:]
        else:
            return ''

if __name__ == "__main__":
    from sys import argv
    
    wwn = WWN(argv[1])
    
    print('''
        WWN:            %s
        WWN (no dots):  %s
        OUI:            %s
        Vendor:         %s
        Serial Number:  %s
        LUN ID:         %s
        ''' 
        %(wwn.wwn, 
          wwn.wwn_nodots,
          wwn.oui,
          wwn.vendor,
          wwn.serial,
          wwn.lunid))
