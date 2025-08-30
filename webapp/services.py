# services.py
# Affinidi credential request construction logic

from django.conf import settings
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

personal_information_credential_type_id = os.environ.get("PERSONAL_INFORMATION_CREDENTIAL_TYPE_ID")
employment_credential_type_id = os.environ.get("EMPLOYMENT_CREDENTIAL_TYPE_ID")
education_credential_type_id = os.environ.get("EDUCATION_CREDENTIAL_TYPE_ID")
address_credential_type_id = os.environ.get("ADDRESS_CREDENTIAL_TYPE_ID")
background_check_credential_type_id = os.environ.get("BACKGROUND_CHECK_CREDENTIAL_TYPE_ID")

def get_six_months_from_now():
    dt = datetime.now() + timedelta(days=180)
    # Format: yyyy-MM-dd'T'HH:mm:ss.SSSZ
    # Python's %f gives microseconds, so we take first 3 digits for milliseconds
    ms = f"{dt.microsecond // 1000:03d}"
    formatted = dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms}Z")
    return formatted

def build_credentials_request(type_id):
    if type_id == "personalInformation":
        return [
            {
                "credentialTypeId": personal_information_credential_type_id,
                "credentialData": {
                    "name": {
                        "givenName": "Grajesh",
                        "familyName": "Chandra",
                        "nickname": "Grajesh Testing",
                    },
                    "birthdate": "01-01-1990",
                    "birthCountry": "India",
                    "citizenship": "Indian",
                    "phoneNumber": "7666009585",
                    "nationalIdentification": {
                        "idNumber1": "pan",
                        "idType1": "askjd13212432d",
                    },
                    "email": "grajesh.c@affinidi.com",
                    "gender": "male",
                    "maritalStatus": "married",
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "Done",
                }
            }
        ]
    elif type_id == "address":
        return [
            {
                "credentialTypeId": address_credential_type_id,
                "credentialData": {
                    "address": {
                        "addressLine1": "Varthur, Gunjur",
                        "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                        "postalCode": "560087",
                        "addressRegion": "Karnataka",
                        "addressCountry": "India",
                    },
                    "ownerDetails": {
                        "ownerName": "TestOwner",
                        "ownerContactDetails1": "+912325435634",
                    },
                    "neighbourDetails": {
                        "neighbourName": "Test Neighbour",
                        "neighbourContactDetails1": "+912325435634",
                    },
                    "stayDetails": {"fromDate": "01-01-2000", "toDate": "01-01-2020"},
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "Letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "done",
                },
                "metaData": {"expirationDate": "2027-09-01T00:00:00.000Z"},
            }
        ]
    elif type_id == "education":
        return [
            {
                "credentialTypeId": education_credential_type_id,
                "credentialData": {
                    "candidateDetails": {
                        "name": "Grajesh Chandra",
                        "phoneNumber": "7666009585",
                        "email": "grajesh.c@affinidi.com",
                        "gender": "male",
                    },
                    "institutionDetails": {
                        "institutionName": "Affinidi",
                        "institutionAddress": {
                            "addressLine1": "Varthur, Gunjur",
                            "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                            "postalCode": "560087",
                            "addressRegion": "Karnataka",
                            "addressCountry": "India",
                        },
                        "institutionContact1": "+91 1234567890",
                        "institutionContact2": "+91 1234567890",
                        "institutionEmail": "test@affinidi.com",
                        "institutionWebsiteURL": "affinidi.com",
                    },
                    "educationDetails": {
                        "qualification": "Graduation",
                        "course": "MBA",
                        "graduationDate": "12-08-2013",
                        "dateAttendedFrom": "12-08-2011",
                        "dateAttendedTo": "12-07-2013",
                        "educationRegistrationID": "admins1223454356",
                    },
                    "verificationStatus": "Verified",
                    "verificationEvidence": {
                        "evidenceName1": "Degree",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "completed",
                },
                "metaData": {"expirationDate": "2027-09-01T00:00:00.000Z"},
            }
        ]
    elif type_id == "employment":
        return [
            {
                "credentialTypeId": employment_credential_type_id,
                "credentialData": {
                    "candidateDetails": {
                        "name": "Grajesh Chandra",
                        "phoneNumber": "7666009585",
                        "email": "grajesh.c@affinidi.com",
                        "gender": "male",
                    },
                    "employerDetails": {
                        "companyName": "Affinidi",
                        "companyAddress": {
                            "addressLine1": "Varthur, Gunjur",
                            "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                            "postalCode": "560087",
                            "addressRegion": "Karnataka",
                            "addressCountry": "India",
                        },
                        "hRDetails": {
                            "hRfirstName": "Testing",
                            "hRLastName": "HR",
                            "hREmail": "hr@affinidi.com",
                            "hRDesignation": "Lead HR",
                            "hRContactNumber1": "+911234567789",
                            "whenToContact": "9:00-6:00 PM",
                        },
                    },
                    "employmentDetails": {
                        "designation": "Testing",
                        "employmentStatus": "Fulltime",
                        "annualisedSalary": "10000",
                        "currency": "INR",
                        "tenure": {"fromDate": "05-2022", "toDate": "06-2050"},
                        "reasonForLeaving": "Resignation",
                        "eligibleForRehire": "Yes",
                    },
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "Done",
                },
                "metaData": {"expirationDate": "2027-09-01T00:00:00.000Z"},
            }
        ]

        return [
            {
                "credentialTypeId": background_check_credential_type_id,
                "credentialData": {
                    "personalInformation": {
                        "positionApplied": "Software Engineer",
                        "firstName": "John",
                        "middleName": "Michael",
                        "lastName": "Doe",
                        "aka": "Johnny",
                        "email": "john.doe@example.com",
                        "phoneNo": "123-456-7890",
                        "alterPhoneNo": "098-765-4321",
                        "civilStatus": "Married",
                        "gender": "Male",
                        "primaryIdCard": "Passport",
                        "primaryIdCardNo": "A12345678",
                        "primaryIdCard2": "Driver's License",
                        "primaryIdCardNo2": "D987654321",
                        "photo": "https://example.com/photos/john_doe.jpg",
                        "notes": "Available for immediate joining.",
                    },
                    "addressDetails": {
                        "address": [
                            {
                                "addressLine1": "123 Main St",
                                "addressLine2": "Apt 4B",
                                "city": "New York",
                                "stateOrRegion": "NY",
                                "postalCode": "10001",
                                "country": "USA",
                                "stayDateFrom": "2015-06-01",
                                "stayDateTo": "2020-05-31",
                                "houseOwnerName": "Jane Smith",
                                "houseOwnerContactNo": "111-222-3333",
                                "houseOwnerEmail": "jane.smith@example.com",
                                "neighborName": "Emily Davis",
                                "neighborContactNo": "444-555-6666",
                                "neighborEmail": "emily.davis@example.com",
                            }
                        ]
                    },
                    "educationDetails": [
                        {
                            "education": [
                                {
                                    "institutionName": "Stanford University",
                                    "institutionContactNo": "650-723-2300",
                                    "institutionEmail": "admissions@stanford.edu",
                                    "isGraduated": "Yes",
                                    "dateFrom": "2010-09-01",
                                    "dateTo": "2014-06-30",
                                    "dateGraduated": "2014-06-30",
                                    "modeOfStudy": "Full-time",
                                    "addressLine1": "450 Serra Mall",
                                    "addressLine2": "",
                                    "postalCode": "94305",
                                    "stateRegion": "CA",
                                    "city": "Stanford",
                                }
                            ]
                        }
                    ],
                    "employmentDetails": {
                        "employment": [
                            {
                                "companyName": "Tech Corp",
                                "position": "Junior Developer",
                                "employmentStatus": "Full-time",
                                "annualSalary": "60000",
                                "salaryCurrency": "USD",
                                "isCurrent": "No",
                                "whenToContact": "Anytime",
                                "canCommunicate": "Yes",
                                "dateFrom": "2016-07-01",
                                "dateTo": "2018-06-30",
                                "reasonForLeaving": "Career Growth",
                                "companyEmail": "hr@techcorp.com",
                                "addressLine1": "789 Tech Ave",
                                "addressLine2": "",
                                "postalCode": "90001",
                                "stateRegion": "CA",
                                "city": "Los Angeles",
                                "country": "USA",
                                "hr_first_name": "Alice",
                                "hr_last_name": "Johnson",
                                "hr_email": "alice.johnson@techcorp.com",
                                "hr_contact_no": "123-456-7890",
                                "hr_personnel_position": "HR Manager",
                                "eligibleForRehire": "Yes",
                                "underAgency": "No",
                                "agencyName": "",
                            }
                        ]
                    },
                    "employmentPerformanceDetails": {
                        "employmentPerformance": [
                            {
                                "companyName": "Tech Corp",
                                "position": "Junior Developer",
                                "supervisorFirstName": "Carol",
                                "supervisorMiddleName": "",
                                "supervisorLastName": "White",
                                "supervisorPosition": "Team Lead",
                                "supervisorEmail": "carol.white@techcorp.com",
                                "addressLine1": "789 Tech Ave",
                                "addressLine2": "",
                                "postalCode": "90001",
                                "stateRegion": "CA",
                                "city": "Los Angeles",
                                "country": "USA",
                                "contactNo": "123-456-7890",
                                "isCurrent": "No",
                                "canCommunicate": "Yes",
                                "whenToContact": "Anytime",
                                "referenceRelationship": "Supervisor",
                                "bestTimeToCall": "10 AM - 4 PM",
                            }
                        ]
                    },
                    "professionalQualificationDetails": {
                        "professionalQualification": [
                            {
                                "certificateIssuingAuthority": "Oracle",
                                "qualificationAttained": "Oracle Certified Professional, Java SE 8 Programmer",
                                "certificateNumber": "OCJP123456789",
                                "dateGranted": "2015-08-15",
                                "country": "USA",
                            }
                        ]
                    },
                },
            }
        ]
    elif type_id == "batch-credentials":
        return [
            {
                "credentialTypeId": personal_information_credential_type_id,
                "credentialData": {
                    "name": {
                        "givenName": "Grajesh",
                        "familyName": "Chandra",
                        "nickname": "Grajesh Testing",
                    },
                    "birthdate": "01-01-1990",
                    "birthCountry": "India",
                    "citizenship": "Indian",
                    "phoneNumber": "7666009585",
                    "nationalIdentification": {
                        "idNumber1": "pan",
                        "idType1": "askjd13212432d",
                    },
                    "email": "grajesh.c@affinidi.com",
                    "gender": "male",
                    "maritalStatus": "married",
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "Done",
                },
            },
            {
                "credentialTypeId": address_credential_type_id,
                "credentialData": {
                    "address": {
                        "addressLine1": "Varthur, Gunjur",
                        "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                        "postalCode": "560087",
                        "addressRegion": "Karnataka",
                        "addressCountry": "India",
                    },
                    "ownerDetails": {
                        "ownerName": "TestOwner",
                        "ownerContactDetails1": "+912325435634",
                    },
                    "neighbourDetails": {
                        "neighbourName": "Test Neighbour",
                        "neighbourContactDetails1": "+912325435634",
                    },
                    "stayDetails": {"fromDate": "01-01-2000", "toDate": "01-01-2020"},
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "Letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "done",
                },
            },
            {
                "credentialTypeId": education_credential_type_id,
                "credentialData": {
                    "candidateDetails": {
                        "name": "Grajesh Chandra",
                        "phoneNumber": "7666009585",
                        "email": "grajesh.c@affinidi.com",
                        "gender": "male",
                    },
                    "institutionDetails": {
                        "institutionName": "Affinidi",
                        "institutionAddress": {
                            "addressLine1": "Varthur, Gunjur",
                            "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                            "postalCode": "560087",
                            "addressRegion": "Karnataka",
                            "addressCountry": "India",
                        },
                        "institutionContact1": "+91 1234567890",
                        "institutionContact2": "+91 1234567890",
                        "institutionEmail": "test@affinidi.com",
                        "institutionWebsiteURL": "affinidi.com",
                    },
                    "educationDetails": {
                        "qualification": "Graduation",
                        "course": "MBA",
                        "graduationDate": "12-08-2013",
                        "dateAttendedFrom": "12-08-2011",
                        "dateAttendedTo": "12-07-2013",
                        "educationRegistrationID": "admins1223454356",
                    },
                    "verificationStatus": "Verified",
                    "verificationEvidence": {
                        "evidenceName1": "Degree",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "completed",
                },
            },
            {
                "credentialTypeId": employment_credential_type_id,
                "credentialData": {
                    "candidateDetails": {
                        "name": "Grajesh Chandra",
                        "phoneNumber": "7666009585",
                        "email": "grajesh.c@affinidi.com",
                        "gender": "male",
                    },
                    "employerDetails": {
                        "companyName": "Affinidi",
                        "companyAddress": {
                            "addressLine1": "Varthur, Gunjur",
                            "addressLine2": "B305, Candeur Landmark, Tower Eiffel",
                            "postalCode": "560087",
                            "addressRegion": "Karnataka",
                            "addressCountry": "India",
                        },
                        "hRDetails": {
                            "hRfirstName": "Testing",
                            "hRLastName": "HR",
                            "hREmail": "hr@affinidi.com",
                            "hRDesignation": "Lead HR",
                            "hRContactNumber1": "+911234567789",
                            "whenToContact": "9:00-6:00 PM",
                        },
                    },
                    "employmentDetails": {
                        "designation": "Testing",
                        "employmentStatus": "Fulltime",
                        "annualisedSalary": "10000",
                        "currency": "INR",
                        "tenure": {"fromDate": "05-2022", "toDate": "06-2050"},
                        "reasonForLeaving": "Resignation",
                        "eligibleForRehire": "Yes",
                    },
                    "verificationStatus": "Completed",
                    "verificationEvidence": {
                        "evidenceName1": "letter",
                        "evidenceURL1": "http://localhost",
                    },
                    "verificationRemarks": "Done",
                },
            },
        ]

        # Add more credential types as needed
    return None
