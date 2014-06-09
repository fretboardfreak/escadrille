Site Update: the first
======================

:date: 2014-06-08 11:30
:category: blog
:tags: site
:summary: It has been about a week now and a bunch of little changes have occurred on the site. I can't itemize them all but I can talk about what I'm working on. Most of the changes that I have been making are focused on tweaking the appearance of the site and the behavior of the scripts that I have.

The appearance tweaks are the hardest to itemize. I've added the summary sections of articles to the article template. This makes the summary metadata field double as the first paragraph of the article. I've also removed the comments section on most pages.  I wanted to just turn off comments for now but I was lazy and didn't check every template.

Speaking of templates I have a whole new set of them now, along with the rest of the pelican theme. By that I mean that I have swapped the notmyidea theme with the bootstrap theme in the pelican-theme repository.  To the sidebar I added a thumbnail and a tagline for the site. The tagline matches the newly changed site title, "Quizzical Silicon".

I'll provide a page of links for everything eventually.

To the repository I added my fret repo as a submodule. At first I tried to symlink files in selectively but the NTFS and FAT32 filesystem don't play nicely with symlinks. So instead I opted for an automated preprocessor approach.  I wrote a bash script that executes task scripts stored in a subdirectory and integrated that into the makefile. Then I wrote a task script that reads a file listing other files to copy into the content directory.  This lets me store some things in my fret repo and pull them into the blog repo through the git submodule.  I also had to update the site update script to update the git submodule too. Then, because I'm a goof, I added a cleanup script that cleans it all up, even the files cookies by the link_avoider script.

For the future I have a bunch of things planned. For instance one of my first goals is to put together a bunch of image galleries to showcase all of my pictures and give me a reason to take more of them. So far I'm happy with the way things are shaping up.
