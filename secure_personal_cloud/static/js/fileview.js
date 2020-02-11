//alert("yo")
var key;
for(var i = 0; i < filepaths.length; i++)
{
	if(filepaths[i][0] != '/') filepaths[i] = '/' + filepaths[i];
};
var currentpath = '/';
var input = document.getElementById("search");
input.addEventListener("keydown", function (e) {
	if (e.keyCode === 13) {  //checks whether the pressed key is "Enter"
		pathmannual();
	}
});
var table = document.getElementById("files");
const sleep = (milliseconds) => {
	return new Promise(resolve => setTimeout(resolve, milliseconds));
};
function fileViewRender(){
	document.getElementById("loader").style.display = "block";
	document.getElementById("files").style.display = "none";
	sleep(200).then(() => {
		var currentfiles = [];
		var currentfilepaths = [];
		document.getElementById("path").innerHTML = "Current Folder: " + currentpath;
		$('input[name=search]').val(currentpath);
		for (var i = 0; i < filepaths.length; i++) {
			var str = filepaths[i];
			if(str == currentpath) {
				currentfiles.push(i);
				currentfilepaths.push('/');
				continue;
			};
			var substr = str.slice(0, currentpath.length);
			if(substr == currentpath){
				var relpath = str.slice(currentpath.length, );
				currentfiles.push(i);
				if(relpath[0] != '/') relpath = '/' + relpath;
				currentfilepaths.push(relpath);
			};
		};

		var currentview = [];
		var currentviewtype = [];
		for (var i = 0; i < currentfiles.length; i++){
			var str = currentfilepaths[i];
			if(str == '/'){
				currentview.push(currentfiles[i]);
				currentviewtype.push('file');
				continue;
			} else{
				str = str.slice(1, );
				var dirname = str.split('/')[0];
				if(currentview.includes(dirname) == false){
					currentview.push(dirname);
					currentviewtype.push('dir');
				};
			};
		};
		var file = React.createClass({
			displayName: "file",

			render: function render() {
				var index = this.props.children;
				var image = "/static/images/small/" + iconpaths(index) + '.png';
				return React.createElement(
					"div",
					{ className: "fileview" },
					React.createElement("input", { type: "image", src: image, height: '100px', onClick: function onClick() {return fileInfo(index)} }),
					React.createElement(
						"div",
						{ style: {"textAlign":"center"} },
						// compress(filenames[index])
						compress(filenames[index])
					),
					"\xA0 \xA0"
				);
			}
		});

		var folder = React.createClass({
			displayName: "folder",

			render: function render() {
				var path = this.props.children;
				return React.createElement(
					"div",
					{ className: "dirview" },
					React.createElement("input", { type: "image", src: "/static/images/folder.png", height: '100px', onClick: function onClick() {return changepath(path);} }),
					React.createElement(
						"div",
						{ style: {"textAlign":"center"} },
						compress(path)
					),
					"\xA0 \xA0"
				);
			}
		});
		var num = currentview.length;
		for (var i = 0; i < num; i++) {
			var s = table.rows.length;
			if(s != 0){
				var width = window.innerWidth;
				var cellwidth = 1550/7;
				var n = Math.floor(width/cellwidth);
				if(n == 0) n = 1;
				if(table.rows[s-1].cells.length < n) var row = table.rows[s-1];
				else var row = table.insertRow(-1);
			} else var row = table.insertRow(-1);
			var cell = row.insertCell(-1); 
			if (currentviewtype[i] == 'file') {
				var name = filenames[currentview[i]];
				var index = currentview[i];
				ReactDOM.render(React.createElement(
					file,
					null,
					// name
					index
				), cell);
			} else {
				var name = currentview[i];
				ReactDOM.render(React.createElement(
					folder,
					null,
					name
					// i
				), cell);
			};
		};
		document.getElementById("loader").style.display = "none";
		document.getElementById("files").style.display = "block";
		})
};

function changepath(path){
	var info = document.getElementById("info");
	$('#info').empty();
	document.getElementById('closeinfo').style.display = 'none';
	info.style.height = 0;
	info.className = "null";
	if(currentpath[currentpath.length - 1] != '/') currentpath = currentpath + '/';
	currentpath = currentpath + path;
	$("table").empty();
	fileViewRender();
};

