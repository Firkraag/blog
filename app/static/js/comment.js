//$("#writeComment").submit(function(event) {
//	event.preventDefault();
//	var $form = $( this ),
//	dest = $form.attr('action');
//	var posting = $.post(dest, {nickname: $('#nickname').val(), url: $('#url').val(), email: $('#email').val(), content: $('#content').value, blog_id: $('#blog_id').name});
//	posting.done(function(data) {
//			alert(data.avatar);
//        	alert(data.nickname);
//        	alert(data.url);
//        	alert(data.email);
//        	alert(data.content);
//	})
//})

function submitComment(event) {
    var nickname = document.getElementById("nickname").value;
    var url = document.getElementById("url").value;
    var email = document.getElementById("email").value;
    var content = document.getElementById("content").value;
    var blog_id = document.getElementById("blog_id").name;
    var params = 'nickname=' + nickname + '&' + 'url=' + url + '&' + 'email=' + email + '&' + 'content=' + content + '&' + 'blog_id=' + blog_id;
    var http = new XMLHttpRequest();
    http.open("POST", '/comment', true);

	//Send the proper header information along with the request
	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	http.onreadystatechange = function() {//Call a function when the state changes.
    	if(http.readyState == 4 && http.status == 200) {
        	var info = JSON.parse(http.responseText);
        	alert(info.avatar);
        	alert(info.nickname);
        	alert(info.url);
        	alert(info.email);
        	alert(info.content);
    	}
	}
};

