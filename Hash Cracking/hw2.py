#!/usr/bin/env python3

import hashlib, os, sys

yahooPlainTextPassArray = []
linkedinHashes = []             # list of the linkedin password hashes given to us by instructor
formspringHashes = set()
rockyouSet = set()

def createLinkedinSolvedFile():
    """ This method is designed to iterate through the 10,000 most common passwords list found from wikipedia,
    hash them, as well as mask them, and see if they match up to any of the hashes from the linkedin hashed passwords list.
    
    This was done by first copy and pasting the top 10,000 most common passwords from wikipedia,
    (https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords).
    
    I iterated through them all and hashed them through SHA1 (which was an obvious guess from the text file name (SHA1.txt) from the linkedin folder),
    then the hashed value was also masked as I observed most of them had five 0s at the beginning of each hash.
    
    Each of the masked and unmasked hashes were then compared to see if they were in the linkedin hashed passwords list.
    If they were, they then were appended to the linkedinSolved text file.
    """
  
    with open("linkedInSolved.txt", 'w') as linkedInTextFile: #creates a text file for the solved passwords and hashes to be written (appended and not overwritten) to
        with open("MostCommonPasswords.txt", 'r') as passwordList:
            solvedPassCount = 0
            for line in passwordList:
                if solvedPassCount == 100:                  # This allows the function to stop at the limit that the instructor has stated to set
                    break
                hashedpass = sha1Hash(line.strip())         # Hashes each word from the unique password list and returns the hash
                maskedpass = maskedHashedPass(hashedpass)   # Masks each of the hashes to see if they can be compared to any from the hashed linkedin list
                if maskedpass in linkedinHashes:    # Checks to see if the hashed plaintext password is in the known hashed passwords list
                    solvedPassCount+=1
                    string = "{} {}".format(hashedpass, line)
                    linkedInTextFile.write(string)    
              
                    
def sha1Hash(password):
    bytestring = password.encode()
    plainPassword = hashlib.sha1(bytestring)
    hashedPassword = plainPassword.hexdigest()
    return hashedPassword

def maskedHashedPass(hashedpass):
    """This function masks the hashed passes the same way as a lot of the hashes are
    from the linkedin hashed passwords file so that they can also be recognized"""
    
    hashedpassList = list(hashedpass)
    for i in range(0,5):
        hashedpassList[i]='0'
    maskedpass = "".join(hashedpassList)
    return maskedpass

def createFormspringSolvedFile():
    saltedSha256Hash()


def saltedSha256Hash():
    
    """This function iterates through the set of rockyou text passwords, salts them (iterating through 00-99), and converts them to SHA256 hashes,
        which is then compared to the set of hashes found from the formspring hashed passwords file."""
    with open("SolvedFormspringList.txt", 'w') as solvedList:
        count1 = 0
        for i in range(0,100):
            salt = str(i).zfill(2)
            for password in rockyouSet:
                passwordString = str(password)
                saltedPassword = salt + password
                bytestring = saltedPassword.encode()
                hashedPassword = hashlib.sha256(bytestring).hexdigest()
                if hashedPassword in formspringHashes:      # hashed salted passwords are compared to the set of hashes in the formspring hashed passwords set
                    if count1 == 100:
                        sys.exit(0)                         # stops program at 100 found passwords as this is the last method to run
                    string = '{} {}\n'.format(hashedPassword, passwordString)
                    solvedList.write(string)
                    count1+=1

    
def main():
    
    # Following 8 lines of code create a unique password list from the yahoo file as well as appending to a list of the unique passwords
    with open("yahooSolvedUnique.txt", 'w') as uniquePassList:
        with open("yahoo.txt", 'r') as plainTextFile:       #formatted file so that it only contains the lines with the IDs, emails, and passwords
            for line in plainTextFile:
                if len(yahooPlainTextPassArray) == 100:
                    break
                legitChecker = list(line)
                if legitChecker.count(':') == 2:
                    textArray = "".join(legitChecker).split(':')   #as the file explains, the ID, email, and password was separated by the colon delimiter, allows us to pluck the password out simply using the split method
                    if textArray[2] not in yahooPlainTextPassArray:
                        yahooPlainTextPassArray.append(textArray[2])
                        uniquePassList.write(textArray[2])

    
    #Creates a list of the hashes for quick access to the hashes from the linkedin file
    with open("linkedinPassFile.txt", 'r') as linkedinFile:
        for line in linkedinFile:
            linkedinHashes.append(line.strip())
                
    #Creates a set of the hashes for quick access to the hashes from the formspring file
    with open("formspring.txt", 'r') as formspringFile:
        for line in formspringFile:
            formspringHashes.add(line.strip())
            
    #Creates a set of all the words in the rockyou text file
    with open("rockyou.txt", 'r', encoding = 'utf-8') as rockyou:
        for line in rockyou:
            rockyouSet.add(line.strip())
    
    createLinkedinSolvedFile()
    createFormspringSolvedFile()
    
if __name__ == '__main__': main()