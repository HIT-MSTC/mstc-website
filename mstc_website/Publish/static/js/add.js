function showform () {
	var a = document.getElementById('Switch');
	var b = document.getElementById('infoform');
	var c = document.getElementById('hasform');
	if (a.getAttribute("data-s") == "off") {
		a.innerHTML="关闭报名";
		a.setAttribute("data-s","on");
		b.hidden = !b.hidden;
		c.setAttribute("value","True");
	}else{
		a.setAttribute("data-s","off");
		a.innerHTML="开启报名";
		b.hidden = !b.hidden;
		c.setAttribute("value","False");
	};
}

function showname () {
	var c = document.getElementById('needother');
	var d = document.getElementById('showother');
	if (c.checked) 
	{
		d.hidden = !d.hidden;
	}
	else
	{
		d.hidden = true;
	};
}
