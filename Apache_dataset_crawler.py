# Imports requests library, is used to read the contents of a webpage
import requests

# Imports os library to read/write files from the OS
import os

# Import lxml library, used to make sense of (HTML structured) webpage contents
from lxml import html

# Total number of files is correct, system fails though, maybe repair (or do not include in final public repository)
def main():

    # Reads contents from the following webpage
    url = "http://mail-archives.apache.org/mod_mbox/lucene-java-user/"
    page = requests.get(url)
    root = html.fromstring(page.content)

    # Finds all the years of email archives featured on website above
    year_tables = reversed(root.xpath('//table[@class="year"]'))

    # Loops through all tables from different years on the website
    for year_table in year_tables:
        year = int(year_table.xpath("thead/tr/th/text()")[0].split(" ")[1])

        # Only if the year range in between 2001-2011
        if year in list(range(2001, 2012)):

            # Finds all the months in said year (2001 does not have all months, we do not use all months of 2011)
            months = reversed(year_table.xpath("tbody/tr"))

            # Loops through all months of a year
            for month in months:
                name = month.xpath('td[@class="date"]/text()')[0]

                # Breaks if the year is 2011 and the month is after July
                # The dataset should correlate with the dataset as provided on AWS:
                #   https://aws.amazon.com/datasets/apache-software-foundation-public-mail-archives/
                # The Amazon dataset does not regard files between July 12 and August 1st, but for simplicity sake we did also include these files
                if (
                    name == "Aug 2011"
                    or name == "Sep 2011"
                    or name == "Oct 2011"
                    or name == "Nov 2011"
                    or name == "Dec 2011"
                ):
                    break

                # Prins the name of the month to show the user the progress (the system works in order)
                print(name)

                # Finds the link to a webpage containing all java-user emails of the Apache Lucene mailing list from a specific month
                link = month.xpath('td[@class="links"]/span/a/@href')[0]
                month_link = link.split("/")[0]

                # The links to a webpage containing the emails of a specific month
                thread_url = url + link
                message_page = requests.get(thread_url)
                message_page_root = html.fromstring(message_page.content)

                # The messages are featured in sections of 50 emails per page (so we need to crawl all of these sections to get all emails in a month)
                page_identifiers = list(
                    range(
                        0,
                        len(
                            message_page_root.xpath(
                                '//table[@id="msglist"]/thead/tr/th[@class="pages"]/a/text()'
                            )
                        ),
                    )
                )
                page_identifiers = ["?" + str(x) for x in page_identifiers]

                # If the total number of emails within a month is lower than 50 (and thus there is only a single section)
                if page_identifiers == []:
                    page_identifiers = [""]

                # Loops through all 50-email sections on an emails-per-month page
                for id in page_identifiers:

                    # Finds the right link
                    new_url = thread_url + id
                    new_message_page = requests.get(new_url)
                    new_message_page_root = html.fromstring(
                        new_message_page.content.decode("utf-8", "ignore").encode(
                            "utf-8"
                        )
                    )
                    emails = new_message_page_root.xpath(
                        '//table[@id="msglist"]/tbody/tr'
                    )

                    # Logs the number of emails in a single email section
                    emails_per_page = 0

                    # Loops through all emails features in a single email section
                    for email in emails:
                        email_path = email.xpath('td[@class="subject"]/a/@href')

                        # If the email_path is not empty
                        #   (some emails are not archived and so only the name of the email is mentioned without the actual email)
                        # We decided this disregard these emails
                        if not email_path == []:

                            # Finds information of a single email on a webpage, in this case:
                            # - The path to the webpage displaying said email
                            # - The author of said email
                            email_path = email_path[0]
                            author = str(
                                email.xpath('td[@class="author"]/text()')[0]
                            ).replace("/", "-")

                            path_to_directory = os.path.join(
                                os.getcwd(), "Datasets", "ApacheLucene-java-user"
                            )

                            # The crawled ApacheLucene-java-user dataset is subdivided by the authors of specific emails (such as the ENRON dataset)
                            # It is useful to note that the amount of different authors (and authors spelling their name otherwise)
                            #   is much higher than the ENRON dataset
                            # And thus the amount of emails per author is much lower
                            folder_name = os.path.join(path_to_directory, author)

                            # If the author folder does not exist already we create a new folder
                            if not author in os.listdir(path_to_directory):
                                try:
                                    os.mkdir(folder_name)
                                    os.mkdir(os.path.join(folder_name, "mbox"))
                                except OSError as e:
                                    print(e)

                            # Some characters are escaped in the file name, these characters correspond with URL-encoded characters
                            email_name = (
                                email_path.replace("/", "-")
                                .replace("%3c", "")
                                .replace("%3e", "")
                            )

                            # If the email was not already present in the dataset we add it to the {{ author }}/mbox folder
                            if email_name not in os.listdir(
                                os.path.join(folder_name, "mbox")
                            ):

                                # Adds specific email data to the email file accordingly
                                email_url = url + month_link + "/" + email_path
                                email_page = requests.get(email_url)
                                email_root = html.fromstring(
                                    email_page.content.decode("utf-8", "ignore").encode(
                                        "utf-8"
                                    )
                                )
                                email_table = email_root.xpath(
                                    '//table[@id="msgview"]'
                                )[0]
                                date = email_table.xpath(
                                    'tbody/tr[@class="date"]/td[@class="right"]/text()'
                                )[0].split(" ")
                                date_num = int(date[1])
                                date_month = date[2]
                                date_year = int(date[3])

                                sender = email_table.xpath(
                                    'tbody/tr[@class="from"]/td[@class="right"]/text()'
                                )[0]
                                subject = email_table.xpath(
                                    'tbody/tr[@class="subject"]/td[@class="right"]/text()'
                                )[0]
                                contents = email_table.xpath(
                                    'tbody/tr[@class="contents"]/td/pre/text()'
                                )[0]

                                date_formatted = (
                                    str(date_num)
                                    + " "
                                    + date_month
                                    + " "
                                    + str(date_year)
                                )

                                file_path = os.path.join(
                                    path_to_directory,
                                    author,
                                    "mbox",
                                    email_name + ".txt",
                                )
                                f = open(file_path, "w")
                                f.writelines(
                                    [
                                        "FROM: " + str(sender) + "\n",
                                        "SUBJECT: " + str(subject) + "\n",
                                        "DATE: " + date_formatted + "\n",
                                        contents,
                                    ]
                                )
                                f.close()

    print("Finished")


main()
