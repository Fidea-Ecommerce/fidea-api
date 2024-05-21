import re
from rapidfuzz import process, fuzz
from difflib import SequenceMatcher


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
    async def search_product(inputan, data, threshold=0.4):
        hasil = []
        for product, store in data:
            judul = product.title.lower()
            similarity_ratio = SequenceMatcher(None, inputan.lower(), judul).ratio()
            if similarity_ratio >= threshold:
                hasil.append((product, store))
        return hasil
