"use strict";

$(function () {
    // Give all links with a label this label as tooltip
    $(".label").each(function () {
        $(this).parent().attr("title", $(this).html());
    });

    // Setup Dropdown menus
    $(".dropdown").dropdownSetup({triggerHover: true});

    let responsiveFooter = function() {
        if (window.matchMedia("(max-width: " + window.breakpoints.narrow[1] + "px)").matches) {
            $("#footer").appendTo($("#wrapper"));
        } else {
            $("#footer").appendTo($("#sidebar"));
        }
    };
    window.addEventListener("resize", responsiveFooter);
    responsiveFooter();
});
