import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://pyfacerec-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    "2301":
        {
            'name': 'Dr. Vibha Tiwari',
            'major': 'AI & ML',
            'starting_year': 1990,
            'total_attendance': 6,
            'standing': 'Good',
            'year': 5,
            'last_attendance_time': "2023-09-11 00:54:34",
            "attendance":
                {
                    "2023-09-11": True
                }
        },
    "2302":
        {
            'name': 'Dr RK Pandit',
            'major': 'Director',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-07-13 01:13:34",
            "attendance":
                {
                    "2023-09-11": True
                }
        },
    "2303":
        {
            'name': 'Shri A. K. Bajoria',
            'major': 'JK Tyre & Industries',
            'starting_year': 1988,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
            "attendance":
                {
                    "2023-09-11": True
                }
        },
    "2304":
        {
            'name': 'Rudraksh Saraf',
            'major': 'AI & ML',
            'starting_year': 2021,
            'total_attendance': 9,
            'standing': 'Good',
            'year': 3,
            'last_attendance_time': "2023-07-13 00:54:34",
            "attendance":
                {
                    "2023-09-11": True
                }
        },
    "2305":
        {
            'name': 'Siddhant Jain',
            'major': 'Machine Learning',
            'starting_year': 2021,
            'total_attendance': 7,
            'standing': 'Good',
            'year': 3,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2306":
        {
            'name': 'Shri Prashant Mehta',
            'major': 'DG Academy of Administration',
            'starting_year': 1989,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2307":
        {
            'name': 'Prof. K. K. Aggarwal',
            'major': 'Chairman NBA',
            'starting_year': 1989,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2308":
        {
            'name': 'Shrimant J.M Scindia',
            'major': 'Politics',
            'starting_year': 2000,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 24,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2309":
        {
            'name': 'Dr. Manjree Pandit',
            'major': 'Dean Academics',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2310":
        {
            'name': 'Dr. Rajni Ranjan Singh',
            'major': 'HOD centre of AI',
            'starting_year': 1990,
            'total_attendance': 5,
            'standing': 'Good',
            'year': 15,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2311":
        {
            'name': 'Mr. Pashupathy Gopalan',
            'major': 'CEO, SunEdison',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2312":
        {
            'name': 'Er. Lokesh Saxena',
            'major': 'Director, DISA India',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2313":
        {
            'name': 'Er. Ramesh Agrawal',
            'major': 'Former MLA',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
    "2314":
        {
            'name': 'Dr. Mohan Yadav',
            'major': 'CM. Madhya Pradesh',
            'starting_year': 1990,
            'total_attendance': 1,
            'standing': 'Good',
            'year': 20,
            'last_attendance_time': "2023-05-20 00:54:34",
                "attendance":
                    {
                        "2023-09-11": True
                    }
        },
}

ref2 = db.reference('Login')

Login_details = {
    "username": "Rudraksh",
    "password": "password"
}

for key, value in data.items():
    ref.child(key).set(value)

for key, value in Login_details.items():
    ref2.child(key).set(value)
