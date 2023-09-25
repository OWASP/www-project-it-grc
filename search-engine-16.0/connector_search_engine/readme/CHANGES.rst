Changelog
---------

Future (?)
~~~~~~~~~~


14.0.2.0.0
~~~~~~~~~~~~

**Breaking change**


For historical reason (first implementation with algolia)
- the id of the binding was added in the index
- and for elastic/algolia the objectID (= the id of the record bound) was also added

This lead to a uncomprehensible situation where the frontend dev have an "id" and an "objectID" with different value and have no idea of which one should be used for filtering

Magic injection of the "id" have been removed (as we already define a export.line in shopinvader) and explicit is better then implicit.

Note: in shopinvader we push in the key "id" the id of the record bound (we do not care of the id of the binding).

Elastic Connector do not use any more the "objectID" key
Algolia Connector still use the "objectID" (required) but the value is the same as the id

See issue shopivader issue `#1000 <https://github.com/shopinvader/odoo-shopinvader/issues/1000>`_


12.0.2.0.0
~~~~~~~~~~

- index field name is now a computed field based on the backend name, the model exported and the lang
- remove dependency on keychain
- Improve UI on search engine backend (domain on model and exporter...)
- improve test coverage
- use black for auto code style
