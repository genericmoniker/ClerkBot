from clerkbot.missionary_accounts import process_lines

WARD_MISSIONARY_DATA = {
    "categoryName": "Ward Missionary Fund",
    "income": 5000,
    "expense": -4000,
    "transfers": 0,
    "startBalance": 10000.00,
    "sortOrder": 4,
    "lines": [
        {
            "subcategory": {
                "categoryId": 3,
                "category": "Ward Missionary Fund",
                "catSortOrder": 4,
                "subcategoryId": 9,
                "subcategory": "Ward Missionary Fund",
                "subcatSortOrder": 1
            },
            "expense": 0,
            "income": 400,
            "transfers": -3500,
            "startBalance": 10000.00
        },
        {
            "subcategory": {
                "categoryId": 3,
                "category": "Ward Missionary Fund",
                "catSortOrder": 4,
                "subcategoryId": 9,
                "subcategory": "Ward Missionary Fund",
                "subcatSortOrder": 1,
                "unitSubcategoryId": 1111111,
                "unitSubcategory": "New, Elder"
            },
            "expense": 0,
            "income": 0,
            "transfers": 0,
            "startBalance": 0
        },
        {
            "subcategory": {
                "categoryId": 3,
                "category": "Ward Missionary Fund",
                "catSortOrder": 4,
                "subcategoryId": 9,
                "subcategory": "Ward Missionary Fund",
                "subcatSortOrder": 1,
                "unitSubcategoryId": 2222222,
                "unitSubcategory": "Moved, Elder"
            },
            "expense": 0,
            "income": 0,
            "transfers": 1825,
            "startBalance": 1825
        },
        {
            "subcategory": {
                "categoryId": 3,
                "category": "Ward Missionary Fund",
                "catSortOrder": 4,
                "subcategoryId": 9,
                "subcategory": "Ward Missionary Fund",
                "subcatSortOrder": 1,
                "unitSubcategoryId": 3333333,
                "unitSubcategory": "Home, Sister"
            },
            "expense": -800,
            "income": 1400,
            "transfers": 0,
            "startBalance": -800
        },
        {
            "subcategory": {
                "categoryId": 3,
                "category": "Ward Missionary Fund",
                "catSortOrder": 4,
                "subcategoryId": 9,
                "subcategory": "Ward Missionary Fund",
                "subcatSortOrder": 1,
                "unitSubcategoryId": 4444444,
                "unitSubcategory": "Smith, Elder"
            },
            "expense": -2000,
            "income": 2400,
            "transfers": 0,
            "startBalance": 0
        }
    ]
}


def test_balance_calculations_are_correct():
    accounts = process_lines(WARD_MISSIONARY_DATA)
    assert len(accounts) == 4
    assert accounts[0].balance == 0.00
    assert accounts[1].balance == 3650.00
    assert accounts[2].balance == -200.00
    assert accounts[3].balance == 400.00
