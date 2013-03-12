
function add_filter()
{
	var my_table = $("table#filter_description");

	my_table.append("glouglou");
}

$(function() {
	$(".buttn").click(function(){
		alert("ok 2");
	});

	$("#my_form").submit(function(){
		var my_table = $("table#filter_description");

		my_table.append("glouglou");

		return false;
	});
});