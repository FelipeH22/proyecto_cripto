import ast
from ftplib import FTP

import PyPDF2 as pdf
import fpdf

import elgamal


class Receiver:
    def __init__(self, **kwargs):
        """
        Initializes a new Receiver instance.

        Args:
            **kwargs: Keyword arguments.

            * generation (bool): Whether to generate a new public/private key pair. If no needed, set to False or do not include it.
            * public_key (tuple(int)): If a public key was obtained before is passed here, in this case, private_key is mandatory.
            * private_key (int): The private key.

        Raises:
            ValueError: If generation is false and public_key and private_key are not provided.
        """
        if "generation" in kwargs and kwargs.get("generation"):
            self.public_key, self.private_key = self.generate_keys()
        elif "public_key" in kwargs and "private_key" in kwargs:
            self.public_key = kwargs.get("public_key")
            self.private_key = kwargs.get("private_key")
        else:
            raise ValueError("Since generation flag is false, public_key and private_key are mandatory parameters")

    def decrypt_file(self, filename):
        """
        Decrypts an already existent pdf file.

        Args:
            filename (str): The name of the pdf file to decrypt. Include the extension ("filename.pdf")
        """

        def read_pdf(filename):
            text = str()
            reader = pdf.PdfReader(filename)
            for x in reader.pages:
                text += x.extract_text()
            return text

        plaintext = elgamal.decrypt(ast.literal_eval(read_pdf(filename)), self.public_key, self.private_key)
        new_pdf = fpdf.FPDF()
        new_pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)
        new_pdf.add_page()
        new_pdf.set_font("Arial", size=9)
        new_pdf.multi_cell(200, 10, str(plaintext))
        new_pdf.output("decrypted.pdf")

    def generate_keys(self):
        return elgamal.generate_key()

    def download_file_ftp(self, hostname, username, password, remote_file_path, filename):
        try:
            ftp = FTP(hostname)
            ftp.login(username, password)
            remote_directory = remote_file_path.rsplit('/', 1)[0]
            ftp.cwd(remote_directory)
            with open(filename, 'wb') as file:
                ftp.retrbinary('RETR ' + filename, file.write)
            ftp.quit()
            print("File downloaded successfully!")
        except Exception as e:
            print("An error occurred:", str(e))
