"use strict";

$(function () {
    // Give all links with a label this label as tooltip
    $(".label").each(function () {
        $(this).parent().attr("title", $(this).html());
    });

    // Setup Dropdown menus
    $(".dropdown").dropdownSetup({triggerHover: false});
});
