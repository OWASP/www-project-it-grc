# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.component.core import Component


class AlgoliaJsonExportMapper(Component):
    _name = "algolia.json.export.mapper"
    _inherit = ["json.export.mapper", "algolia.se.connector"]

    def _apply(self, map_record, options=None):
        res = map_record._source.jsonify(self._json_parser)[0]

        # Search engine mapper compatibility
        #
        # Algolia do not use the key "id" as key for the
        # record but use a special one like "objectID"
        # If the key defined globaly in _record_id_key is not in the result of
        # the mapper and if the key "id" exist in the result
        # then we automatically put the value of the "id" as value
        # of the key _record_id_key
        #
        # example: for shopinvader all the exporter define the mapping for the key "id"
        # then if you use Algolia there is no need of a glue module
        # the "objectID" is will have the same value as the value of "id"
        #
        # If you need something different you can add a mapping in your exporter

        if self.collection._record_id_key not in res and "id" in res:
            res[self.collection._record_id_key] = res["id"]
        return res
