# Copyright 2017-2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
# Borrowed from cms_form.utils


def data_merge(a, b):
    """Merges `b` into `a` and return merged result.

    NOTE: tuples and arbitrary objects are not handled
    as it is totally ambiguous what should happen.
    Thanks to http://stackoverflow.com/a/15836901/647924
    """
    key = None
    try:
        if a is None or isinstance(a, (str, int, float)):
            # border case for first run or if a is a primitive
            a = b
        elif isinstance(a, list):
            # lists can be only appended
            if isinstance(b, list):
                # merge lists
                a.extend(b)
            else:
                # append to list
                a.append(b)
        elif isinstance(a, dict):
            # dicts must be merged
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise ValueError(
                    'Cannot merge non-dict "{}" into dict "{}"'.format(b, a)
                )
        else:
            raise NotImplementedError('NOT IMPLEMENTED "{}" into "{}"'.format(b, a))
    except TypeError as e:  # pragma: no cover
        raise TypeError(
            '"{}" in key "{}" when merging "{}" into "{}"'.format(e, key, b, a)
        )
    return a
