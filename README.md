## Basic Network Diagnostic Tool

Python CLI Tool offers the following methods to find issues in the network data

**NOTE** - Please refer to method documentation to know limitations in the implementation

1. **Incorrect Phases:**
    - Performs downstream trace from seed equipment to find equipments with no equipment container and then
    performs an upstream trace from there to find equipments with no common phases.
    
    
### Build

    python setup.py sdist
    
#### Setup

Requirements: Python 3.7+

1. Install dependencies

        pip install netdiag-0.2.0.tar.gz

2. Setup `.env` file: The project needs a `.env` file where you run from with the following content to pick up the config:  

        ewb_host=<host>
        ewb_port=<port>
        ewb_scheme=<http/https>
   
   Example config:
   
        ewb_host="localhost"
        ewb_port=9000
        ewb_scheme="http"
   
#### Run

See ```netdiag --help ```
        