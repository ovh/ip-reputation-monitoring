#!/usr/bin/env python3
#
# Copyright (C) 2017, OVH SAS
#
# This file is part of ip-reputation-monitoring.
#
# ip-reputation-monitoring is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Running the flask API.
"""

from flask import Flask, jsonify
from config import settings


def create_app():
    """ Initialize flask application. """
    app = Flask(__name__)

    from api.controllers.reputation import reputation as reputation_blueprint
    app.register_blueprint(reputation_blueprint, url_prefix='/reputation')
    from api.controllers.blacklist import blacklist as blacklist_blueprint
    app.register_blueprint(blacklist_blueprint, url_prefix='/blacklist')
    from api.controllers.spamhaus import spamhaus as spamhaus_blueprint
    app.register_blueprint(spamhaus_blueprint, url_prefix='/spamhaus')

    if not settings.API['debug']:
        @app.errorhandler(500)
        def internal_server_error(error):
            """ Default handler for 500 errors """
            app.logger.error('An internal error occured: %s', error)
            return jsonify({'error': 'An internal error occured, please retry later.'}), 500

        @app.errorhandler(404)
        def page_not_found(error):
            """ Default handler for 404 errors """
            app.logger.info('Requested endpoint cannot be found: %s', error)
            return jsonify({'error': 'Requested endpoint cannot be found.'}), 404

    return app


APP = create_app()
if __name__ == "__main__":
    APP.run(**settings.API)