function goback(){
	var info = document.getElementById("info");
	$('#info').empty();
	document.getElementById('closeinfo').style.display = 'none';
	info.style.height = 0;
	info.className = "null";
	if(currentpath != '/'){
		if(currentpath[currentpath.length - 1] == '/') currentpath = currentpath.slice(0, currentpath.length - 1);
		arr = currentpath.split('/');
		arr.pop();
		currentpath = arr.join('/') + '/';
	};
	$("table").empty();
	fileViewRender();
};

function pathinput(){
	if(document.getElementById("inputpath").style.display === "block") {
		document.getElementById("inputpath").style.display ="none";
		document.getElementById("closeinfo").style.top = '292px';
	} else {
		document.getElementById("inputpath").style.display = "block";
		document.getElementById("closeinfo").style.top = '362px';
	};
};

function pathmannual(){
	var info = document.getElementById("info");
	$('#info').empty();
	document.getElementById('closeinfo').style.display = 'none';
	info.style.height = 0;
	info.className = "null";
	var str = $('input[name=search]').val();
	if(str[0] != '/') str = '/' + str;
	if(str[str.length - 1] != '/') str = str + '/';
	currentpath = str;
	$("table").empty();
	fileViewRender();
};

function compress(str){
	if(str.length <= 15) return str;
	else return (str.slice(0,15) + "...");
};

function fileInfo(index){
	var container = document.getElementById("info");
	container.className = "info";
	var name = filenames[index];
	var time = uploadtime[index];
	var size = filesize[index];
	var md5 = md5sum[index];
	var enc = 'AES ' + 'encrypted';
	var info = React.createClass({
		displayName: "info",
		render: function render() {
			var image = '/static/images/large/' + iconpathslarge(index) + '.png'; 
			return React.createElement(
					"div",
					{ id: "fade", style: {'height': '500px', 'width': '100%', 'backgroundColor': '#ccc', 'top': '0', 'opacity':'0'} },
					React.createElement(
							"div",
							{ style: {'left':'10%', 'top': '70px', 'position': 'relative', 'float':'left'} },
							React.createElement("img", { src: image, style: {'width': '360px', 'height':'360px'} })
					),
					React.createElement(
							"div",
							{ style: {'top': '60px', 'position': 'relative', 'left': '50%', 'width': '40%', 'height': '360px'} },
							React.createElement(
									"h1",
									{ style: {'textAlign': 'left', 'marginRight': '100px'} },
									"File Details"
							),
							React.createElement(
									"div",
									{ style: {'width': '40%', 'position': 'absolute'} },
									React.createElement(
											"h3",
											null,
											"File Name:"
									),
									React.createElement(
											"h3",
											null,
											"File Size:"
									),
									React.createElement(
											"h3",
											null,
											"File Upload Time:"
									),
									React.createElement(
											"h3",
											null,
											"MD5SUM:"
									),
									React.createElement(
											"h3",
											null,
											"Encryption Status:"
									)
							),
							React.createElement(
									"div",
									{ style: {'width': '60%', 'position': 'absolute', 'top': '47px', 'left': '40%'} },
									React.createElement(
											"h3",
											null,
											name
									),
									React.createElement(
											"h3",
											null,
											"0 bytes"
									),
									React.createElement(
											"h3",
											null,
											time
									),
									React.createElement(
											"h3",
											null,
											md5
									),
									React.createElement(
											"h3",
											null,
											enc
									)
							),
							React.createElement(
									"div",
									{ style: {'position': 'absolute', 'left': '0%', 'top': '300px'} },
									React.createElement(
											"button",
											{ "className": "w3-button w3-green w3-padding-large w3-large w3-margin-top w3-hover-green download", onClick: function onClick() {return downloadfile(index);} },
											"Download ",
											React.createElement("i", { "className": "fa fa-download" })
									)
							),
							React.createElement(
									"div",
								{ style: {'position': 'absolute', 'left': '70%', 'top': '300px'} },
									React.createElement(
											"button",
											{ "className": "w3-button w3-red w3-padding-large w3-large w3-margin-top w3-hover-red", "data-toggle":"modal", "data-target":"#myModal", onClick: function onClick() {return deletefile(index);} },
											"Delete ",
											React.createElement("i", { "className": "fa fa-remove" })
									)
							)
					)
			);
		}
	});
	document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
	sleep(500).then(() => {
		var clb = document.getElementById('closeinfo');
		clb.style.display = 'block';
		ReactDOM.render(React.createElement(info, null), container);
		document.getElementById('fade').className = 'fade';
	});

};

// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
};

function closeinfo(){
	document.getElementById('fade').className = 'fadeout';
	$('#info').empty();
	document.getElementById('closeinfo').style.display = 'none';
	document.getElementById("info").className = 'infoout';
};

function keyinput(){
	if(document.getElementById('key').style.display = 'none') document.getElementById('key').style.display = 'block';
	else document.getElementById('key').style.display = 'none';
};

function closekey(){
	key = $('#keyinput').val();
	document.getElementById('key').style.display = 'none';
}
function downloadfile(index){
	if($('#keyinput').val() == ''){
		alert("Enter Encryption key:");
		document.getElementById('key').style.display = 'block';
		return;
	};
	if(encryption[index] == "AES" || true){
		try{
			var namearray = filenames[index].split('.');
			var extension = namearray[namearray.length - 1];
			var mime = mimetype[extension];
			var format = "data:" + mime + ";base64,";
			var url = filelinks[index];
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
				// Typical action to be performed when the document is ready:
				var decryptedText = sjcl.decrypt(key, xhttp.responseText);
					var uriContent = format + encodeURIComponent(decryptedText);
					var blob = new Blob([ uriContent ], {type:mime});
				var link = document.createElement("a");
					link.download = filenames[index];
					// Construct the uri
					var uri = URL.createObjectURL(blob);
					link.href = uriContent;
					document.body.appendChild(link);
					link.click();
					// Cleanup the DOM
					document.body.removeChild(link);
				//    newWindow = window.open(uriContent, 'neuesDokument');
				//    alert("opened");
				}
			};
			xhttp.open("GET", url, true);
			xhttp.send();
		} catch(err)
		{
			alert(err.message);
		}
	} else alert('wtf');
	
};

function deletefile(index){
	var url = window.location.href + "delete/" + fileids[index] + '/';
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", url, true);
	xhttp.send();
	//alert(url);
	document.location.reload();
};

function iconpaths(index){
	var name = filenames[index];
	var extarr = name.split('.');
	var ext = extarr[extarr.length-1];
	switch(ext){
		case 'png':
		case 'jpg':
		case 'jpeg':
		case 'svg':
		return 'img';
		case 'mp3':
		case 'amr':
		case 'ogg':
		case 'wav':
		case 'weba':
		return 'mp3';
		case 'mp4':
		case 'mkv':
		case 'webm':
		case 'gif':
		return 'mp4';
		case 'doc':
		case 'docx':
		return 'doc';
		case 'ppt':
		case 'pptx':
		return 'ppt';
		case 'pdf':
		return 'pdf';
		case'xls':
		case 'xlsx':
		return 'xls';
		case 'zip':
		case 'gz':
		case 'xz':
		case 'tgz':
		case 'tar':
		case 'rar':
		return 'zip';
		default:
		return 'file';

	};
};

function iconpathslarge(index){
	var name = filenames[index];
	var extarr = name.split('.');
	var ext = extarr[extarr.length-1];
	switch(ext){
		case 'png':
		case 'jpg':
		case 'jpeg':
		case 'svg':
		return 'img';
		case'js':
		return 'js';
		case 'py':
		return 'py';
		case 'html':
		return 'html';
		case 'cpp':
		return 'cpp';
		case 'c':
		return 'c';
		case 'mp3':
		case 'amr':
		case 'ogg':
		case 'wav':
		case 'weba':
		return 'mp3';
		case 'mp4':
		case 'mkv':
		case 'webm':
		case 'gif':
		return 'mp4';
		case 'doc':
		case 'docx':
		return 'doc';
		case 'ppt':
		case 'pptx':
		return 'ppt';
		case 'pdf':
		return 'pdf';
		case'xls':
		case 'xlsx':
		return 'xls';
		case 'zip':
		case 'gz':
		case 'xz':
		case 'tgz':
		case 'tar':
		case 'rar':
		return 'zip';
		default:
		return 'file';

	};
};

fileViewRender();