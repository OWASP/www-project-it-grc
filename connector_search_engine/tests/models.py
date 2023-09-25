# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from contextlib import contextmanager

from odoo import fields, models

from ..tools.adapter import SearchEngineAdapter


class FakeSeAdapter(SearchEngineAdapter):
    def __init__(self, *args):
        super().__init__(*args)
        if not hasattr(self, "_mocked_calls"):
            # Not using the context manager below
            self._mocked_calls = []

    def index(self, data):
        self._mocked_calls.append(
            dict(index=self.index_record, method="index", args=data)
        )

    def delete(self, binding_ids):
        self._mocked_calls.append(
            dict(index=self.index_record, method="delete", args=binding_ids)
        )

    def clear(self):
        self._mocked_calls.append(
            dict(index=self.index_record, method="clear", args=None)
        )

    def each(self):
        self._mocked_calls.append(
            dict(index=self.index_record, method="each", args=None)
        )
        return [{"id": 42}]

    @classmethod
    @contextmanager
    def mocked_calls(cls):
        """Handle mocking of calls.

        Usage:

            with FakeSeAdapter.mocked_calls() as calls:
                # do something, then
                self.assertEqual(calls[0]['method'], 'clear')
                # do more
        """
        cls._mocked_calls = []
        yield cls._mocked_calls
        cls._mocked_calls = []


class FakeSerializer:
    def serialize(self, record):
        return {"name": record.name, "id": record.id}


class SeBackend(models.Model):
    _inherit = "se.backend"

    backend_type = fields.Selection(
        selection_add=[("fake", "Fake")], ondelete={"fake": "cascade"}
    )

    def _get_adapter_class(self):
        if self.backend_type == "fake":
            return FakeSeAdapter
        else:
            return super()._get_adapter_class()


class SeIndex(models.Model):
    _inherit = "se.index"

    serializer_type = fields.Selection(
        selection_add=[("fake", "Fake")], ondelete={"fake": "cascade"}
    )

    def _get_serializer(self):
        if self.serializer_type == "fake":
            return FakeSerializer()
        else:
            return super()._get_serializer()


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "se.indexable.record"]
