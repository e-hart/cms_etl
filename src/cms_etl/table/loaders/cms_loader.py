"""Load CMS data from the CMS API."""

import json
import os
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import pkg_resources
import requests

from cms_etl.models.cms_meta_res import CMSMetaResponse
from cms_etl.utils import console


class CMSSourceLoader:
    """Load CMS data from the CMS API"""

    def __init__(self):
        source_path = pkg_resources.resource_filename("cms_etl", "data/cms_sources.json")
        with open(
            source_path,
            "r",
            encoding="utf-8",
        ) as f:
            self.source_dict: dict = json.load(f)

    def get_dataset_url(self, category: str, source: str) -> str:
        """Get the URL for a dataset."""
        url = self.source_dict[category]["sources"][source]["csv_url"]
        if url:
            return url
        else:
            raise ValueError(f"URL not found for {category} - {source}")

    def get_dataset(
        self, category: str, source: CMSMetaResponse
    ) -> Tuple[pd.DataFrame, Dict[str, str | int]] | None:
        """Get a dataset from the CMS API."""
        console.print(f"Getting csv for {source.title}")

        csv_url = source.distribution[0].downloadURL
        console.print(f"CSV URL: {csv_url}")
        csv_filename = csv_url.split("/")[-1]

        # if csv is not in ./data/cms_cache, download it
        cache_dir = pkg_resources.resource_filename("cms_etl", "data/cms_cache")
        if not os.path.exists(cache_dir):
            try:
                Path(cache_dir).mkdir(parents=True, exist_ok=True)
            except OSError as e:
                console.print(f"Error creating cache directory: {e}")

        if csv_filename not in os.listdir(cache_dir):
            try:
                with requests.get(csv_url, stream=True, timeout=5) as r:
                    r.raise_for_status()
                    with open(
                        f"{cache_dir}/{csv_filename}",
                        "wb",
                    ) as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
            except requests.HTTPError as e:
                console.print(f"HTTP Error: {e}")

        try:
            console.print(f"Reading csv: {cache_dir}/{csv_filename}")
            df = pd.read_csv(f"{cache_dir}/{csv_filename}", low_memory=False)
        except pd.errors.ParserError as e:
            console.print("Error parsing csv.", e)
            return None
        return df, {
            "source_type": "cms",
            "care_category": category,
            "s1_category_id": self.get_category_id(category),
            "source_name": source.title,
            "filename": csv_filename,
            "url": csv_url,
        }

    def get_cat_sources(self, category: str) -> list[str]:
        """Get the sources for a category."""
        return self.source_dict[category]["sources"]

    def get_categories(self) -> list[str]:
        """Get the categories."""
        return list(self.source_dict.keys())

    def get_category_id(self, category: str) -> int:
        """Get the category ID for a category."""
        return self.source_dict[category]["s1_category_id"]
