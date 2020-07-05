# Imports TestCase class of unittest library
from unittest import TestCase

# Imports os library to access files on the Operating System
import os

# Imports WordExtractor
from ikk.word_extraction import WordExtractor

# TestCase TestWordExtractor tests methods in class WordExtractor
class TestWordExtractor(TestCase):

    # Method setUp initializes a WordExtractor class
    def setUp(self):
        self.extractor = WordExtractor()

    # Method test_remove_header_ENRON tests the removal of the header of emails in the ENRON corpus using
    #   the remove_header_ENRON method in word_extraction.py
    def test_remove_header_ENRON(self):
        enron_file_lines = [
            "Message-ID: <18782981.1075855378110.JavaMail.evans@thyme>\n",
            "Date: Mon, 14 May 2001 16:39:00 -0700 (PDT)\n",
            "From: phillip.allen@enron.com\n",
            "To: tim.belden@enron.com\n",
            "Subject: Mime-Version: 1.0\n",
            "Content-Type: text/plain; charset=us-ascii\n",
            "Content-Transfer-Encoding: 7bit\n",
            "X-From: Phillip K Allen\n",
            "X-To: Tim Belden <Tim Belden/Enron@EnronXGate>\n",
            "X-cc:\n",
            "X-bcc:\n",
            "X-Folder: \Phillip_Allen_Jan2002_1\Allen, Phillip K.'Sent Mail\n",
            "X-Origin: Allen-P\n",
            "X-FileName: pallen (Non-Privileged).pst\n",
            "\n",
            "Here is our forecast\n",
            "\n",
            " ",
        ]
        ENRON_result = self.extractor.remove_header_ENRON(enron_file_lines)
        self.assertEqual(ENRON_result, "\nHere is our forecast\n\n ")
        return ENRON_result

    # Method test_remove_header_and_footer_Apache tests the removal of the header and footer of emails in the Apache corpus using
    #   the remove_header_and_footer_Apache method in word_extraction.py
    def test_remove_header_and_footer_Apache(self):
        apache_file_lines = [
            "FROM: Dan <lue...@gmail.com>\n",
            "SUBJECT: NIOFSDirectory AssertionError in sun.nio.ch.NativeThreadSet\n",
            "DATE: 6 Dec 2009\n",
            "\n",
            "Hello,\n",
            "\n",
            "Do I have any other options?\n",
            "\n",
            "Thanks,\n",
            "Dan\n",
            "--\n",
            "View this message in context: http://www.nabble.com/LUCENE-1282-tp18224180p18224180.html\n",
            "Sent from the Lucene - Java Users mailing list archive at Nabble.com.\n",
            "\n",
            "\n",
            "---------------------------------------------------------------------\n",
            "To unsubscribe, e-mail: java-user-unsubscribe@lucene.apache.org\n",
            "For additional commands, e-mail: java-user-help@lucene.apache.org",
            "\n",
        ]

        Apache_result = self.extractor.remove_header_and_footer_Apache(
            apache_file_lines
        )
        self.assertEqual(
            Apache_result,
            "\nHello,\n\nDo I have any other options?\n\nThanks,\nDan\n--\n\n\n\n",
        )
        return Apache_result

    # Method test_extract_words tests the extraction of words using the extract_words method in word_extraction.py
    # It also tests whether extract_words raises the right Errors upon specific inputs
    def test_extract_words(self):
        ENRON_file_name = os.path.join(os.getcwd(), "test", "ENRON_test_file")
        result = self.extractor.extract_words(ENRON_file_name, dataset="ENRON")
        self.assertEqual(result, self.test_remove_header_ENRON().lower().split())
        result = self.extractor.extract_words(
            ENRON_file_name, dataset="ApacheLucene-java-user"
        )
        self.assertNotEqual(result, self.test_remove_header_ENRON().lower().split())

        Apache_file_name = os.path.join(os.getcwd(), "test", "Apache_test_file")
        result = self.extractor.extract_words(Apache_file_name, dataset="ENRON")
        self.assertNotEqual(
            result, self.test_remove_header_and_footer_Apache().lower().split()
        )
        result = self.extractor.extract_words(
            Apache_file_name, dataset="ApacheLucene-java-user"
        )
        self.assertEqual(
            result, self.test_remove_header_and_footer_Apache().lower().split()
        )

        Non_existent_file_name = os.path.join(
            os.getcwd(), "test", "test_Non_existent_file"
        )
        with self.assertRaises(ValueError):
            self.extractor.extract_words(Non_existent_file_name)

        Non_existent_dataset = "test_Non_existent_dataset"
        with self.assertRaises(ValueError):
            self.extractor.extract_words(Apache_file_name, dataset=Non_existent_dataset)

    # Method test_process_file is not implemented as the method is straightforward
    # process_file in word_extraction.py only stems words using an imported library and counts the occurrence of specific words in the file
    def test_process_file(self):
        pass
