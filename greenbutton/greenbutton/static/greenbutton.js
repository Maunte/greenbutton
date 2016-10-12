$(document).ready( function() {

    // Form Error Handling *******************************************************************************************

    $(".form_div").submit( function(e) {
        var token = $("#access_token").val();
        if (token == "") {
            e.preventDefault();
            $("#access_token").addClass("form-control-warning");
            alert("Enter an Access Token");
        } else {
            $("<input />").attr("type", "hidden").attr("name", "access_token").attr("value", token).appendTo(this);
        }
    });

    $(document).on("click", ".batch_radio", function() {
        $(".batch_form").css("display", "none");
        $("#"+this.id.replace("radio", "form")).toggle();
    });

    $("#epower_form").submit( function() {

        if ($("#epower_quality_radio").is(":checked")) {
            document.epower_form.action = "electric-power-quality/";
        } else if ($("#epower_usage_radio").is(":checked")) {
            document.epower_form.action = "electric-power-usage/";
        } else {
            alert("Javascript Error!");
        }
    });

    $(document).on("click", "#toggle_xml", function() {
        $("#xml_div").toggle();
        var xml_display = $("#xml_div").css("display");
        var table_display = $("#table_div").css("display");
        if (xml_display != "none" && table_display != "none") {
            $("#table_div").toggle();
        }
    });
    $(document).on("click", "#toggle_table", function() {
        $("#table_div").toggle();
        var table_display = $("#table_div").css("display");
        var xml_display = $("#xml_div").css("display");
        if (table_display != "none" && xml_display != "none") {
            $("#xml_div").toggle();
        }
    });

    // Parsing Green Button Response object ***************************************************************************

});