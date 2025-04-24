from getpass import getpass
import time
from nova_act import NovaAct,BOOL_SCHEMA

def linkedin_job_apply():
    # Initialize Nova
    with NovaAct(starting_page="https://www.linkedin.com/home" ) as nova:
        nova.start()
    
    
        try:
        # Get job title from user
            job_title = input("Enter the job title you want to search for: ")
        
            # Navigate to LinkedIn
       
            nova.act("go to linkedin.com")
        
            # Check for captcha
            result = nova.act("Is there a captcha on the screen?", schema=BOOL_SCHEMA)
            if result.matches_schema and result.parsed_response:
                input("Please solve the captcha and hit return when done")
        
            # Sign in process
        
            nova.act("click on sign in")
        
         # Enter email
            nova.act("enter email your email adress and click Enter")
            nova.act("click on password field and wait")

        
            # Securely get password from user
            password = getpass("Enter your LinkedIn password: ")
            nova.page.keyboard.type(password)
        
            # Click sign in button
            nova.act("click sign in button")
        
      
        
            # Navigate to Jobs
        
            nova.act("click on jobs icon")
        
            # Search for the job
       
            nova.act(f"type {job_title} in the search bar and press enter")
        

        
  
            nova.act("click on the first job result")
        
        
        
        # Click Easy Apply button

            nova.act("click on LinkedIn Easy Apply button")
        
      
        
   
            nova.act("click Next button")
        
        # On resume page, click Review
            nova.act("click Review button")
        
     
        
   
            nova.act("click Submit application button")
        
       
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
        # Clean up
            nova.stop()

def main():
    """Main function to run the LinkedIn job application automation"""
    try:
        linkedin_job_apply()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
