CLASSIFICATION_VALUES = {
    "Spam": 29,
    "Marketing": 31,
    "Events": 37,
    "Delivery": 41,
    "Analytics": 43,
    "Business": 47,
    "Invoice": 53,
    "Urgent": 59,
}

RATING_VALUES = {
    1: 2,
    2: 3,
    3: 5,
    4: 7,
    5: 11,
    6: 13,
    7: 17,
    8: 19,
    9: 23,
}

def find_classification_and_rating(num):
    classification = None
    rating = None
    
    # Check for classification
    for key, value in CLASSIFICATION_VALUES.items():
        if num % value == 0:
            classification = key
            break

    # Check for rating
    for key, value in RATING_VALUES.items():
        if num % value == 0:
            rating = key
            break

    return classification, rating


