This addon uses the native json python package provided by python. When
a json for a record is recomputed, the new value is compared to the original
one to see if an export to the search engine index is needed.  This is
done by comparing the md5 of the two json strings. This process when done on
a large number of records can be slow when the json is large and complex. To speed
up this process you can install the orjson package.

.. code-block:: bash

    pip install orjson
