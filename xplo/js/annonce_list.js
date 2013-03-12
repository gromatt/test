
function get_height_value(obj)
{
    var height_str = $(obj).css("height");
    var height_sub_str = height_str.substring(0, height_str.length-2)
    //pour la conversion en nombre
    return height_sub_str - 0
}

var bloc_desc_list = $("div.bloc_description");

$("div.bloc_description").each(function(index)
{
    var internal_bloc_list = $("div.bloc_description_internal", this);
    if(internal_bloc_list.length != 1)
    {
        alert("error " + internal_bloc_list.length);
    }
    var internal_bloc = internal_bloc_list[0];
    var bloc_height = get_height_value(this);
    var internal_bloc_height = get_height_value(internal_bloc);

    if(internal_bloc_height < bloc_height)
    {
        // pour centrer le texte
        var top = Math.round((bloc_height - internal_bloc_height)) * 0.5;

        $(internal_bloc).css("top", top + "px");
        //$(internal_bloc).css("background-color", "yellow");
    }
});

