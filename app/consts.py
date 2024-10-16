PERMISSIONS = [
    {
        "codename": "CAN_CREATE_COURSE",
        "name": "Create Course",
        "flag": 1,
        "description": "Can Create Course",
    },
    {
        "codename": "CAN_ASSIGN_USER_COURSE",
        "name": "Assign User Course",
        "flag": 2,
        "description": "Can Assign User To A Course",
    },
    {
        "codename": "CAN_CREATE_ASSESSMENT",
        "name": "Create Assessment",
        "flag": 3,
        "description": "Can Create Assessment",
    },
    {
        "codename": "CAN_ASSIGN_USER_ASSESSMENT",
        "name": "Assign User Assessment",
        "flag": 4,
        "description": "Can Assign User To An Assessment",
    },
    {
        "codename": "CAN_EVALUATE_USER_ASSESSMENT",
        "name": "Evaluate User Assessment",
        "flag": 5,
        "description": "Can Evaluate User To An Assessment",
    },
]


class PermissionEnum:
    CAN_CREATE_COURSE = "CAN_CREATE_COURSE"
    CAN_ASSIGN_USER_COURSE = "CAN_ASSIGN_USER_COURSE"
    CAN_CREATE_ASSESSMENT = "CAN_CREATE_ASSESSMENT"
    CAN_ASSIGN_USER_ASSESSMENT = "CAN_ASSIGN_USER_ASSESSMENT"
    CAN_EVALUATE_USER_ASSESSMENT = "CAN_EVALUATE_USER_ASSESSMENT"
