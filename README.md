# Arhivist 

#REST-API
<p>We can get a json of all of the books.</p>

<code>http http://127.0.0.1:8000/api/books/</code>
<pre>
HTTP/1.0 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 2168
Content-Type: application/json
Date: Wed, 27 Dec 2017 14:48:38 GMT
Server: WSGIServer/0.2 CPython/3.6.2
Vary: Accept
X-Frame-Options: SAMEORIGIN
   
{
    "count": 2, 
    "next": null, 
    "previous": null, 
    "results": [
        {
            "author": [
                1
            ], 
            "canonical_volume_link": "https://books.google.com/books/about/How_to_Live_Like_You_Were_Dying_PDF.html?hl=&id=gNFcTw52DPUC", 
            "category": [
                1
            ], 
            "description": "Would I Lie to You? Not This ...", 
            "file_ext": "", 
            "id": 1, 
            "isbn_10": 976891212, 
            "isbn_13": 9780976891215, 
            "language": 1, 
            "owner": "admin", 
            "page_count": 10, 
            "path": "/home/test/", 
            "published_date": "2005-01-01", 
            "publisher": 2, 
            "raw_title": "How to Live Like You Were Dyin", 
            "thumbnail": "", 
            "title": "How to Live Like You Were Dying", 
            "validate": false
        }, 
        {
            "author": [
                2
            ], 
            "canonical_volume_link": "https://books.google.com/books/about/some.html?hl=&id=gNFcTw52DPUC", 
            "category": [
                2
            ], 
            "description": "Some descr", 
            "file_ext": "", 
            "id": 2, 
            "isbn_10": 976891222, 
            "isbn_13": 9780976891233, 
            "language": 2, 
            "owner": "admin", 
            "page_count": 10, 
            "path": "/home/test/", 
            "published_date": "2015-01-01", 
            "publisher": 1, 
            "raw_title": "Some title", 
            "thumbnail": "", 
            "title": "Some_title", 
            "validate": false
        }
    ]
}
    
</pre>
any more, so go ahead and delete that.  
Once that's done we can start refactoring our views slightly.
