# iatp: Internet Archive title page adjuster

## Overview

This is a simple Python 3 script to adjust the title page of a text document uploaded to the Internet Archive.

It just does the following:

- Downloads a `scandata.xml` file from an IA item.
- Modifies the XML, updating the `pageType` of a specified page to "Title" and removing the "Title" anywhere else.
- Uploads the XML file, replacing the old one.
- (Hopefully) cleans up the XML temp files.

## Discussion 

In my work, I upload a lot of items to the [Internet Archive](https://archive.org), mostly digitized books and government documents. The IA has [robust APIs](https://archive.org/services/docs/api/index.html), useful [tools](https://github.com/jjjake/internetarchive), and is generally a fantastic website to work with. 

One minor frustration, though, is the way that the IA's algorithms attempt to automatically generate thumbnails and identify title pages for uploaded texts. Founder Brewster Kahle recently wrote a blog post[[1](https://blog.archive.org/2019/01/05/helping-us-judge-a-book-by-its-cover-software-help-request/)] casting about for ways to improve the analysis of book covers. I don't have any ideas to help out there, but I do wish there were a better way to assert the desired title page of an uploaded text.

I found an archive.org discussion post[[2](https://archive.org/post/1010270/pdf-not-starting-on-page-1)] describing how this detection works, and the manual work-around for updating title pages is to use the method I've listed at the top. 

I wrote this code in order to make that process less tedious.

## Using this script

### Requirements

You will need to be an item administrator to make this change. I am using the [internetarchive](https://github.com/jjjake/internetarchive) library to handle downloads and uploads, so I am assuming that it is installed, and that you have logged in with your IA credentials (directions are in the `internetarchive` [documentation](https://archive.org/services/docs/api/internetarchive/quickstart.html#configuring).)

### Running from the command line

You can run this in a command line to modify items one by one. For example, if you want to modify _sampleitem_ and assert that its title page should be 6, you can enter:

```
> python iatp.py sampleitem 6
```

If it works, your results will be like this:
```
sampleitem: d- success
Generated new scandata.xml file and uploading...
Success!
```

### Using the script

For bulk work, you can work within Python, importing or copying my code:

```python
>>> assert_title_page(sampleitem, 6)
```

The assert_title_page function doesn't handle directories or file cleanup. The underlying `internetarchive` item download command will create a new directory for every identifier.

The existing download command also allows for a silent=True parameter to suppress the printed-out download information. You can pass that through in my command, too:

```python
>>> assert_title_page(sampleitem, 6, silent=True)
```

### Considerations

- Uploading a new `scandata` file should prompt a derive process on the item, after which the new title page (and thumbnail) will take effect.
- The asserted page numbers are technically _leaf_ numbers (and listed as such in the XML), and they start with zero. In general, for left-to-right texts, odd numbers are on the left (verso) side and even numbers are the right (recto), the opposite of standard page numbers. A title page is thus likely to be an even leaf number for this purpose.
- There is no guarantee that the Internet Archive won't change their architecture at any point to render this ineffectual.
- I'm not directly trying to update thumbnails, just the title pages. However, it seems like the thumbnails are generally re-derived from this process, too. 
- This has only been tested on my Windows work PC using Python 3.7.0. 

Feel free to adapt, suggest additional ideas, or otherwise be in touch.





