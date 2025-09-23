import json
import holidays

def helper(country, year, subdiv = None):
    try:
        country_holidays = holidays.country_holidays(country=country, subdiv=subdiv, years=year)
        # collect unique holiday names for that country
        holiday_names = dict.fromkeys(country_holidays.values(), '')
        return holiday_names
    except Exception as e:
        print(f"⚠️ Skipping {country}: {e}")

    return {}

def get_all_holiday_names(year: int = 2025) -> dict[str, str]:
    """
    Get the set of holiday names for all countries supported by the `holidays` package.

    Args:
        year (int): Year to fetch holidays for (default = 2025).

    Returns:
        dict[str, set[str]]: A mapping of country code -> set of holiday names.
    """
    all_holidays = {}

    for country_code, subdivs in holidays.list_supported_countries().items():
        if not subdivs:
            all_holidays.update(helper(country_code, year))

        else:
            all_holidays[country_code] = {}
            for subdiv in subdivs:
                all_holidays.update(helper(country_code, year, subdiv))
    return all_holidays


if __name__ == "__main__":
    holidays_by_country = get_all_holiday_names(2025)
    print(json.dumps(holidays_by_country, indent=4))