# -*- coding: utf-8 -*-
'''
A quick script that will:
    - download a scandata.xml file
    - copy to a new file and change the designated title page (if necessary)
    - delete the scandata online
    - upload the new scandata
    - cleanup after itself

Requires that the user have permission to edit the item online

Uses the existing internetarchive tool at https://github.com/jjjake/internetarchive

To use this as a command-line python script, run like this to assert that
you want sampleidentifier to have page 2 as its title page:
    
    > python iatp.py sampleidentifier 2

'''

import sys
import internetarchive as ia
import os
from shutil import rmtree
from tempfile import mkdtemp


def assert_title_page(identifier, titlepage, silent=False):
    tp = str(titlepage)
    result = list()
    # first download scandata.xml file from the item
    try:
        item = ia.get_item(identifier)
    except:
        raise('IA identifier not found.')
    scandata = identifier + '_scandata.xml'
    for f in item.files:
        if f['name'] == scandata:
            ia.download(identifier, files=scandata, silent=silent)
            with open(os.path.join(identifier, scandata), 'r') as fh:
                xml = fh.read()
                nochange = True
                match = False
                final = list()
                for line in xml.splitlines():
                    newline = line
                    if 'leafNum' in line:  # like: <page leafNum="0">
                        leafnum = line.split('"')[1]
                        if leafnum == tp:
                            match = True
                    if 'pageType' in line:  # like: <pageType>Normal</pageType>
                        if match is True:
                            if 'Title' in line:
                                result.append('Title page is already declared.')
                            else:
                                newline = line.replace('Normal', 'Title')
                                nochange = False
                            match = False  # don't match in the rest of this document
                        elif 'Title' in line:  # erroneous title page from IA
                            newline = line.replace('Title', 'Normal')
                            nochange = False
                    final.append(newline)
            if nochange is True:
                result.append('No changes detected.')
            else:
                with open(os.path.join(identifier, scandata), 'w') as fh:
                    fh.write('\n'.join(final))
                    result.append('Generated new scandata.xml file and uploading...')
                ia.upload(identifier, files=[os.path.join(identifier, scandata)])
                result.append('Success!')
            rmtree(identifier)
    return '\n'.join(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        identifier = sys.argv[1]
        titlepage = sys.argv[2]
        d = mkdtemp()
        os.chdir(d)
        print(assert_title_page(identifier, titlepage))
        rmtree(d, ignore_errors=True)

