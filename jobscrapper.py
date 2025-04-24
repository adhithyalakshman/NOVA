from getpass import getpass
import time
import pandas as pd
from datetime import datetime
from nova_act import NovaAct, BOOL_SCHEMA

def linkedin_job_scraper():
    # Initialize Nova
    with NovaAct(starting_page="https://www.linkedin.com/home") as nova:
        nova.start()
    
        try:
            # Get job title from user
            job_title_input = input("Enter the job title you want to search for: ")
            
            # Check for captcha
            result = nova.act("Is there a captcha on the screen?", schema=BOOL_SCHEMA)
            if result.matches_schema and result.parsed_response:
                input("Please solve the captcha and hit return when done")
            
            # Sign in process
            nova.act("click on sign in")
            nova.act("enter adhithyalakshman111@gmail.com and click Enter")
            nova.act("click on password field and wait")
            
            password = getpass("Enter your LinkedIn password: ")
            nova.page.keyboard.type(password)
            nova.act("click sign in button")
            
            # Navigate to Jobs section
            nova.act("click on jobs icon")
            
            # Search for the job
            nova.act(f"type {job_title_input} in the search bar and press enter")
            nova.act("press enter")
            
            # Add Entry level filter
            nova.act("click on Experience Level filter")
            nova.act("select Entry level option")
            
            jobs_data = []

            for i in range(11):
                try:
                    nova.act(f"click on job result number {i+1}")
                    # Wait for job panel to load

                    # Extract job details with better prompts
                    job_title_result = nova.act(
                        "Read the job title from the job details panel on the right side",
                        schema={"type": "string"}
                    )
                    company_name_result = nova.act(
                        "Read the company name from the job details panel on the right side",
                        schema={"type": "string"}
                    )
                    location_result = nova.act(
                        "Read the job location from the job details panel on the right side",
                        schema={"type": "string"}
                    )

                    job_title = job_title_result.parsed_response
                    company_name = company_name_result.parsed_response
                    location = location_result.parsed_response
                    application_link = nova.page.url

                    print(f"Found job: {job_title} at {company_name} in {location}")

                    jobs_data.append({
                        'Job Title': job_title,
                        'Company Name': company_name,
                        'Location': location,
                        'Application Link': application_link
                    })

                    nova.act("go back to search results")

                except Exception as e:
                    print(f"Error processing job {i+1}: {str(e)}")
                    continue
            
            # Save data to CSV
            df = pd.DataFrame(jobs_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"\nJob data has been saved to {filename}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            nova.stop()

def main():
    try:
        linkedin_job_scraper()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
