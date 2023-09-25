# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Connector Search Engine Serializer Ir Export",
    "summary": "Use Exporter (ir.exports) as serializer for index",
    "version": "16.0.1.0.2",
    "development_status": "Alpha",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/search-engine",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "connector_search_engine",
        "jsonifier",
    ],
    "data": [
        "views/se_index_view.xml",
    ],
    "demo": [],
}
