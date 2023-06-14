from ftplib import FTP
import PyPDF2 as pdf
import fpdf
import elgamal


class Sender:
    def __init__(self, public_key):
        """
        Initializes a new Sender instance.

        Args:
            public_key (tuple(int)): The public key sent by the receiver. It consists of a tuple of integers.
        """
        self.public_key = public_key

    def read_pdf(self, filename):
        """
        Reads the original pdf content.

        Args:
            filename (str): The name of the original pdf to be encrypted. Include the file extension ("file.pdf")
        Returns:
            Text extracted from the pdf file
        """
        text = str()
        reader = pdf.PdfReader(filename)
        for x in reader.pages:
            text += x.extract_text()
        return text

    def file_encryption(self, text):
        """
        Encrypts the extracted text from the file. It works for any text though.

        Args:
            text (str): Text to be encrypted
        Returns:
            Text encrypted
        """
        return elgamal.encrypt(text, self.public_key)

    def export_encrypted_file(self, ciphertext, **kwargs):
        """
        Creates the new pdf with the encrypted text.

        Args:
            ciphertext (str): The ciphertext to be written to the PDF file.
            **kwargs: Keyword arguments.
            **filename (str, optional): The filename of the PDF file to be generated. Defaults to "output.pdf".
            **white_text (bool, optional): Whether to write the ciphertext in white color. Defaults to False.
            **with_password (bool, optional): Whether to save the PDF file with a password. Defaults to False.

        Returns:
            None.

        Raises:
            Exception: If an error occurs.
        """
        try:
            if "filename" in kwargs:
                filename = kwargs.get("filename")
            else:
                filename = "output.pdf"
            new_pdf = fpdf.FPDF(format="letter")
            new_pdf.add_page()
            if "white_text" in kwargs and kwargs.get("white_text"):
                new_pdf.set_fill_color(255, 255, 255)
                new_pdf.set_text_color(255, 255, 255)
            new_pdf.set_font("Arial", size=2)
            new_pdf.multi_cell(200, 10, str(ciphertext))
            new_pdf.output(filename)
            if "with_password" in kwargs and kwargs.get("with_password"):
                writer = pdf.PdfWriter()
                with open(filename, 'rb') as file:
                    generated = pdf.PdfReader(file)
                    for page_num in range(len(generated.pages)):
                        writer.add_page(generated.pages[page_num])
                writer.encrypt(str(self.public_key))
                with open(filename, 'wb') as output_file:
                    writer.write(output_file)
        except:
            print("Something went wrong. Check parameters and processed text")

    def send_file(self, hostname, username, password, filename, remote_directory):
        try:
            ftp = FTP(hostname)
            ftp.login(username, password)
            ftp.cwd(remote_directory)
            with open(filename, 'rb') as file:
                ftp.storbinary('STOR ' + filename, file)
            ftp.quit()
            print("File uploaded successfully!")
        except Exception as e:
            print("An error occurred:", str(e))


    """# Example usage
    hostname = 'ftp.example.com'
    username = 'your_username'
    password = 'your_password'
    file_path = 'path_to_local_file/file.txt'
    remote_directory = '/path/to/remote/directory'

    upload_file_ftp(hostname, username, password, file_path, remote_directory)"""
