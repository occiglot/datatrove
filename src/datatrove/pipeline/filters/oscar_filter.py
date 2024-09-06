import re

from datatrove.data import Document
from datatrove.pipeline.filters.base_filter import BaseFilter
from datatrove.pipeline.writers.disk_base import DiskWriter

DEFAULT_OSCAR_MIN_HARMFUL_PP = 25.0
DEFAULT_OSCAR_MAX_HARMFUL_PP = 100_000

DEFAULT_EXCLUDE_CATEGORIES = {
    # See http://dsi.ut-capitole.fr/blacklists/index_en.php
    "agressif",
    "adult",
    "cryptojacking",
    "dangerous_material",
    "phishing",
    "warez",
    "ddos",
    "hacking",
    "malware",
    "mixed_adult",
    "sect",
}


class OSCARFilter(BaseFilter):
    name = "🗑 OSCAR"

    def __init__(self,
                 exclusion_writer: DiskWriter = None,
                 min_harmful_ppl: float = DEFAULT_OSCAR_MIN_HARMFUL_PP,
                 max_harmful_ppl: float = DEFAULT_OSCAR_MAX_HARMFUL_PP,
                 exclude_categories: set = DEFAULT_EXCLUDE_CATEGORIES):
        """
        filters data based on OSCAR annotations

        Args:
            regex_exp: regex expression
            exclusion_writer:
        """
        super().__init__(exclusion_writer)
        self.min_harmful_ppl = min_harmful_ppl
        self.max_harmful_ppl = max_harmful_ppl
        self.exclude_categories = exclude_categories

    def filter(self, doc: Document) -> bool | tuple[bool, str]:
        """Args:
            doc: document

        Returns:
            is_filter
        """
        if doc.metadata['oscar_quality_warnings']:
            return False, 'oscar_quality_warning'
        if doc.metadata['harmful_pp'] and doc.metadata['harmful_pp'] < self.min_harmful_ppl:
            return False, 'kenlm_min_harmful_ppl'
        if doc.metadata['harmful_pp'] and doc.metadata['harmful_pp'] > self.max_harmful_ppl:
            return False, 'kenlm_max_harmful_ppl'
        if doc.metadata['oscar_categories'] and len(set(doc.metadata['oscar_categories']) & self.exclude_categories) > 0:
            return False, 'oscar_category'
        return True
