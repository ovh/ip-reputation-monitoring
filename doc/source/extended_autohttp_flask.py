import re
import itertools
import six

from docutils.parsers.rst import directives

from sphinx.util import force_decode
from sphinx.util.docstrings import prepare_docstring
from sphinx.pycode import ModuleAnalyzer

import sphinxcontrib.autohttp.flask as flask
from sphinxcontrib import httpdomain
from sphinxcontrib.autohttp.common import http_directive, import_object


def get_routes(app, endpoint=None):
    endpoints = []
    routes = []
    for rule in app.url_map.iter_rules(endpoint):
        if rule.endpoint not in endpoints:
            endpoints.append(rule.endpoint)
    for endpoint in endpoints:
        methodrules = {}
        for rule in app.url_map.iter_rules(endpoint):
            methods = rule.methods.difference(['OPTIONS', 'HEAD'])
            path = rule.rule
            for method in methods:
                if method in methodrules:
                    methodrules[method].append(path)
                else:
                    methodrules[method] = [path]
        for method, paths in methodrules.items():
            routes.append((method, paths, endpoint))

    routes = sorted(routes, key=lambda tup: tup[1][0])
    for route in routes:
        yield route


class AutoExtendedflaskDirective(flask.AutoflaskDirective):

    option_spec = {'endpoints': directives.unchanged,
                   'blueprints': directives.unchanged,
                   'undoc-endpoints': directives.unchanged,
                   'undoc-blueprints': directives.unchanged,
                   'undoc-static': directives.unchanged,
                   'include-empty-docstring': directives.unchanged,
                   'path-validate-regexs': directives.unchanged,
                   'path-cancel-regexs': directives.unchanged}

    @property
    def path_validate_regexs(self):
        path_validate_regexs = self.options.get('path-validate-regexs', None)
        if not path_validate_regexs:
            return []
        return re.split(r'\s*,\s*', path_validate_regexs)

    @property
    def path_cancel_regexs(self):
        path_cancel_regexs = self.options.get('path-cancel-regexs', None)
        if not path_cancel_regexs:
            return []
        return re.split(r'\s*,\s*', path_cancel_regexs)

    def check_regex_validate_path(self, paths):
        """
        :return: True if on regex valid the path
        """
        if not self.path_validate_regexs:
            return True
        for path_validate_regex in self.path_validate_regexs:
            for path in paths:
                if re.match(path_validate_regex, path):
                    return True
        return False

    def check_regex_cancel_path(self, paths):
        """
        :return: True if on regex cancel the path
        """
        if not self.path_validate_regexs:
            return True
        for path_validate_regex in self.path_cancel_regexs:
            for path in paths:
                if re.match(path_validate_regex, path):
                    return True
        return False

    def make_rst(self, **kwargs):
        app = import_object(self.arguments[0])
        if self.endpoints:
            routes = itertools.chain(*[get_routes(app, endpoint)
                                     for endpoint in self.endpoints])
        else:
            routes = get_routes(app)

        for method, paths, endpoint in routes:
            if not self.check_regex_validate_path(paths):
                continue
            if self.check_regex_cancel_path(paths):
                continue
            try:
                blueprint, _, endpoint_internal = endpoint.rpartition('.')
                if self.blueprints and blueprint not in self.blueprints:
                    continue
                if blueprint in self.undoc_blueprints:
                    continue
            except ValueError:
                pass  # endpoint is not within a blueprint

            if endpoint in self.undoc_endpoints:
                continue
            try:
                static_url_path = app.static_url_path  # Flask 0.7 or higher
            except AttributeError:
                static_url_path = app.static_path  # Flask 0.6 or under
            if ('undoc-static' in self.options and endpoint == 'static' and
                    static_url_path + '/(path:filename)' in paths):
                continue
            view = app.view_functions[endpoint]
            docstring = view.__doc__ or ''
            if hasattr(view, 'view_class'):
                meth_func = getattr(view.view_class, method.lower(), None)
                if meth_func and meth_func.__doc__:
                    docstring = meth_func.__doc__
            if not isinstance(docstring, six.text_type):
                analyzer = ModuleAnalyzer.for_module(view.__module__)
                docstring = force_decode(docstring, analyzer.encoding)

            if not docstring and 'include-empty-docstring' not in self.options:
                continue
            docstring = prepare_docstring(docstring)
            for line in http_directive(method, paths, docstring):
                yield line


def setup(app):
    httpdomain.setup(app)
    app.add_directive('autoextendedflask', AutoExtendedflaskDirective)
