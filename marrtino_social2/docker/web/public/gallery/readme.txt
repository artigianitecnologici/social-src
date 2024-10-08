Free PHP Gallery by TNTcode.com
=============================== 

- unzip all files from this zip
- edit settings.php file and set your own admin username / password
- upload the files on your server using a FTP program or Adobe Dreamweaver, etc
- access the folder in your browser, e.g www.Example.com/gallery/ 
- you can now click "admin" at the bottom of the page and enter your user/password
- on the admin page you can create 1-2 categories
- visit the gallery main page again, click the categories and then the "Upload photos" button


No database is required for this script, the categories that you create are actual folders on servers, and the name of your photos is taken from the jpg file name.


New in version 1.0.4
====================
	- in settings.php added variable $settings_max_upload_file_size_mb in order to control maximum uploaded photo size
	- on category page > upload form it now shows the upload limits from settings.php and upload limits from php.ini
	- added a "B" flag in 2 of the .htaccess rules, see the note at the end of this file and end of .htaccess file
	
	
New in version 1.0.1
====================

	- you can now use special characters in category names and photo names, if you notice problems please contact us
	- you can upoad multiple photos by FTP and then go to "admin > regenerate images" in order to create thumbnails for them

	- note: the new file name of each photo file was changed like this: landscape.jpg, landscape_small.jpg and landscape_thumb.jpg; names like landscape_source.jpg are no longer used


Known problems:
=============== 

1) The url rewrite doesn't work, e.g /gallery/login shows error but /gallery/login.php works ok
Solution: make sure on server you have the .htaccess in the gallery folder, open .htaccess file and uncomment this line:
RewriteBase /gallery
Replace the path /gallery with your own path if needed

2) Change sorting of photos or categories
Open system_header.php and look for these two: 
	krsort($categories_array[$folder]);
	ksort($categories_array);

See the comments above them on how to change sorting, first one sorts photos inside categories and the second one sorts the list of categories

3) Some servers had problems processing category names that contains spaces or other special characters
to fix this, a "B" flag was added in 2 rules of the .htaccess file [QSA] becoming [B,QSA]
if you click a category name and it returns "page not found", try removing the "B," in .htaccess rules

	Apache reference on B flag: https://httpd.apache.org/docs/2.4/rewrite/flags.html#flag_b


If you need any help contact us at https://www.tntcode.com/contact/ 