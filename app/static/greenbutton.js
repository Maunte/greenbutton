$(document).ready( function() {
    $(document).on("click", ".id_select", function() {
        var data_pair = $(this).attr("data-pair");
        var data_group = $(this).attr("data-group");
        var group = document.querySelectorAll("[data-group='"+data_group+"']");
        for (i=0; i<group.length;i++) {
            if ($(group[i]).attr("data-pair") != data_pair) {
                if ($(group[i]).attr("type") == "text") {
                    $(group[i]).prop("disabled", true);
                }
            } else {
                $(group[i]).attr("disabled", false);
                $(group[i]).prop("checked", true);
            }
        }
    });
});