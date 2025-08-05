class User:
    def __init__(self, attributes: dict):
        # Normalize and clean data during initialization
        self.first_name = attributes.get("first_name", "").strip()
        self.last_name = attributes.get("last_name", "").strip()
        self.email = attributes.get("email", "").strip()
        self.wbs = self._parse_wbs(attributes.get("wbs", ""))
        self.kw_filter = [kw.lower() for kw in attributes.get("kw_filter", [])]
        self.loc_filter = [loc.lower() for loc in attributes.get("loc_filter", [])]
        self.max_rent = self._parse_float(attributes.get("max_rent", 0.0))
        self.min_rooms = self._parse_float(attributes.get("min_rooms", 0.0))
        self.min_sqm = self._parse_float(attributes.get("min_sqm", 0.0))
        self.net_income = self._parse_float(attributes.get("net_income", 0.0))

    @staticmethod
    def _parse_wbs(value):
        # Convert user input to boolean
        if isinstance(value, bool):
            return value
        return 'yes' in str(value).lower()

    @staticmethod
    def _parse_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
