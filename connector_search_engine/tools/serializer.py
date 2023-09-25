# copyright: 2023 ACSONE SA/NV (https://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from abc import ABC, abstractmethod

from odoo.models import Model


class ModelSerializer(ABC):
    """Base serializer for the search engine."""

    @abstractmethod
    def serialize(self, record: Model) -> dict:
        """Serialize the record into a dict.

        The dict will be sent to the search engine.
        """
        ...
