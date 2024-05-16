import re
from rapidfuzz import process, fuzz


class Miscellaneous:
    @staticmethod
    async def check_password_strength(password):
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[!@#$%^&*()-+=]", password):
            return False
        return True

    @staticmethod
    async def search_product(query, products):
        results = process.extract(query, products, scorer=fuzz.token_sort_ratio)
        return results
