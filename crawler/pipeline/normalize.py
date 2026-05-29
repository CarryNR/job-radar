import re

CITY_ALIASES = {
    "北京市": "北京",
    "上海市": "上海",
    "深圳市": "深圳",
    "广州市": "广州",
    "杭州市": "杭州",
    "成都市": "成都",
}


def normalize_city(city: str | None) -> str | None:
    if not city:
        return None
    city = city.strip()
    return CITY_ALIASES.get(city, city.replace("市", ""))


def normalize_salary(text: str | None) -> tuple[int | None, int | None]:
    if not text:
        return None, None
    nums = [int(n) for n in re.findall(r"(\d+)", text.replace(",", ""))]
    if not nums:
        return None, None
    if len(nums) == 1:
        return nums[0] * 1000, nums[0] * 1000
    low, high = nums[0], nums[1]
    if low < 100:
        low, high = low * 1000, high * 1000
    return low, high


def truncate_description(text: str, max_len: int = 500) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
