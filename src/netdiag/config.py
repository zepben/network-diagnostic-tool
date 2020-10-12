#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Format of settings variables.
    """
    ewb_host: str
    ewb_port: int
    ewb_scheme: str

    class Config:
        """Link to environment variables
        """
        env_file = '.env'
