

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

function generate_annonce_list_html()
{
    $.ajax({url:"get_annonce_list_html/",success:function(result)
    {
        $("div#annonce_list").html(result);
    }});
}

function generate_annonce_list_html_of_page(i)
{
    $.ajax({url:"get_annonce_list_html/" + i,success:function(result)
    {
        $("div#annonce_list").html(result);
    }});
}

function append_to_table_annonce_list_html_of_page(i)
{
    $.ajax({url:"get_annonce_list_html/" + i,success:function(result)
    {
        //$("div#annonce_list_tmp").html(result);

        //ensuite j'appende le resultat a la table existante
        var cur_table = $('div#annonce_list table')[0];

        $("tr:not(:first-child)", result).each(function(index)
        {
            //if(index == 0)
            //{
            var last_tr = $("tr", cur_table).filter(':last-child')[0];
            $(cur_table).append(this);
            //}
        });
    }});
}

function refresh_request()
{
    var nb_pages = $("input#nb_pages")[0].value;

    for(var my_idx = 1; my_idx <= nb_pages; my_idx++)
    {
        $.ajax({url:"refresh_request_page_nb/" + my_idx,
                async: false, // sinon il incremente my_idx ...
        success:function(result)
        {
            update_nb_of_annoucements_found();

            generate_conditions_html();

            if(my_idx == 1)
            {
                generate_annonce_list_html_of_page(1);
            }
            else
            {
                append_to_table_annonce_list_html_of_page(my_idx);
            }

        }});

    }
}

function update_nb_of_annoucements_found()
{
    $.ajax({url:"get_nb_results_html/",success:function(result)
    {
        $("div#nb_results").html(result);
    }});   
}

function generate_parameters_html()
{
    $.ajax({url:"get_parameters_html/",success:function(result)
    {
        $("div#parameters").html(result);
    }});
}