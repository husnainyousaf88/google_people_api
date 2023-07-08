import requests



# "https://www.linkedin.com/developers/apps/verification/37c1074c-772e-473f-b861-20fef2becac1"



from linkedin import linkedin

# Set up LinkedIn API credentials
linkedin_api_key = '77t2a4sy8ntt18'
linkedin_api_secret = 'mW2VizpkT1jMn6jD'
linkedin_user_token = 'YOUR_USER_TOKEN'
linkedin_user_secret = 'YOUR_USER_SECRET'


def check_linkedin_user(email):
    # Set up LinkedIn API client
    authentication = linkedin.LinkedInDeveloperAuthentication(
        linkedin_api_key,
        linkedin_api_secret,
        linkedin_user_token,
        linkedin_user_secret,
        'http://localhost:8000/auth/callback'
    )
    application = linkedin.LinkedInApplication(authentication)

    # Search for LinkedIn profiles based on email
    profiles = application.search_profile(selectors=[{'people': ['id']}], params={'email': email})

    # Check if LinkedIn profile found
    if profiles and profiles.get('people', {}).get('_total', 0) > 0:
        print("User exists on LinkedIn.")
    else:
        print("User does not exist on LinkedIn.")

# Provide the email address to check
email_to_check = 'example@example.com'

# Check if user exists on LinkedIn
check_linkedin_user("husnain.yousaf8888@gmail.com")
