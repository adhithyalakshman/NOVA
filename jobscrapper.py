from getpass import getpass
import time
import csv
from datetime import datetime
from nova_act import NovaAct, BOOL_SCHEMA

def linkedin_job_scraper():
    # Initialize Nova
    with NovaAct(starting_page="https://www.linkedin.com/home") as nova:
        nova.start()
    
        try:
            # Get job title from user
            job_title = input("Enter the job title you want to search for: ")
            
         
            
            # Check for captcha
            result = nova.act("Is there a captcha on the screen?", schema=BOOL_SCHEMA)
            if result.matches_schema and result.parsed_response:
                input("Please solve the captcha and hit return when done")
            
            # Sign in process
            nova.act("click on sign in")
            
            # Enter email
            nova.act("enter adhithyalakshman111@gmail.com and click Enter")
            
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
            
            # Add experience level filter for Entry level
            nova.act("click on Experience Level filter")
            nova.act("select Entry level option")
            
            # Create CSV file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Job Title', 'Company Name', 'Location', 'Application Link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Scrape first 100 jobs
                for i in range(100):
                    try:
                        # Get job details
                        nova.act(f"click on job result number {i+1}")
                        time.sleep(2)  # Wait for job details to load
                        
                        # Get job title
                        job_title = nova.act("get the job title").parsed_response
                        
                        # Get company name
                        company_name = nova.act("get the company name").parsed_response
                        
                        # Get location
                        location = nova.act("get the job location").parsed_response
                        
                        # Get application link
                        application_link = nova.page.url
                        
                        # Write to CSV
                        writer.writerow({
                            'Job Title': job_title,
                            'Company Name': company_name,
                            'Location': location,
                            'Application Link': application_link
                        })
                        
                        # Go back to search results
                        nova.act("go back to search results")
                        time.sleep(1)  # Wait for results to load
                        
                    except Exception as e:
                        print(f"Error processing job {i+1}: {str(e)}")
                        continue
                
            print(f"\nJob data has been saved to {filename}")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Clean up
            nova.stop()

def main():
    """Main function to run the LinkedIn job scraper"""
    try:
        linkedin_job_scraper()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
