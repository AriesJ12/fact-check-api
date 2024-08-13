class Config:
    DEBUG = True  # Set to False in production
    NHS_API_BASE_URL = "https://api.nhs.uk/live-well/"
    USER_AGENT = "Mozilla/5.0"
    CONTENT_TYPE = "application/json"
    CONDITIONS = [
        "alcohol-advice",
        "bone-health",
        "eat-well/food-types",
        "eat-well/how-to-eat-a-balanced-diet",
        "eat-well/5-a-day",
        "eat-well/digestive-health",
        "exercise",
        "sexual-health",
        "healthy-teeth-and-gums",
        "healthy-weight/managing-your-weight",
        "pain",
    ]