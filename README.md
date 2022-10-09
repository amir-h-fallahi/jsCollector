# jsCollector
The jsCollector is a python script to extract JS files from a html file.

---

### Installation
```
git clone https://github.com/amir-h-fallahi/jsCollector.git 
cd jsCollector
pip3 install -r requirements.txt
chmod +x jsCollector.py
./jsCollector.py -h
```

### Usage
Fetch JS files from a URL
```sh
./jsCollector.py -u https://example.com
```
Also multiple URLs
```sh
./jsCollector.py -u https://example.com/index.html,https://example.com/admin.html
```
Pass html file as an argument
```sh
./jsCollector.py -f index.html
```
Pass html file as stdin
```sh
cat index.html | ./jsCollector.py
```

### Features
* Extract link tags 
```html
<link rel="prefetch" href='https://example.com/prefetch.js'>
```
* Extract Script tags
```html
<script src=https://example.com/js/index.js></script>
```
* Extract All Urls (even in the comment or out of the HTML context)
```html
<!-- <script src='https://example.com/js/admin-73eL43n.js'></script> -->
```
* Convert relative urls to absolute => if possible


Test the jsCollector tool with `test.html` file (that exists in the repo)
```sh
cd jsCollector
cat test.html | ./jsCollector.py
```
---
