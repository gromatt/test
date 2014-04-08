

function generate_conditions_html()
{
	$.ajax({url:"get_conditions_html",success:function(result)
	{
    	$("div#conditions").html(result);
  	}});
}

function generate_form_add_condition()
{
	$.ajax({url:"get_add_condition_form",success:function(result)
	{
		$("div#ecran_gris").css("display", "block");

    	$("div#add_condition").html(result);

    	$("div#add_condition").css("display", "block");
  	}});
}

function make_disappear_form_add_condition()
{
	$("div#ecran_gris").css("display", "none");

    $("div#add_condition").css("display", "none");
}

function add_condition()
{
    var attr_sel = $("select#attribute")[0];
    var attribute = attr_sel.value;

    var bf_sel = $("select#boolean_function")[0];
    var boolean_function = bf_sel.value;

    var arg_sel = $("input#condition_argument")[0];
    var argument = arg_sel.value;

    $.ajax({url:"add_condition/" + attribute + "/" + boolean_function + "/" + argument,success:function(result)
	{
		generate_conditions_html();

		make_disappear_form_add_condition();
	}});
}