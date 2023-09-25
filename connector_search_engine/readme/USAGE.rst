Overview
~~~~~~~~

A search engine is a system designed to store information in a way that makes
it easy to find through search and analytics queries. The main difference
between a search engine and a database is that a search engine is optimized
for search and analytics queries, while a database is optimized for
transactional and relational queries.

This addons is designed around 4 main concepts:

* **The search engine backend** is used to define into Odoo the kind
  of search engine that will be used to index the data. It's main responsibility
  is to provide an instance of `odoo.addons.search_engine.tools.adapter.SearchEngineAdapter`
  that will be used to communicate with the search engine.

* **The search engine index** is used to define into Odoo the index where
  the data will be indexed. An index is always linked to a search engine backend.
  The index provides methods to use to manage the lifecycle of the data put into
  the index for the records of a given model. To do so, it uses:

  * **The SearchEngineAdapter** provided by the backend to communicate with the
    search engine.
  * **A ModelSerializer** that is used to transform an odoo record into
    a dictionary that can be indexed into the search engine.
  * **A JsonValidator** that is used to validate the data that is to be
    indexed into the search engine.

  The RecordSerializer and IndexDataValidator are defined on the index itself.
  The current addon provides a default implementation only for the IndexDataValidator.
  You can find into the github repository `search-engine <https://github.com:
  OCA/search-engine/tree/16.0>`_ An implementation of the RecordSerializer based
  on the jsonifier addon `connector_search_engine_jsonifier`.

* **The search engine indexable record** is a mixin that is used to define
  the records that can be indexed into a search engine index. The mixin
  provides methods:

  * To add a record to an index.
  * To remove a record from an index.
  * To mark the record into an index (*the search engine bindings*) as to be
    recomputed (This method should be called when modifications are made on
    the record that could impact the data that are indexed into the search
    engine. It will instruct the index that the record must be recomputed and
    re-indexed).

  It also ensures that when the record is unlinked, it is removed from the indexes
  it was indexed into.

* **The search engine binding** is a model that represents the link between
  an index and an indexable odoo record. It give you access to the data
  that are indexed into the search engine for the record. It's also used to
  manage the lifecycle of the data into the search engine. When a binding is
  created, it's marked as to be computed. Once the data are computed, the
  binding is marked as to be indexed. Once the data are indexed, the binding
  is marked as indexed. If the linked record is unlinked, the binding is
  marked as to be removed. Once the data are removed from the search engine,
  the binding is deleted.

Indexing lifecycle
~~~~~~~~~~~~~~~~~~

The indexing lifecycle is based on the following steps:

* When a record is added to an index, a binding is created and marked as to be
  computed.
* A cron job scheduled every 5 minutes will look for bindings that are to be
  computed and for each of them will schedule a job to re compute the json data.
* When the json data is computed, the binding is marked as to be exported if the
  json is valid and is different from the one that has been computed last time.
* A cron job scheduled every 5 minutes will ensure the syncing with the search
  engine. It will:

  * look for bindings that are to be exported and for each of them will schedule
    a job to export the json data into the search engine. Once exported, the
    binding is marked as 'done'.
  * look for bindings that are to be removed and for each of them will schedule
    a job to remove the data from the search engine. Once removed, the binding
    is deleted.

To keep in sync the data from your model instance and the data that are indexed
into the search engine, you should call the method `_se_mark_to_update` on the
mode instance when you make modifications that could impact the data that are
indexed into the search engine.

* When the method `_se_mark_to_update` is called, the binding is marked as to be
  computed.
* From there, the same process as described above will be used to recompute the
  data and reindex them into the search engine.

When a model instance is unlinked, the binding is marked as to be removed. From
there if will be processed by the job syncing the data with the search engine.

.. note::

  In previous versions of this addon, there was no method to mark a record as
  to be recomputed. As a consequence, all the records were re-computed every day
  to ensure that the data in the search engine were up to date. This was a
  performance issue and consumed a lot of resources. If despite this, you want
  to recompute all the records every day, you can activate the cron jon
  `Search engine: recompute all index` and deactivate the one named
  `earch engine: Generate job for recompute binding to recompute per index`.
