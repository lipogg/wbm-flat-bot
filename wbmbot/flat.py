import re
import hashlib

class Flat:
    def __init__(self, attributes: dict):
        self.detail_link = attributes.get("detail_url", "")
        self.title = attributes.get("title", "")
        self.total_rent = self._parse_currency(attributes.get("total_rent", 0.0))
        self.base_rent = self._parse_currency(attributes.get("base_rent", 0.0))
        self.size = self._parse_sqm(attributes.get("size", 0.0))
        self.rooms = self._parse_sqm(attributes.get("rooms", 0.0))
        self.zip_code = self._extract_zipcode(attributes.get("zip_code", ""))
        self.property_attrs = [attr.lower() for attr in attributes.get("property_attrs", [])]
        self.wbs = any("wbs" in attr for attr in self.property_attrs)
        # Compute hash for deduplication
        self.hash = self._compute_hash()

    def matches_criteria(self, user):
        if self.total_rent > user.max_rent:
            return False
        if self.rooms < user.min_rooms:
            return False
        if self.size < user.min_sqm:
            return False
        if user.kw_filter and not all(
                keyword in " ".join(self.property_attrs).lower() for keyword in user.kw_filter):
            return False
        if user.loc_filter and not any(
                self.zip_code.startswith(prefix.strip()) for prefix in user.loc_filter if prefix.strip()):
            return False

        return True

    def within_range(self, user):
        if not (0.15 * user.net_income <= self.base_rent <= 0.30 * user.net_income):
            return False
        return True

    def update_details(self, detail_attrs: dict):
        # Update or add attributes only available from detail page
        if "base_rent" in detail_attrs:
            self.base_rent = self._parse_currency(detail_attrs.get("base_rent", ""))
        if "detail_url" in detail_attrs:
            self.detail_link = detail_attrs.get("detail_url", "")
        # can be extended to retrieve more attributes from details page

    def _compute_hash(self):
        hash_input = f"{self.title}{self.total_rent}{self.size}{self.rooms}{self.zip_code}{self.wbs}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

    @staticmethod
    def _parse_currency(value):
        try:
            return float(value.replace("€", "").replace("EUR", "").replace(".", "").replace(",", ".").strip())
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _parse_sqm(value):
        try:
            return float(value.replace("m²", "").replace(",", ".").strip())
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _extract_zipcode(text):
        match = re.search(r'\b\d{5}\b', text)
        return match.group() if match else ""