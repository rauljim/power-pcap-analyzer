power-pcap-analyzer
===================

Parse data from Monsoon Power Monitor (.pt4) and tcpdump (.pcap) to generate network/power graphs.


Instructions
------------

Place your input data (.pt4 and .pcap files) in the "raw" directory. For each experiment, both files must have the same name. For instance, 201306201120.pcap and 201306201120.pcap.

If you want to test the code but you don't have raw data yet, you may use these samples:
- http://people.kth.se/~rauljc/spotify/201306201120.pt4
- http://people.kth.se/~rauljc/spotify/201306201120.pcap

Run the main script:

```
python power_pcap_analyzer.py
```


Dependencies
------------

Using Ubuntu, you'll need the following packages:

- python-pcapy
- python-matplotlib


Legal
-----

(C) 2013 Raul Jimenez

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. See LICENSE file.
